import unittest
import os
import tempfile
import random
import keras
import numpy as np
import tensorflow as tf
from keras_pos_embd import TrigPosEmbedding


class TestSinCosPosEmbd(unittest.TestCase):

    def test_invalid_output_dim(self):
        with self.assertRaises(NotImplementedError):
            TrigPosEmbedding(
                mode=TrigPosEmbedding.MODE_EXPAND,
                output_dim=5,
            )

    def test_missing_output_dim(self):
        with self.assertRaises(NotImplementedError):
            TrigPosEmbedding(
                mode=TrigPosEmbedding.MODE_EXPAND,
            )

    def test_brute(self):
        seq_len = random.randint(1, 10)
        embd_dim = random.randint(1, 20) * 2
        indices = np.expand_dims(np.arange(seq_len), 0)
        model = keras.models.Sequential()
        model.add(TrigPosEmbedding(
            input_shape=(seq_len,),
            mode=TrigPosEmbedding.MODE_EXPAND,
            output_dim=embd_dim,
            name='Pos-Embd',
        ))
        model.compile('adam', keras.losses.mae, {})
        model_path = os.path.join(tempfile.gettempdir(), 'test_trig_pos_embd_%f.h5' % random.random())
        model.save(model_path)
        model = keras.models.load_model(model_path, custom_objects={'TrigPosEmbedding': TrigPosEmbedding})
        model.summary()
        predicts = model.predict(indices)[0].tolist()
        sess = tf.Session()
        for i in range(seq_len):
            for j in range(embd_dim):
                actual = predicts[i][j]
                if j % 2 == 0:
                    expect = tf.sin(i / tf.pow(10000.0, j / embd_dim))
                else:
                    expect = tf.cos(i / tf.pow(10000.0, (j - 1) / embd_dim))
                expect = expect.eval(session=sess)
                self.assertAlmostEqual(expect, actual, places=6, msg=(embd_dim, i, j, expect, actual))

    def test_add(self):
        seq_len = random.randint(1, 10)
        embd_dim = random.randint(1, 20) * 2
        inputs = np.ones((1, seq_len, embd_dim))
        model = keras.models.Sequential()
        model.add(TrigPosEmbedding(
            input_shape=(seq_len, embd_dim),
            mode=TrigPosEmbedding.MODE_ADD,
            name='Pos-Embd',
        ))
        model.compile('adam', keras.losses.mae, {})
        model_path = os.path.join(tempfile.gettempdir(), 'test_trig_pos_embd_%f.h5' % random.random())
        model.save(model_path)
        model = keras.models.load_model(model_path, custom_objects={'TrigPosEmbedding': TrigPosEmbedding})
        model.summary()
        predicts = model.predict(inputs)[0].tolist()
        sess = tf.Session()
        for i in range(seq_len):
            for j in range(embd_dim):
                actual = predicts[i][j]
                if j % 2 == 0:
                    expect = 1.0 + tf.sin(i / tf.pow(10000.0, j / embd_dim))
                else:
                    expect = 1.0 + tf.cos(i / tf.pow(10000.0, (j - 1) / embd_dim))
                expect = expect.eval(session=sess)
                self.assertAlmostEqual(expect, actual, places=6, msg=(embd_dim, i, j, expect, actual))
