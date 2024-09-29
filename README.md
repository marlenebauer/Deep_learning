# Deep_learning

## Table of contents
* [General info](#general-info)
* [Libraries](#libraries)
* [Data preprocessing](#data-preprocessing)
* [Model architecture](#model-architecture)
* [Contributors](#contributors)

## General info
This repository contains the code and resources for a deep learning model developed for parking lot detection and segmentation from aerial images at a 40 cm spatial resolution. The project focuses on analyzing parking lots in the city of Würzburg, using high-resolution aerial imagery. Accurate detection of parking lots is crucial for urban planning and environmental management, as excessive parking space contributes to soil sealing—the covering of natural land with impervious surfaces like asphalt, which prevents water absorption, disrupts ecosystems, and exacerbates urban heat islands. Monitoring parking infrastructure can support sustainable urban development by identifying areas for green space reclamation or optimizing land use. This work was conducted as part of the course module "Advanced Deep Learning".

## Libraries
numpy 1.26.4  
keras 3.4.1  
tensorflow 2.17.0  
tensorflow-datasets 4.9.6  
tf-keras 2.17.0  
glob 0.7  
matplotlib 3.7.1  

## Data preprocessing
The data preprocessing involves three key steps: (1) digitizing all parking lots from randomly selected aerial tiles of Würzburg using a combination of OpenStreetMap (OSM) data and manual mapping for accuracy; (2) clipping the large 2500x2500 pixel aerial tiles (40 cm resolution) into smaller 128x128 pixel tiles with overlapping edges to improve model performance; and (3) saving the resulting training tiles in .npy format for further use in model training. Code can be found in [data_preprocessing.py](data_preprocessing.py).

## Model architectures

## Contributors
Marlene Bauer (marlene.bauer@stud-mail.uni-wuerzburg.de)  
Anna Bischof (anna.bischof@stud-mail.uni-wuerzburg.de)  
Christina Krause (christina.krause@stud-mail.uni-wuerzburg.de)  
