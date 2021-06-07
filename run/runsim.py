import operator
import functools as ft 
import matplotlib.pyplot as plt
import numpy as np
from models import sch, vadModel
from tools.functions import runkut4, runkut4_ECG, ECG_McSharry, equacoes_ECG
from tools.plot import runPlot, runCSV
from tools.printTool import initPrint
from tqdm import tqdm
from init import Data
from config.Cmd import Cmd  
from tools.read import readFromFile
import scipy as scipy
from scipy.optimize import minimize, rosen, rosen_der, root
import csv   

it_ = 1

print("Criando instância do modelo...")

model = sch.Simaan()
model.setECG()
model.eletricalParameters()

def runsim(theta):

  global model

  model.diode_reset()
  vad = vadModel.VAD(model, 
    deltaPVAD=theta[6]
  )
  vad.x.extend(model.x)

  global it_ 
  print("Iteração nº" + str(it_), end=" -> ")
  it_ += 1
  # initPrint('Preparing Simulation with ventricular assist device...\nThis can take a while.')

  #x = [pao qa Vve Pas Pae Qi Qo V_vad]
  vad.b0 = theta[0]
  vad.b1 = theta[1]
  vad.b2 = theta[2]
  vad.a0 = theta[3]
  vad.a1 = theta[4]
  vad.a2 = theta[5]

  ii = 0
  ejectmode = 'Sync'

  for i in range(model.n-1):
      #ramp function
      model.rampFunction(i, vad)
      vad.valveManager(i, model)
      vad.modeManager(i, ii, ejectmode)
      # Calculate de External Bladder pressure from the Drive Pressure]
      A2 = -1/(vad.Rd*vad.Cd)
      B2 = -A2

      vad.Pex = runkut4(model.passo,A2,vad.Pex,B2,vad.Pd)
      vad.Pex2 = vad.Pex + np.dot(vad.xdot[2],0.15)
      vad.Ri = vad.Ri0 + np.exp(-0.25*vad.x[5])
      vad.Ro = 0.00015*np.absolute(vad.Qo[i]) + 0.05

      xo, xi, zi, zo, ri, ro, rri, rro = vad.returnValues()

      delta = (model.Dm/model.Rm)  + (model.Da/model.Ra)
      a11 = xi*ro - rri
      a12 = ri - xi*rro
      a13 = (xi*zo - zi)/vad.Cp
      a16 = zi*(model.Ea[i] + model.Emin)
      a21 = ro - xo*rri
      a22 = xo*ri - rro
      a23 = (zo - xo*zi)/vad.Cp
      a26 = xo*zi*(model.Ea[i] + model.Emin)
      a46 = (model.Da/model.Ra)*(model.Ea[i] + model.Emin)
      a66 =  -delta*(model.Ea[i] + model.Emin)
      a86 = (model.Dm/model.Rm)*(model.Ea[i] + model.Emin)
      a88 = -((1/model.Rs) + model.Dm/model.Rm)

      #A e B são matrizes variantes no tempo
      A = np.zeros((8,8), dtype=float)
      
      A[0] = np.true_divide([a11, a12, a13, -xi*zo, 0, a16, 0,0],(1-xi*xo))
      A[1] = np.true_divide([a21, a22, a23, -zo, 0, a26, 0,0],(1-xi*xo))
      A[2] = [1, -1, 0, 0, 0, 0, 0, 0]
      A[3] = np.true_divide([0,1,0, -model.Da/model.Ra, -1, a46, 0, 0],model.Cao)
      A[4] = np.true_divide([0,0,0, 1, -model.Rc, 0, -1, 0],model.Ls)
      A[5] = [-1,0,0, model.Da/model.Ra, 0, a66, 0, model.Dm/model.Rm]
      A[6] = np.true_divide([0,0,0, 0, 1, 0, -1/model.Rs, 1/model.Rs],model.Cs)
      A[7] = np.true_divide([0,0,0, 0, 0, a86, 1/model.Rs, a88],model.Cae)

      #Matriz B, 5X1
      B = np.zeros((8,4), dtype=float)

      B[0,0] = -A[0][2]
      B[1,0] = -A[1][2]
      B[0,1] = A[0][2]*vad.Cp
      B[1,1] = A[1][2]*vad.Cp

      for i_index in range(8):
        B[i_index,2] = -A[i_index][5]
        B[i_index,3] = -A[i_index][5]*(model.Emin*model.dV)/(model.Ea[i]+model.Emin)
      
      vad.x = runkut4(model.passo,A,vad.x,B,[vad.Vd_vad, vad.Pex2, model.Vd, 1])
      vad.xdot = np.dot(A,vad.x) + np.dot(B,[vad.Vd_vad, vad.Pex2, model.Vd, 1])
      vad.gammad[i+1] = vad.gammad[i] + model.passo/model.tc
    
      if vad.gammad[i+1] >= 1:
        ii = ii + 1
        vad.gammaHandler(i+1, ii)

      #Reference Change
      vad.refereceChange(i)
      vad.att(model,i+1)

      model.Pve[i + 1] = (model.Vve[i + 1] - model.Vd)*(model.Ea[i + 1] + model.Emin) - model.Emin*model.dV
      vad.Pee[i + 1] = vad.Pe[ii]

  error_init = 49999

  error = list(abs(np.array(vad.mPao_ref_v[error_init:]) - np.array(vad.mPao_v[error_init:])))
  J = np.dot(error,model.T[error_init:])

  result_str = 'Valores de theta: ' + str(theta) + ' J:' + str(J) + "\n"
  print(result_str, end="")

  #PLOT
  # with open("./plotResults/mini_withPVAD/mini_results_withPVAD.csv", "a") as file_object:
  #   writer = csv.writer(file_object)
  #   writer.writerow(np.append(theta, J))

  runPlot(model, vad)
  runCSV(model, vad)
  return J

  plt.figure(figsize=(5,5))
  plt.ylim(70, 120)
  plt.xlim(0,10)
  plt.xlabel('Tempo(s)')
  plt.ylabel('Pressão(mmHg)')
  plt.plot(model.T, vad.mPao_v, label='Pressão na aorta')
  plt.plot(model.T, vad.mPao_ref_v, 'r--',label='Valor de referência de pressão na aorta')
  plt.legend()
  str_output = './plotResults/mini_withPVAD/fig_' + str(it_ - 1) + '.png' 
  plt.savefig(str_output)
  plt.close()
  #PLOT
  
  return J

bnds = ((0,None), (0, None), (0, None), (0,None), (0, None), (0, None), (0, 1))
result = minimize(runsim, [49.0, -22.0, 5.0, 9, -10, 1, 0.4], method='Nelder-Mead', bounds=bnds, options={'maxiter' : 100})

# print(result)

# runsim([49.0, -22.0, 5.0, 9, -10, 1, 0.4])

#runsim([440693,-155075, 38767, 105016, -105072, 1.4, 0.4])