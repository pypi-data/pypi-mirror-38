# -*- coding: utf-8 -*-

import keras

import keras.backend as K

from keras.layers import Add
from keras.layers import Concatenate
from keras.layers import Conv1D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Embedding
from keras.layers import GlobalMaxPooling1D
from keras.layers import Input
from keras.layers import LSTM

# This code only works when using the TensorFlow backend
if K.backend() == 'tensorflow':
    from tensorflow.saved_model import signature_constants
    from tensorflow.saved_model import signature_def_utils
    from tensorflow.saved_model import tag_constants
    from tensorflow.saved_model.builder import SavedModelBuilder

class Model(keras.models.Model):

    def __init__(self,
                 channels,
                 windows,
                 sentence_length,
                 num_classes=1,
                 dropout_rate=0.5,
                 classifier_activation='sigmoid',
                 include_top=True,
                 **kwargs):

        x = Input(shape=(sentence_length,), dtype='int32')

        embeddings = self._embeddings(x, channels)
        sequences = self._sequences(embeddings)
        features = self._features(sequences, windows)

        if not include_top:
            y = features
        else:
            y = Dropout(rate=dropout_rate)(features)
            y = Dense(units=num_classes,
                      activation=classifier_activation)(y)

        super(Model, self).__init__(inputs=x, outputs=y, **kwargs)

    def _embeddings(self, inputs, channels):
        return [Embedding(**channel)(inputs) for channel in channels]

    def _sequences(self, embeddings):
        sequence = lambda embedding: self._sequence(embedding)
        return [sequence(embedding) for embedding in embeddings]

    def _sequence(self, embedding):
        input_shape = K.int_shape(embedding)
        embedding_size = input_shape[2]

        return LSTM(units=embedding_size,
                    return_sequences=True)(embedding)

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

    def _concatenate(self, tensors):
        if len(tensors) == 1:
            return tensors[0]
        else:
            return Concatenate()(tensors)

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
