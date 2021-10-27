## Para 1ª execução, realize uma das opções abaixo:

Import automático:

```
python init.py -m initproject  
```

Manualmente com pip:

``
pip install -r requirements.txt
``

``
pip install -e .
``

## Run via código:

```python
from run.Simulation import Simulation

Simulation.startSimulation(mode='vad', inputPath='./input.txt')

````

## Run via terminal:

``
python init.py -m vad .\input.txt
``

``
python init.py -m test .\input.txt
``

``
python init.py -m simaan
``


ps. Os valores de simulações podem ser alterados em input.txt