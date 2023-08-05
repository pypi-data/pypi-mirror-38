"""
================================================================================
dev_met2img.py : Predicting diseases based on images (EMBEDDINGs) 
        with stratified cross-validation (including support building images and training)
================================================================================
Author: Team Integromic, ICAN, Paris, France' 
(**this version is still developping)
date: 25/12/2017' (updated to 30/10/2018)

function : run n times (cross validation) using embeddings 
    with fillup and manifold algorithms (t-SNE, LDA, isomap,...) 
    support color, gray images with manual bins or bins learned from training set
====================================================================================================================
Steps: 
1. set variables, naming logs and folder for outputs, inputs (images)
2. read original data from excel file including data (*_x.csv), labels (*_y.csv)
3. Split data into stratified kfolds, then applying dimension reduction, transformation... 
4. load and call model
5. training and evaluate on validation set
6. summarize results, compute metric evaluation, average accuracy, auc each run, the experiment, and show on the screen, also save log.
====================================================================================================================
Input: 2 csv files, 1 for data (*_x.csv), 2 for labels (*_y.csv)
Output: 3 files (*.txt) of log on general information of the experiment in folder './results/' (default), 
    AND images (*.png) in folder './images/' (if not exist in advance)
    AND numerous files (*.txt) stored acc,loss at each epoch in folder results/<folder_of_dataset>/details
    AND numerous files (*.json) of models in folder results/<folder_of_dataset>/models

Metric evaluation: Accuracy, Area Under Curve (AUC), 
    Average True Negative (tn), Averaged False Negative (fn), Averaged True Negative (fp), Averaged True Positive (tp)	
    Precision (preci), Recall, F1-score	(f1), MCC
    Execution time, epoch stopped using Early Stopping

File 2,3 to take overview results after each k-fold-cv, file 1 for detail of each fold
'file 1: parameters; selected hyperparameters/labels/performance of each fold; 
    the final results of the experiment is at the last line
    the name of this file appended "ok" as finishes
'file 2: mean at the beginning and finished of acc, loss of train/val; the execution time; 
    the mean/sd of these at the last line
'file 3: mean at acc (computed based on averaged confusion matrix for cross-check)/auc/confusion matrix (tn,tp,fn,tn);
    tn: true negative, tp: true positive, fn: false negative, fp: false positive, and Matthews corrcoef (MMC)
    the mean/sd of these at the last line    
====================================================================================================================
"""

#get parameters from command line
import experiment
options, args = experiment.para_cmd()

#check if read parameters from configuration file
import os
if options.config_file <> '':
    if os.path.isfile(options.config_file):
        experiment.para_config_file(options)
        #print options
    else:
        print 'config file does not exist!!!'
        exit()

#check whether parameters all valid
experiment.validation_para(options)
   
#select run either GPU or CPU
if options.cudaid > -1 and options.cudaid <= 10 : #if >10 get all gpus and memories
    #use gpu
    print 'gpu: ' + str(options.cudaid)    
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = str(options.cudaid)
elif  options.cudaid <= -1:
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

if __name__ == "__main__":   
    if options.type_run in ['vis','visual']:
        experiment.deepmg_visual(options,args)
    elif options.type_run in ['learn']:
        if options.test_size in [0,1]:
            experiment.run_kfold_deepmg(options,args)
            
        else: #if set the size of test set, so use holdout validation
            experiment.run_holdout_deepmg(options,args)
    

 