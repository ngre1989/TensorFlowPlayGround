#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 06:38:54 2017

@author: shengtanwu

Autoencoder Example
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/",one_hot = False)

learning_rate = 0.01

training_epochs = 20

batch_size = 256

display_step = 4

examples_to_show = 20

#Network Parameters
n_input = 784

# tf Graph input(only pictures)
X = tf.placeholder(tf.float32,[None,n_input])

# hidden layer settings
# 1st and 2nd layer num features
# hidden layer settings
n_hidden_1 = 256 # 1st layer num features
n_hidden_2 = 128 # 2nd layer num features
weights = {
    'encoder_h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'encoder_h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'decoder_h1': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_1])),
    'decoder_h2': tf.Variable(tf.random_normal([n_hidden_1, n_input])),
}
biases = {
    'encoder_b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'encoder_b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'decoder_b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'decoder_b2': tf.Variable(tf.random_normal([n_input])),
}

# Building the encoder
def encoder(x):
    # Encoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['encoder_h1']),
                                   biases['encoder_b1']))
    # Decoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['encoder_h2']),
                                   biases['encoder_b2']))
    return layer_2


# Building the decoder
def decoder(x):
    # Encoder Hidden layer with sigmoid activation #1
    layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['decoder_h1']),
                                   biases['decoder_b1']))
    # Decoder Hidden layer with sigmoid activation #2
    layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['decoder_h2']),
                                   biases['decoder_b2']))
    return layer_2

#construct model
encoder_op = encoder(X)
decoder_op = decoder(encoder_op)

#prediction
y_pred = decoder_op

#Targets(Labels) are the input data
y_true = X

cost = tf.reduce_mean(tf.pow(y_true-y_pred,2))
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

# Let's Goooooo!
with tf.Session() as sess:
    # tf.initialize_all_variables() no long valid from
    # 2017-03-02 if using tensorflow >= 0.12
    if int((tf.__version__).split('.')[1]) < 12 and int((tf.__version__).split('.')[0]) < 1:
        init = tf.initialize_all_variables()
    else:
        init = tf.global_variables_initializer()
        
    sess.run(init)
    total_batch = int(mnist.train.num_examples/batch_size)
    
# Training Cycle!!!!
# using for loop 
# also can use while cost<= something:

    for epoch in range(training_epochs):
        # loop over all batches
        for i in range(total_batch):
            
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            
            _,c = sess.run([optimizer,cost],feed_dict = {X: batch_xs})
        if epoch % display_step == 0:
            print 'Epoch:','%04d'%(epoch +1),'cost=','{:.9f}'.format(c)
            
    print "Optimization Finished!"
    
    # run model on the test set!!!!!!
    # y_pred is the model and feed_dict is the 
    # examples_to_show = 10
    # sess.run return a list of result images
    
    encode_decode = sess.run(
            y_pred, feed_dict = {X: mnist.test.images[:examples_to_show]}
            )
    
    #plt result
    
    f, a = plt.subplots(2,examples_to_show,figsize = (examples_to_show,2))
    for i in range(examples_to_show):
        a[0][i].imshow(np.reshape(mnist.test.images[i], (28,28)))
        a[1][i].imshow(np.reshape(encode_decode[i],(28,28)))
    plt.show()
    

