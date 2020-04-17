# findBiomarkers
searches for candidate biomarkers in RNA Sequence data

Author: Andrew E. Davidson
aedavids@ucsc.edu
[https://github.com/aedavids/findBiomarkers](https://github.com/aedavids/findBiomarkers)

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

## Starting notebooks

```
cd ~workSpace/UCSC/findBiomarkers
conda activate findBiomarkers
export PYTHONPATH="${PYTHONPATH}:`pwd`/src"
jupyter notebook
```
## Running Unit test
```
cd ~workSpace/UCSC/findBiomarkers
conda activate findBiomarkers
export PYTHONPATH="${PYTHONPATH}:`pwd`/src"
cd src/test
python -m unittest discover .
```
## Table of Contents
Jupyter notebooks

- [lungCancerClassifierExploration.ipynb](./jupyterNotebooks/lungCancerClassifierExploration.ipynb)
    * AEDWIP laslsls

- [lungCancerClassifier.ipynb](./jupyterNotebooks/lungCancerClassifier.ipynb)
    * AEDWIP trains a model
    
- [lungCancerClassifierExploration.ipynb](./jupyterNotebooks/lungCancerClassifierExploration.ipynb)
    * evaluates model