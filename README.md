# Deep_learning

## Table of contents
* [General info](#general-info)
* [Libraries](#libraries)
* [Data preprocessing](#data-preprocessing)
* [Data exploration ](#data-exploration)
* [Model architecture](#model-architecture)
* [Evaluation](#evaluation)
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
This resulted in 31213 tiles, which interfered with training. Therefore, the tiles were filtered and only the tiles that contained at least on parking lot pixel were kept. In a second folder, all tiles that contain above median amount of parking lot pixels were copied, code can be found in [data_preparation.py](data_preparation.py). The folder was created to serve as addtional tiles for the implementation of Curriculum Learning as described in [ParkingLotDetection_allmodels.ipynb](ParkingLotDetection_allmodels.ipynb). Finally, all testing data present in the above median images was filtered out, code can be found here [Filter_masks_above_median.ipynb](Filter_masks_above_median.ipynb). 

## Data exploration 
The final dataset contained 8260 tiles before augmentation. With a class splitting of  89,7% non-parking lot pixel: 121325908 and 10,3% of parking lot pixel: 14005932. Due to the imbalanced dataset, class weights were calculated and applied in the learning designed. The median amount of parkinglot pixels in the dataset amounted to 945 pixel. Further explorations can be found in [data_exploration_final.ipynb](data_exploration_final.ipynb). 

## Model architectures
Three models were setup for training: u-net model, VGG16 in combination with u-net and a deeplabv3plus. The code to run the dataset on the models can be found on [ParkingLotDetection_allmodels.ipynb](ParkingLotDetection_allmodels.ipynb). 

## Evaluation 
An evaluation script was set up containing Loss and Accuracy plotting, and code to calculate tthe following evaluation metrics: Intersection of Union, Precision, Recall and F1-Score. Also to be found in [ParkingLotDetection_allmodels.ipynb](ParkingLotDetection_allmodels.ipynb). 

## Contributors
Marlene Bauer (marlene.bauer@stud-mail.uni-wuerzburg.de)  
Anna Bischof (anna.bischof@stud-mail.uni-wuerzburg.de)  
Christina Krause (christina.krause@stud-mail.uni-wuerzburg.de)  
