# -*- coding: utf-8 -*-
#/usr/bin/python2
'''
By kyubyong park. kbpark.linguist@gmail.com.
https://www.github.com/kyubyong/dc_tts
'''

from __future__ import print_function
from nltk import tokenize

import textwrap

from siri.hyperparams import Hyperparams as hp
import numpy as np
import tensorflow as tf
from siri.utils import *
import codecs
import re
import os
import unicodedata
import num2words

def load_vocab():
    char2idx = {char: idx for idx, char in enumerate(hp.vocab)}
    idx2char = {idx: char for idx, char in enumerate(hp.vocab)}
    return char2idx, idx2char

def text_normalize(text):
    text = ''.join(char for char in unicodedata.normalize('NFD', text)
                           if unicodedata.category(char) != 'Mn') # Strip accents

    text = text.lower()
    text = re.sub("[^{}]".format(hp.vocab), " ", text)
    text = re.sub("[ ]+", " ", text)
    return text

def load_data(text):
    '''Loads data
      Args:
          mode: "train" or "synthesize".
    '''
    # Load vocabulary
    text = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), text)
    char2idx, idx2char = load_vocab()

    lines = tokenize.sent_tokenize(text)
    lines_wrapped = []
    for line in lines:
        lines_wrapped += textwrap.wrap(line, hp.max_N - 5, break_long_words=False)
    lines_wrapped = ["{}. {}".format(i, line) for i, line in enumerate(lines_wrapped)]
    print(lines_wrapped)
    sents = [text_normalize(line.split(" ", 1)[-1]).strip() + "E" for line in lines_wrapped] # text normalization, E: EOS
    texts = np.zeros((len(sents), hp.max_N), np.int32)
    for i, sent in enumerate(sents):
        texts[i, :len(sent)] = [char2idx[char] for char in sent]
    return texts

def get_batch():
    """Loads training data and put them in queues"""
    with tf.device('/cpu:0'):
        # Load data
        fpaths, text_lengths, texts = load_data() # list
        maxlen, minlen = max(text_lengths), min(text_lengths)

        # Calc total batch count
        num_batch = len(fpaths) // hp.B

        # Create Queues
        fpath, text_length, text = tf.train.slice_input_producer([fpaths, text_lengths, texts], shuffle=True)

        # Parse
        text = tf.decode_raw(text, tf.int32)  # (None,)

        if hp.prepro:
            def _load_spectrograms(fpath):
                fname = os.path.basename(fpath)
                mel = "mels/{}".format(fname.decode("utf-8").replace("wav", "npy"))
                mag = "mags/{}".format(fname.decode("utf-8").replace("wav", "npy"))
                return fname, np.load(mel), np.load(mag)

            fname, mel, mag = tf.py_func(_load_spectrograms, [fpath], [tf.string, tf.float32, tf.float32])
        else:
            fname, mel, mag = tf.py_func(load_spectrograms, [fpath], [tf.string, tf.float32, tf.float32])  # (None, n_mels)

        # Add shape information
        fname.set_shape(())
        text.set_shape((None,))
        mel.set_shape((None, hp.n_mels))
        mag.set_shape((None, hp.n_fft//2+1))

        # Batching
        _, (texts, mels, mags, fnames) = tf.contrib.training.bucket_by_sequence_length(
                                            input_length=text_length,
                                            tensors=[text, mel, mag, fname],
                                            batch_size=hp.B,
                                            bucket_boundaries=[i for i in range(minlen + 1, maxlen - 1, 20)],
                                            num_threads=8,
                                            capacity=hp.B*4,
                                            dynamic_pad=True)

    return texts, mels, mags, fnames, num_batch
