# Nima
# Modified SVR code from Wanlin Cui
import numpy as np
import math
from sklearn import svm
from ContextEngineBase import ContextEngineBase
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

## Implementation of the SVR algorithm:
class LinSVM(ContextEngineBase):
    svmObj = None  
    # testList = []
    #  Name of the file that contains the key for encryption/decryption
    def __init__(self, numInputs, outputClassifier, 
            inputClassifiers,appFieldsDict): 
        ContextEngineBase.__init__(self, numInputs, 
                outputClassifier, inputClassifiers, appFieldsDict)
        self.numInputs = numInputs
        self.outputClassifier = outputClassifier
        self.inputClassifiersList = inputClassifiers
        self.customFieldsDict = appFieldsDict
        self.svmObj = svm.LinearSVC()

    def printO(self):
        #print self.observationMatrix
        #print self.outputVector
        print self.testList
        

    def addBatchObservations(self, newInputObsMatrix, newOutputVector):
        if(len(newInputObsMatrix.shape) == 2 and newInputObsMatrix.shape[1] == self.numInputs
                and newOutputVector.shape[0] == newInputObsMatrix.shape[0]):
            #print("All good!")
            newOutputVector = newOutputVector.ravel()
            i = 0
            for newInputVector in newInputObsMatrix:
                newOutputValue = newOutputVector[i]
                self.addSingleObservation(newInputVector, newOutputValue)
                i += 1
        else:
            raise ValueError ("Wrong dimensions! %f" %newInputObsMatrix.shape[1])

    def train(self):
        if self.outputClassifier == 0:
            raise ValueError('Linear SVM output must be defined as discrete.')
        if (self.numObservations > 0):
            #print("Training started")
            self.svmObj.fit(self.observationMatrix, self.outputVectorIdx)
            return True
        else:
            raise ValueError ("Not enough observations to train!")
            return False

    def execute(self, inputObsVector):
        if(len(inputObsVector) == self.numInputs):
            #print("Begin execute")
            #x_Test = np.vstack((self.x_Test,inputObsVector))
            x_Test = np.reshape(inputObsVector,(1,self.numInputs))
            y_Test = self.svmObj.predict(x_Test)
            # self.testList.append(y_Test[0])
            return self.outputClustering.cluster_centers_[y_Test][0]
        else:
            raise ValueError ("Wrong dimensions, fail to execute")
            return None
