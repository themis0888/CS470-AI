# -*- coding: utf-8 -*-

import classificationMethod
import numpy as np
import util

def softmax(X):
  e = np.exp(X - np.max(X))
  det = np.sum(e, axis=1)
  return (e.T / det).T

def sigmoid(X):
  return 1. / (1.+np.exp(-X))

def ReLU(X):
  return X * (X > 0.)

def binary_crossentropy(true, pred):
  pred = pred.flatten()
  return -np.sum(true * np.log(pred) + (1.-true) * np.log(1.-pred))

def categorical_crossentropy(true, pred):
  return -np.sum(np.log(pred[np.arange(len(true)), true]))

class NeuralNetworkClassifier(classificationMethod.ClassificationMethod):
  def __init__(self, legalLabels, type, seed):
    self.legalLabels = legalLabels
    self.type = type
    self.hiddenUnits = [100, 100]
    self.numpRng = np.random.RandomState(seed)
    self.initialWeightBound = None
    self.epoch = 1000

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method.
    Iterates several learning rates and regularization parameter to select the best parameters.

    Do not modify this method.
    """
    if len(self.legalLabels) > 2:
      zeroFilledLabel = np.zeros((trainingData.shape[0], len(self.legalLabels)))
      zeroFilledLabel[np.arange(trainingData.shape[0]), trainingLabels] = 1.
    else:
      zeroFilledLabel = np.asarray(trainingLabels).reshape((len(trainingLabels), 1))

    trainingLabels = np.asarray(trainingLabels)

    self.initializeWeight(trainingData.shape[1], len(self.legalLabels))
    for i in xrange(self.epoch):
      netOut = self.forwardPropagation(trainingData)

      # If you want to print the loss, please uncomment it
      # print "Step: ", (i+1), " - ", self.loss(trainingLabels, netOut)

      self.backwardPropagation(netOut, zeroFilledLabel, 0.02 / float(len(trainingLabels)))

    # If you want to print the accuracy for the training data, please uncomment it
    # guesses = np.argmax(self.forwardPropagation(trainingData), axis=1)
    # acc = [guesses[i] == trainingLabels[i] for i in range(trainingLabels.shape[0])].count(True)
    # print "Training accuracy:", acc / float(trainingLabels.shape[0]) * 100., "%"

  def initializeWeight(self, featureCount, labelCount):
    """
    Initialize weights and bias with randomness.

    Do not modify this method.
    """
    self.W = []
    self.b = []
    curNodeCount = featureCount
    self.layerStructure = self.hiddenUnits[:]

    if labelCount == 2:
      self.outAct = sigmoid
      self.loss = binary_crossentropy
      labelCount = 1 # sigmoid function makes the scalar output (one output node)
    else:
      self.outAct = softmax
      self.loss = categorical_crossentropy

    self.layerStructure.append(labelCount)
    self.nLayer = len(self.layerStructure)

    for i in xrange(len(self.layerStructure)):
      fan_in = curNodeCount
      fan_out = self.layerStructure[i]
      if self.initialWeightBound is None:
        initBound = np.sqrt(6. / (fan_in + fan_out))
      else:
        initBound = self.initialWeightBound
      W = self.numpRng.uniform(-initBound, initBound, (fan_in, fan_out))
      b = self.numpRng.uniform(-initBound, initBound, (fan_out, ))
      self.W.append(W)
      self.b.append(b)
      curNodeCount = self.layerStructure[i]

  def forwardPropagation(self, trainingData):
    """
    Fill in this function!

    trainingData : (N x D)-sized numpy array
    - N : the number of training instances
    - D : the number of features
    RETURN : output or result of forward propagation of this neural network

    Forward propagate the neural network, using weight and biases saved in self.W and self.b
    You may use self.outAct and ReLU for the activation function.
    Note the type of weight matrix and bias vector:
    self.W : list of each layer's weights, while each weights are saved as NumPy array
    self.b : list of each layer's biases, while each biases are saved as NumPy array
    - D : the number of features
    - C : the number of legal labels
    Also, for activation functions
    self.outAct: (automatically selected) output activation function
    ReLU: rectified linear unit used for the activation function of hidden layers
    """
    W, a, z = [], [], []
    "*** YOUR CODE HERE ***"
    W.append(trainingData.dot(self.W[0]))
    z.append(W[0] + self.b[0])
    a.append(ReLU(z[0]))

    W.append(a[0].dot(self.W[1]))
    z.append(W[1] + self.b[1])
    a.append(ReLU(z[1]))
    
    W.append(a[1].dot(self.W[2]))
    z.append(W[2] + self.b[2])
    a.append(self.outAct(z[2]))

    self.memory   = (trainingData, self.b, self.W, W, a, z)
    self.depth    = len(a)
    
    return a[len(a)-1]

  def backwardPropagation(self, netOut, trainingLabels, learningRate):
    """
    Fill in this function!

    netOut : output or result of forward propagation of this neural network
    trainingLabels: (D x C) 0-1 NumPy array
    learningRate: python float, learning rate parameter for the gradient descent

    Back propagate the error and update weights and biases.

    Here, 'trainingLabels' is not a list of labels' index.
    It is converted into a matrix (as a NumPy array) which is filled to 0, but has 1 on its true label.
    Therefore, let's assume i-th data have a true label c, then trainingLabels[i, c] == 1
    Also note that if this is a binary classification problem, the number of classes
    which neural network makes is reduced to 1.
    So to match the number of classes, for the binary classification problem, trainingLabels is flatten
    to 1-D array.
    (Here, let's assume i-th data have a true label c, then trainingLabels[i] == c)

    It looks complicated, but it is simple to use.
    In conclusion, you may use trainingLabels to calcualte the error of the neural network output:
    delta = netOut - trainingLabels
    and do back propagation as a manual.
    """

     
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    dz, da = [[0 for i in range(self.depth)] for i in range(2)]
    dW, db = [], []
    X,b,W,WW,a,z = self.memory
    delta = netOut - trainingLabels

    da[2] = delta.dot(W[2].T).reshape(a[1].shape)
    dz[2] = np.array(da[2], copy=True)
    dz[2][z[1] <= 0] = 0

    da[1] = dz[2].dot(W[1].T).reshape(a[0].shape)
    dz[1] = np.array(da[1], copy=True)
    dz[1][z[0] <= 0] = 0

    db.append(np.sum(dz[1], axis=0))
    db.append(np.sum(dz[2], axis=0))
    db.append(np.sum(delta, axis=0))
    dW.append((X.T).dot(dz[1]))
    dW.append((a[0].T).dot(dz[2]))
    dW.append((a[1].T).dot(delta))
    
    self.W = [W[0]-learningRate*dW[0], W[1]-learningRate*dW[1], W[2]-learningRate*dW[2]]
    self.b = [b[0]-learningRate*db[0], b[1]-learningRate*db[1], b[2]-learningRate*db[2]]


  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.

    Do not modify this method.
    """
    logposterior = self.forwardPropagation(testData)

    if self.outAct == softmax:
      return np.argmax(logposterior, axis=1)
    elif self.outAct == sigmoid:
      return logposterior > 0.5


