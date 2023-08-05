# -*- coding: utf-8 -*-

import keras

import keras.backend as K

from keras.constraints import max_norm

from keras.layers import Add
from keras.layers import Concatenate
from keras.layers import Conv1D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Embedding
from keras.layers import GlobalMaxPooling1D
from keras.layers import Input

# This code only works when using the TensorFlow backend
if K.backend() == 'tensorflow':
    from tensorflow.saved_model import signature_constants
    from tensorflow.saved_model import signature_def_utils
    from tensorflow.saved_model import tag_constants
    from tensorflow.saved_model.builder import SavedModelBuilder

class Model(keras.models.Model):
    '''Convolutional Model for Sentence Classification.

    This model uses a convolutional model to extract the most relevant
    features from the input sentences it is feeded with. This model
    suits well for classifying sentences that can be represented with a
    non-trivial set of keywords.

    The model must be parametrized using the `channels` and the
    `windows` that fit the problem to solve. The `channels` are just the
    specification of each of the word embeddings used by the model while
    the windows are the specification of each of the convolutional
    layers used to extract the most relevant features from the input
    sentences.

    NOTE: When using *TensorFlow* as backend for *Keras*, the model can
          be exported to the `protobuf` format. See the export-related
          method of this class and the documentation at
          https://www.tensorflow.org/serving/ to get more information.

    Reference
    ---------
    This class implements the model proposed in::

        Kim, Y. (2014). Convolutional neural networks for sentence
        classification. arXiv preprint arXiv:1408.5882.
    '''

    def __init__(self,
                 channels,
                 windows,
                 sentence_length,
                 num_classes=1,
                 dropout_rate=0.5,
                 maxnorm_value=3,
                 classifier_activation='sigmoid',
                 include_top=True,
                 **kwargs):
        '''Initializes the model

        Parameters
        ----------
        channels
            A list that contains the specification of each channel. See
            class documentation for more information.
        windows
            A list that contains the specification of each window. See
            class documentation for more information.
        sentence_length : int
            The length of each input sentence.
        num_classes : int, optional
            The number of classes the model classifies the output in.
        dropout_rate : float, optional
            The keep rate of the dropout normalization layer.
        maxnorm_value : float, optional
            The value of the l2 constraint applied to the last dense
            classification layer.
        classifier_activation : str, optional
            The type of activation of the classifier output. Use
            'softmax' for multi-class classification or 'sigmoid' for
            binary or multi-label classification.
        include_top : bool, optional
            Includes (or not) the classification layers as part of the
            model to be created.
        **kwargs
            Optional keywords arguments to be provided for the
            initialization method of the Keras `Model` class. See Keras
            documentation to get more information.
        '''
        x = Input(shape=(sentence_length,), dtype='int32')

        embeddings = self._embeddings(x, channels)
        features = self._features(embeddings, windows)

        if not include_top:
            y = features
        else:
            y = Dropout(rate=dropout_rate)(features)
            y = Dense(units=num_classes,
                      activation=classifier_activation,
                      kernel_constraint=max_norm(maxnorm_value))(y)

        super(Model, self).__init__(inputs=x, outputs=y, **kwargs)

    def _embeddings(self, inputs, channels):
        return [Embedding(**channel)(inputs) for channel in channels]

    def _features(self, embeddings, windows):
        features = []
        for window in windows:
            conv = Conv1D(**window)

            results = [conv(embedding) for embedding in embeddings]
            feature = self._add(results)
            feature = GlobalMaxPooling1D()(feature)

            features.append(feature)

        return self._concatenate(features)

    def _add(self, tensors):
        if len(tensors) == 1:
            return tensors[0]
        else:
            return Add()(tensors)

    def _concatenate(self, tensors, **kwargs):
        if len(tensors) == 1:
            return tensors[0]
        else:
            return Concatenate(**kwargs)(tensors)

    # This code only works when using the TensorFlow backend
    if K.backend() == 'tensorflow':

        def export(self, path, **kwargs):
            '''Exports the model for *TensorFlow serving*

            Parameters
            ----------
            path: the path to the directory to be used to stored the
                  files of the exported model. The path should point to
                  a directory that **must not** exist.
            **kwargs: Named parameters to be provided to the underliying
                      `save` method of the builder used during export.
                      See the documentation in https://www.tensorflow.org/api_docs/python/tf/saved_model/builder/SavedModelBuilder#save

            NOTE: This feature only makes sense if using the
                  *TensorFlow* backend. See https://keras.io/backend/
                  for more information.
            '''
            builder = SavedModelBuilder(path)
            builder.add_meta_graph_and_variables(
                sess=K.get_session(),
                tags=[tag_constants.SERVING],
                signature_def_map=self.signature_mapping())
            builder.save(**kwargs)

        def signature_mapping(self):
            '''Returns the signature mapping to be used with this model

            Return Value
            ------------
            The mapping used by this model when exporting to *Protobuf*.
            See https://www.tensorflow.org/serving/signature_defs for
            more information.

            NOTE: This feature only makes sense if using the
                  *TensorFlow* backend. See https://keras.io/backend/
                  for more information.
            '''
            return {
                signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY:
                    self._prediction_signature()
            }

        def _prediction_signature(self):
            return signature_def_utils.predict_signature_def(
                inputs={"inputs": self.input},
                outputs={"outputs": self.output})

if __name__ == '__main__':
    pass
