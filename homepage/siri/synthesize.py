# -*- coding: utf-8 -*-
# /usr/bin/python2
'''
By kyubyong park. kbpark.linguist@gmail.com.
https://www.github.com/kyubyong/dc_tts
'''

from __future__ import print_function

import os
import subprocess

from siri.hyperparams import Hyperparams as hp
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from siri.train import Graph
from siri.utils import *
from siri.data_load import load_data
from scipy.io.wavfile import write
from tqdm import tqdm

# Feed Forward
def feed_forward(text, target_dir):
    tf.reset_default_graph()

    with tf.Session() as sess:
        g = Graph(mode="synthesize")

        sess.run(tf.global_variables_initializer())

        # Restore parameters
        var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'Text2Mel')
        saver1 = tf.train.Saver(var_list=var_list)
        saver1.restore(sess, tf.train.latest_checkpoint(hp.logdir + "-1"))

        var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'SSRN') + \
                   tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, 'gs')
        saver2 = tf.train.Saver(var_list=var_list)
        saver2.restore(sess, tf.train.latest_checkpoint(hp.logdir + "-2"))

        L = load_data(text)
        Y = np.zeros((len(L), hp.max_T, hp.n_mels), np.float32)
        prev_max_attentions = np.zeros((len(L),), np.int32)
        for j in tqdm(range(hp.max_T)):
            _gs, _Y, _max_attentions, _alignments = \
                sess.run([g.global_step, g.Y, g.max_attentions, g.alignments],
                         {g.L: L,
                          g.mels: Y,
                          g.prev_max_attentions: prev_max_attentions})
            Y[:, j, :] = _Y[:, j, :]
            prev_max_attentions = _max_attentions[:, j]
        # Get magnitude
        Z = sess.run(g.Z, {g.Y: Y})

        wavs = []
        for i, mag in enumerate(Z):
            print("Working on file", i+1)
            wav = spectrogram2wav(mag)
            wavs.append(wav)
        output = np.concatenate(wavs, axis=0)
        write(target_dir + "/output.wav", hp.sr, output)

        # Generate mp3 file with lame
        proc = subprocess.Popen(["lame", "--preset", "insane", target_dir + "/output.wav"])
        proc.communicate()

        return target_dir + "/output.mp3"
