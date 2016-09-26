#!/bin/bash

exclude="-e PERSON_ID -e GAME_ID -e CLOSE_DEF_PERSON_ID"
costFooKey="SHOT_RESULT"

#-------------------------------------------------
#      PARSE DATA INTO SOMETHING USEFUL

### generate player data using Alvaro's code
# writes output locally, paths are hard-coded 

echo -e "-------------------------------------------------\ngen_playerData.py\n-------------------------------------------------"

#   -> Playes_Games_Data.pkl 
echo gen_playerData.py

if [ $? != 0 ]
then
    exit 
fi

### generate shot data using Ryan's code
# using test files Ryan produced for now
#   -> collected_shot_data_2014.pkl
#   -> collected_shot_data_2014.pkl

### whiten data

echo -e "-------------------------------------------------\nwhiten.py\n-------------------------------------------------"

#   -> Playes_Games_Data_zeroMean.pkl
echo whiten.py -v -t -m zeroMean ${exclude} Playes_Games_Data.pkl

if [ $? != 0 ]
then
    exit
fi

#   -> collected_shot_data_2014_zeroMean.pkl
echo whiten.py -v -t -m zeroMean ${exclude} collected_shot_data_2014.pkl

if [ $? != 0 ]
then
    exit
fi

#-------------------------------------------------
#     CLUSTER (Unsupervised classification)


### cluster with Gaussian Mixture Model

echo -e "-------------------------------------------------\nclassify.py\n-------------------------------------------------"

#   -> Playes_Games_Data_zeroMean_GMM.pkl
echo classify.py -v -t ${exclude} -n 2 -m GMM --pklModel Playes_Games_Data_zeroMean_GMM-model.pkl Playes_Games_Data_zeroMean.pkl Playes_Games_Data_zeroMean.pkl #--plot

if [ $? != 0 ]
then
    exit
fi

### cluster with KMeans
#   -> Playes_Games_Data_zeroMean_KMeans.pkl
#classify.py -v -t ${exclude} -n 2 -m KMeans --pklModel Playes_Games_Data_zeroMean_KMeans-model.pkl Playes_Games_Data_zeroMean.pkl Playes_Games_Data_zeroMean.pkl --plot

if [ $? != 0 ]
then
    exit
fi

#-------------------------------------------------
#     MAP data together

echo -e "-------------------------------------------------\nmap.py\n-------------------------------------------------"

### GMM
echo map.py -v -t collected_shot_data_2014_zeroMean.pkl Playes_Games_Data_zeroMean_GMM.pkl mappedData_zeroMean_GMM.pkl

if [ $? != 0 ]
then
    exit
fi

### KMeans
#map.py -v -t collected_shot_data_2014_zeroMean.pkl Playes_Games_Data_zeroMean_KMeans.pkl mappedData_zeroMean_KMeans.pkl

if [ $? != 0 ]
then
    exit
fi

#-------------------------------------------------
#     Predict (Supervised regression of shot probability)

echo -e "-------------------------------------------------\nregress.py\n-------------------------------------------------"

### GMM
#   -> mappedData_zeroMean_GMM_RandomForest.pkl
echo regress.py -v -t ${exclude} -m RandomForest --pklModel mappedData_zeroMean_GMM_RandomForest-model.pkl ${costFooKey} mappedData_zeroMean_GMM.pkl mappedData_zeroMean_GMM.pkl

if [ $? != 0 ]
then
    exit
fi

### KMeans
#   -> mappedData_zeroMean_KMeans_RandomForest.pkl
#regress.py -v -t ${exclude} -m RandomForest --pklModel mappedData_zeroMean_KMeans_RandomForest-model.pkl ${costFooKey} mappedData_zeroMean_KMeans.pkl mappedData_zeroMean_KMeans.pkl

if [ $? != 0 ]
then
    exit
fi
