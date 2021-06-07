import operator
import functools as ft 
import matplotlib.pyplot as plt
import numpy as np
import os
_path = os.path.abspath(__file__) 
path = './plotResults/'

#PLOT VAD
#plt.plot(model.T, vad.mPao_ref_v)
def runPlot(model, vad):

    print("\rPlotting...", end='')
    plt.figure(figsize=(5,5))
    plt.xlabel('Tempo(s)')
    plt.ylabel('Pressão(mmHg)')

    plt.plot(model.T, vad.mPao_v, label='Pressão na aorta')
    plt.plot(model.T, vad.mPao_ref_v, 'r--',label='Valor de referência de pressão na aorta')
    plt.legend()
    plt.savefig('./plotResults/fig1.png')

    plt.figure(figsize=(5,5))
    plt.xlabel('Tempo(s)')
    plt.ylabel('Pressão(mmHg)')

    plt.plot(model.T, model.Pao,label='Pressão na aorta')
    plt.plot(model.T, np.dot(vad.deltaS,np.max(model.Pao)),label='Instante de ejeção do ventrículo esquerdo')
    plt.plot(model.T, np.dot(vad.deltaPVAD,np.max(model.Pao)),'g--',label='Instante de ejeção do DAV')
    plt.legend()
    plt.savefig('./plotResults/fig2.png', bbox_inches='tight')

    plt.figure(figsize=(5,5))
    plt.xlabel('Tempo(s)')
    plt.ylabel('Volume(ml)')

    plt.plot(model.T, vad.Pee, label='Pressão de ejeção')
    plt.legend()    
    plt.savefig('./plotResults/fig3.png', bbox_inches='tight')

    #plt.plot(model.Vve, vad.Ri)
    #plt.title('Modelo de colapso ventricular; Resistência de entrada do DAV em função do volume ventricular')
    #plt.show()

    #plt.plot(model.Pao)
    #plt.title('Modelo de colapso ventricular; Resistência de entrada do DAV em função do volume ventricular')
    #plt.show()
    #PLOT

    plt.figure(figsize=(5,5))
    plt.plot(model.T, model.Pve)
    plt.plot(model.T, model.Pao, 'r--')
    plt.xlabel('Tempo(s)')
    plt.ylabel('Pressão(mmHg)')
    plt.savefig('./plotResults/fig4.png', bbox_inches='tight')

    plt.figure(figsize=(5,5))
    plt.plot(model.Vve)
    plt.savefig(path + 'fig5.png', bbox_inches='tight')
    plt.xlabel('Tempo(s)')
    plt.ylabel('Volume(ml)')

    plt.figure(figsize=(5,5))
    plt.plot(model.Qa)
    plt.savefig('./plotResults/fig6.png', bbox_inches='tight')

    plt.figure(figsize=(5,5))
    plt.xlabel('Tempo(s)')
    plt.ylabel('Fluxo de bombeamento no DAV (ml/s)')

    plt.plot(model.T,vad.Qi,label='Entrada')
    plt.plot(model.T,vad.Qo,'r--',label='Saída')
    plt.legend()

    plt.savefig('./plotResults/fig7.png', bbox_inches='tight')

    plt.figure(figsize=(5,5))
    plt.plot(model.Pve, model.Vve)
    plt.title('')
    plt.savefig('./plotResults/fig8.png', bbox_inches='tight')

    #SUBPLOT
    fig, axs = plt.subplots(2)
    fig.suptitle('Resultados')
    axs[0].plot(model.T, vad.mPao_v, label='Pressão na aorta')
    axs[0].plot(model.T, vad.mPao_ref_v, 'r--',label='Valor de referência de pressão na aorta')
    axs[1].plot(model.T, vad.Pee, label='Pressão de ejeção')
    fig.savefig('./plotResults/full_figure.pdf', bbox_inches='tight', pad_inches=1, cmap="gray")
    #SUBPLOT

    print('\rPlot is ready at ' + path)


def runCSV(model, vad):
    import csv  
    with open(path + 'output_40.csv', 'w', encoding='utf-8', newline=''    ) as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        writer.writerow(['Time (ms)', 'Pao', 'Qa', 'Vve', 'Pas', 'Pae', 'Pve'])
        
        for i in range(len(model.Pao)):
            writer.writerow(np.around([(i + 1)/10 , model.Pao[i],model.Qa[i], model.Vve[i], model.Pas[i], model.Pae[i], model.Pve[i]], 3))
   
    with open(path + 'output_pvad_40.csv', 'w', encoding='utf-8', newline=''    ) as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        writer.writerow(['mPao_ref_v', 'mPao_v', 'Pee', 'deltaS', 'deltaP' 'Qi', 'Qo'])
        
        for i in range(len(vad.mPao_v)):
            writer.writerow(np.around([vad.mPao_ref_v[i], vad.mPao_v[i], vad.Pee[i], vad.deltaS[i], vad.deltaPVAD[i], vad.Qi[i], vad.Qo[i]]))
            