#!/usr/bin/python
from . import ModelDbSyncer
from ..events import MetricEvent


# Computes various scores for models, such as precision, recall, and f1_score.


def compute_metrics(
        model, metric_func, actual, predicted, X, prediction_col, label_col,
        **params):
    score = metric_func(actual, predicted, **params)
    metric_event = MetricEvent(
        X, model, label_col, prediction_col, metric_func.__name__, score)
    ModelDbSyncer.Syncer.instance.add_to_buffer(metric_event)
    return score
