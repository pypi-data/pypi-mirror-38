from __future__ import absolute_import  # 加入绝对引入这个新特性,便于导入系统中函数(和自己写的文件名一样的函数)
from __future__ import division  # 精确除法　导入精确除法后，若要执行截断除法，可以使用"//"操作符：3/4=0.75  3//4=0
from __future__ import print_function  # 使用新版本的print

from novamind.ops.tf_ops import batch_norm, create_variables, ave_pool
import tensorflow as tf


def Basic_Residual_block(in_img, filters, down_sample, is_training=True, weight_decay=0.0001, projection=False, model='train'):
    input_depth = int(in_img.get_shape()[3])
    if down_sample:
        stride = 2
    else:
        stride = 1

    with tf.variable_scope('conv1'):
        weight_1 = create_variables(name='weight_1', shape=[3, 3, input_depth, filters], weight_decay=weight_decay)
        biases_1 = create_variables(name='biases_1', shape=[filters], weight_decay=weight_decay, initializer=tf.zeros_initializer())
        conv1_ReLu = tf.nn.relu(tf.nn.conv2d(in_img, weight_1, strides=[1, stride, stride, 1], padding='SAME') + biases_1)

    with tf.variable_scope('conv2'):
        weight_2 = create_variables(name='weight_2', shape=[3, 3, filters, filters], weight_decay=weight_decay)
        biases_2 = create_variables(name='biases_2', shape=[filters], weight_decay=weight_decay, initializer=tf.zeros_initializer())
        conv2_ReLu = tf.nn.conv2d(conv1_ReLu, weight_2, strides=[1, 1, 1, 1], padding='SAME') + biases_2
        conv2_ReLu = batch_norm(conv2_ReLu, 'bn', is_training)

    if input_depth != filters:
        if projection:   # Not very good
            # Option B: Projection shortcut
            weight_3 = create_variables(name='weight_3', shape=[1, 1, input_depth, filters], weight_decay=weight_decay)
            biases_3 = create_variables(name='biases_3', shape=[filters], weight_decay=weight_decay, initializer=tf.zeros_initializer())
            input_layer =  tf.nn.conv2d(in_img, weight_3, strides=[1, 1, 1, 1], padding='SAME') + biases_3
        else:
            # Option A: Zero-padding
            if down_sample:
                in_img = ave_pool(in_img)
            input_layer = tf.pad(in_img, [[0, 0], [0, 0], [0, 0], [int((filters - input_depth)/2), filters - input_depth - int((filters - input_depth)/2)]])  # 维度是4维[batch_size, :, :, dim] 我么要pad dim的维度
    else:
        input_layer = in_img

    output = conv2_ReLu + input_layer
    # output = tf.nn.relu(output)
    return output


"""
  resnet-cifar10
  in: [32, 32, 3]
  conv: [32， 32， 16]
  conv1 :[32, 32, 16*k]
  conv2: [16, 16, 32*k]
  conv3: [8, 8, 64*k]
  ave-pool : [8*8] pooling----[1*1]
  fc: [64*k, 10]
"""

class resnetcifar(object):  # Inference
    def __init__(self, layers_depth=32, depth_filter=1, weight_decay=0.0001):
        '''
        :layers_depth : how many layers of cnn model. default is 32.
               you can change:20, 44, 56, 110.
        :depth_filter : multi filter. default is 1.
        '''
        self.img = None
        self.reuse = False
        self.weight_decay = weight_decay
        self.k = depth_filter    # Original architecture
        self.filter = [16, 16*self.k, 32*self.k, 64*self.k]
        (self.stack_layers, rem) = divmod(layers_depth - 2, 6)
        assert rem == 0, 'depth must be 6n + 2, 余数为0'
        self.block = Basic_Residual_block

    def __call__(self, img, is_training):
        self.img = img
        with tf.variable_scope("resnetcifar", reuse=self.reuse) as scope_name:
            if self.reuse:
                scope_name.reuse_variables()
            # conv1
            with tf.variable_scope('conv_pre'):   # 32
                weight_1 = create_variables(name='weight', shape=[3, 3, 3, self.filter[0]], weight_decay=self.weight_decay)
                biases_1 = create_variables(name='biases', shape=[self.filter[0]], weight_decay=self.weight_decay, initializer=tf.zeros_initializer())
                conv1_conv = tf.nn.conv2d(self.img, weight_1, strides=[1, 1, 1, 1], padding='SAME') + biases_1
                conv1_BN = batch_norm(conv1_conv, 'bn', is_training)
                conv1 = tf.nn.relu(conv1_BN)
            # conv2
            in_img = conv1
            for ii in range(1, 4):
                with tf.variable_scope('conv' + str(ii)):   # 64
                    for kk in range(self.stack_layers):
                        down_sample = True if kk == 0 and ii != 1 else False
                        with tf.variable_scope('con_' + str(kk)):
                            in_img = self.block(in_img, filters=self.filter[ii], down_sample=down_sample, is_training=is_training, weight_decay=self.weight_decay)
            in_img = tf.nn.relu(in_img)
            with tf.variable_scope('fc'):
                fc_layer = batch_norm(in_img, 'bn', is_training)
                global_pool = tf.reduce_mean(fc_layer, [1, 2])
        self.reuse = True
        return global_pool

# max: 0.930
