
Keras Position-Wise Feed Forward
================================


.. image:: https://travis-ci.org/CyberZHG/keras-position-wise-feed-forward.svg
   :target: https://travis-ci.org/CyberZHG/keras-position-wise-feed-forward
   :alt: Travis


.. image:: https://coveralls.io/repos/github/CyberZHG/keras-position-wise-feed-forward/badge.svg?branch=master
   :target: https://coveralls.io/github/CyberZHG/keras-position-wise-feed-forward
   :alt: Coverage


Implementation of position-wise feed forward layer in the paper: `Attention is All You Need <https://arxiv.org/pdf/1706.03762.pdf>`_

Install
-------

.. code-block:: bash

   pip install keras-position-wise-feed-forward

Usage
-----

.. code-block:: python

   import keras
   from keras_position_wise_feed_forward import FeedForward

   input_layer = keras.layers.Input()
   feed_forward_layer = FeedForward()(input_layer)
   model = keras.models.Model(inputs=input_layer, outputs=feed_forward_layer)
   model.compile(optimizer='adam', loss='mse', metrics={})
   model.summary()
