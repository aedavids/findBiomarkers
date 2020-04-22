# findBiomarkers
searches for candidate biomarkers in RNA Sequence data

Author: Andrew E. Davidson
aedavids@ucsc.edu
[https://github.com/aedavids/findBiomarkers](https://github.com/aedavids/findBiomarkers)

## Starting notebooks
bin/startNotesbooks.sh  

## Installation

set up conda env with required packages

```
$ conda create --name findBiomarkers --file requirements.txt
```

you may need to install tensorflow and jupyter notebooks manually as follows

```
$ conda activate findBiomarkes
(findBiomarkers) $ pip install tensorflow
(findBiomarkers) $ pip install -q git+https://github.com/tensorflow/docs

(findBiomarkers) $ conda install -c conda-forge notebook
(findBiomarkers) $ conda install -c conda-forge jupyter_contrib_nbextensions
```

## Installation notes
- clone [https://github.com/aedavids/findBiomarkers](https://github.com/aedavids/findBiomarkers)
- download the required data set
  * you can find a copy at s3://bme-230a.santacruzintegration.com/tcga_target_gtex.h5
  * or run [Rob Curries' ingest notebook](https://github.com/rcurrie/tumornormal/blob/master/ingest.ipynb)

## Running Unit test
```
cd ~workSpace/UCSC/findBiomarkers
conda activate findBiomarkers
export PYTHONPATH="${PYTHONPATH}:`pwd`/src"
cd src/test
python -m unittest discover .
```
## Table of Contents

- [./documentation/dataDictionary](./documentation/dataDictionary)

Jupyter notebooks

- [lungCancerClassifierExploration.ipynb](./jupyterNotebooks/lungCancerClassifierExploration.ipynb)
    * basic exploration to get an idea of how to train a classifier
    
- [cancerExploration.ipynb](./jupyterNotebooks/cancerExploration.ipynb)
    * checks to see if data set is balanced. Use to suggest data sub sets to 
    train with

- [lungCancerClassifier.ipynb](./jupyterNotebooks/lungCancerClassifier.ipynb)
    * binary classifier    
    
- [lungCancerClassifierEvaluation.ipynb](./jupyterNotebooks/lungCancerClassifierEvaluation.ipynb)
    * How well does model work
    
- [TCGA_Target_GTexPrototype.ipynb](./jupyterNotebooks/TCGA_Target_GTexPrototype.ipynb)
    * used to develop dataUtilities/TCGA_Target_GTex.py
    
- [testTCGA_Target_GTex.ipynb](./jupyterNotebooks/testTCGA_Target_GTex.ipynb)
    * test  dataUtilities/TCGA_Target_GTex.py
    

Depecated Tree house notebooks
The use a data set the compins the TCGA-target-GTex data sets with tree house childhood cancer

lungCancerClassifierExploration-TreeHouse.ipynb
lungCancerClassifier-TreeHouse.ipynb
lungCancerClassifierEvaluation-Treehouse.ipynb

