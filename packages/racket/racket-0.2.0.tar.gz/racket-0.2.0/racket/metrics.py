from importlib import import_module

import tensorflow as tf
import tensorflow.keras.backend as K


__metrics__ = {

    'tf': [
        'accuracy',
        'auc',
        'average_precision_at_k',
        'false_negatives',
        'false_negatives_at_thresholds',
        'false_positives',
        'false_positives_at_thresholds',
        'mean',
        'mean_absolute_error',
        'mean_cosine_distance',
        'mean_iou',
        'mean_per_class_accuracy',
        'mean_relative_error',
        'mean_squared_error',
        'mean_tensor',
        'percentage_below',
        'precision',
        'precision_at_k',
        'precision_at_thresholds',
        'precision_at_top_k',
        'recall',
        'recall_at_k',
        'recall_at_thresholds',
        'recall_at_top_k',
        'root_mean_squared_error',
        'sensitivity_at_specificity',
        'sparse_average_precision_at_k',
        'sparse_precision_at_k',
        'specificity_at_sensitivity',
        'true_negatives',
        'true_negatives_at_thresholds',
        'true_positives',
        'true_positives_at_thresholds',
    ],
    'keras': [
        'binary_accuracy',
        'categorical_accuracy',
        'deserialize',
        'get',
        'serialize',
        'sparse_top_k_categorical_accuracy',
        'top_k_categorical_accuracy'
    ]
}

# def auc(y_true, y_pred):
#     auc_score = tf.metrics.auc(y_true, y_pred)[1]
#     K.get_session().run(tf.local_variables_initializer())
#     return auc_score


class Metric:

    __all__ = __metrics__['tf'] + __metrics__['keras']

    def __init__(self, name):
        if name not in self.__all__:
            raise ValueError('Invalid metric')
        self.name = name
        if self.name in __metrics__['tf']:
            metrics = import_module('tensorflow.metrics')
        else:
            metrics = import_module('tensorflow.keras.metrics')
        self.metric = getattr(metrics, self.name)

    def __call__(self, y_true, y_pred):
        score = self.metric(y_true, y_pred)[1]
        K.get_session().run(tf.local_variables_initializer())
        return K.eval(score)

