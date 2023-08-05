#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ecnet/error_utils.py
# v.1.6.0
# Developed in 2018 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains functions necessary creating, training, saving, and reusing neural
# network models
#

# Stdlib imports
import pickle
from pickle import dump, load
from functools import reduce
from os import environ, mkdir, path

# 3rd party imports
import tensorflow as tf
from tensorflow import add, global_variables_initializer, matmul, nn
from tensorflow import placeholder, random_normal, reset_default_graph
from tensorflow import Session, square, train, Variable
from numpy import asarray, sqrt as nsqrt

environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def __linear_fn(n):
    '''
    Linear definition for activation function dictionary
    '''
    return n


ACTIVATION_FUNCTONS = {
    'relu': nn.relu,
    'sigmoid': nn.sigmoid,
    'softmax': nn.softmax,
    'linear': __linear_fn
}


class Layer:
    '''
    Layer object: contains layer size (number of neurons), activation function
    '''

    def __init__(self, size, act_fn):

        self.size = size
        if act_fn not in ACTIVATION_FUNCTONS.keys():
            raise ValueError(
                'Unsupported activation function {}'.format(act_fn)
            )
        self.act_fn = ACTIVATION_FUNCTONS[act_fn]


class MultilayerPerceptron:
    '''
    Neural network (multilayer perceptron): contains methods for adding layers
    with specified neuron counts and activation functions, training the model,
    using the model on new data, saving the model for later use, and reusing a
    previously trained model
    '''

    def __init__(self, id=0):
        '''
        Initialization of object
        '''

        self.__layers = []
        self.__weights = []
        self.__biases = []
        self.__id = id
        if not path.isdir('./tmp/'):
            mkdir('./tmp/')
        reset_default_graph()

    def add_layer(self, size, act_fn):
        '''
        Add a layer to the model

        *size*      - number of neurons in the layer
        *act_fn*    - activation function for the layer:
        '''

        self.__layers.append(Layer(size, act_fn))

    def connect_layers(self):
        '''
        Connects the layers in self.layers, generating weights between layers
        and biases for each layer
        '''

        for layer in range(len(self.__layers) - 1):
            self.__weights.append(
                Variable(random_normal([
                    self.__layers[layer].size,
                    self.__layers[layer + 1].size
                ]), name='W_fc{}'.format(layer + 1))
            )
        for layer in range(1, len(self.__layers)):
            self.__biases.append(
                Variable(random_normal([
                    self.__layers[layer].size
                ]), name='B_fc{}'.format(layer))
            )

    def fit(self, x_l, y_l, learning_rate, train_epochs):
        '''
        Fits the neural network model

        *x_l*   - learning input data
        *y_l*   - learning targets
        *learning_rate* - learning rate
        *train_epochs*  - number of training steps (epochs)
        '''

        if len(y_l) is 0 or len(x_l) is 0:
            raise ValueError('Learning set cannot be empty - check data split')

        x = placeholder('float', [None, self.__layers[0].size])
        y = placeholder('float', [None, self.__layers[-1].size])

        pred = self.__feed_forward(x)
        cost = square(y - pred)
        optimizer = train.AdamOptimizer(
            learning_rate=learning_rate
        ).minimize(cost)

        with Session() as sess:
            sess.run(global_variables_initializer())
            for _ in range(train_epochs):
                sess.run(optimizer, feed_dict={x: x_l, y: y_l})
            saver = train.Saver()
            saver.save(sess, './tmp/_m{}/_ckpt'.format(self.__id))
        sess.close()

    def fit_validation(self, x_l, y_l, x_v, y_v, learning_rate, max_epochs):
        '''
        Fits the neural network model, using periodic validation to determine
        when to stop learning (when validation performance stops improving)
        '''

        if len(y_l) is 0 or len(x_l) is 0:
            raise ValueError(
                'Learning set cannot be empty - check data split'
            )
        if len(y_v) is 0 or len(x_v) is 0:
            raise ValueError(
                'Validation set cannot be empty - check data split'
            )

        x = placeholder('float', [None, self.__layers[0].size])
        y = placeholder('float', [None, self.__layers[-1].size])

        pred = self.__feed_forward(x)
        cost = square(y - pred)
        optimizer = train.AdamOptimizer(
            learning_rate=learning_rate
        ).minimize(cost)

        with Session() as sess:
            sess.run(global_variables_initializer())

            valid_rmse_lowest = 100
            current_epoch = 0

            while current_epoch < max_epochs:
                sess.run(optimizer, feed_dict={x: x_l, y: y_l})
                current_epoch += 1
                if current_epoch % 250 == 0:
                    valid_rmse = self.__calc_rmse(
                        sess.run(pred, feed_dict={x: x_v}), y_v
                    )
                    if valid_rmse < valid_rmse_lowest:
                        valid_rmse_lowest = valid_rmse
                    elif valid_rmse > valid_rmse_lowest + (
                        0.05 * valid_rmse_lowest
                    ):
                        break

            saver = train.Saver()
            saver.save(sess, './tmp/_m{}/_ckpt'.format(self.__id))
        sess.close()

    def use(self, x):
        '''
        Use the neural network on input data *x*, returns predicted values
        '''

        with Session() as sess:
            saver = train.Saver()
            saver.restore(sess, './tmp/_m{}/_ckpt'.format(self.__id))
            results = self.__feed_forward(x).eval()
        sess.close()
        return results

    def save(self, filepath):
        '''
        Saves the neural network to *filepath* for later use
        '''

        with Session() as sess:
            saver = train.Saver()
            saver.restore(sess, './tmp/_m{}/_ckpt'.format(self.__id))
            saver.save(sess, filepath)
        sess.close()
        architecture_file = open('{}.struct'.format(filepath), 'wb')
        dump(self.__layers, architecture_file)
        architecture_file.close()

    def load(self, filepath):
        '''
        Loads a neural network model found at *filepath*
        '''

        architecture_file = open('{}.struct'.format(filepath), 'rb')
        self.__layers = load(architecture_file)
        self.connect_layers()
        with Session() as sess:
            saver = train.Saver()
            saver.restore(sess, filepath)
            saver.save(sess, './tmp/_m{}/_ckpt'.format(self.__id))
        sess.close()

    def __feed_forward(self, x):
        '''
        Private method: feeds data through the neural network, returns output
        of final layer
        '''

        output = x
        for idx, layer in enumerate(self.__layers[1:]):
            output = layer.act_fn(
                add(matmul(
                    output,
                    self.__weights[idx]
                ), self.__biases[idx])
            )
        return output

    def __calc_rmse(self, y_hat, y):
        '''
        Private method: calculates the RMSE of the validation set during
        validation training
        '''

        try:
            return(nsqrt(((y_hat - y)**2).mean()))
        except:
            return(nsqrt(((asarray(y_hat) - asarray(y))**2).mean()))
