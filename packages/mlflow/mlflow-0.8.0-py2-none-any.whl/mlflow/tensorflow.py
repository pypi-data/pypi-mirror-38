"""
The ``mlflow.tensorflow`` module provides an API for logging and loading TensorFlow models
as :py:mod:`mlflow.pyfunc` models.

You must save your own ``saved_model`` and pass its
path to ``log_saved_model(saved_model_dir)``. To load the model to predict on it, you call
``model = pyfunc.load_pyfunc(saved_model_dir)`` followed by
``prediction = model.predict(pandas DataFrame)`` to obtain a prediction in a pandas DataFrame.

The loaded :py:mod:`mlflow.pyfunc` model *does not* expose any APIs for model training.
"""

from __future__ import absolute_import

import os
import shutil

import pandas
import tensorflow as tf

import mlflow
from mlflow import pyfunc
from mlflow.exceptions import MlflowException
from mlflow.models import Model
from mlflow.protos.databricks_pb2 import DIRECTORY_NOT_EMPTY
from mlflow.tracking.utils import _get_model_log_dir
from mlflow.utils.file_utils import _copy_file_or_tree
from mlflow.utils.logging_utils import eprint

FLAVOR_NAME = "tensorflow"


def log_model(tf_saved_model_dir, tf_meta_graph_tags, tf_signature_def_key, artifact_path,
              conda_env=None):
    """
    Log a *serialized* collection of Tensorflow graphs and variables as an MLflow model
    for the current run. This method operates on Tensorflow variables and graphs that have been
    serialized in Tensorflow's `SavedModel` format. For more information about the `SavedModel`,
    see the following Tensorflow documentation: https://www.tensorflow.org/guide/saved_model#
    save_and_restore_models.

    :param tf_saved_model_dir: Path to the directory containing serialized Tensorflow variables and
                               graphs in `SavedModel` format.
    :param tf_meta_graph_tags: A list of tags identifying the model's metagraph within the
                               serialized `SavedModel` object. For more information, see the `tags`
                               parameter of the `tf.saved_model.builder.SavedModelBuilder` method:
                               https://www.tensorflow.org/api_docs/python/tf/saved_model/builder/
                               SavedModelBuilder#add_meta_graph
    :param tf_signature_def_key: A string identifying the input/output signature associated with the
                                 model. This is a key within the serialized `SavedModel`'s signature
                                 definition mapping. For more information, see the
                                 `signature_def_map` parameter of the
                                 `tf.saved_model.builder.SavedModelBuilder` method.
    :param artifact_path: The run-relative path to which to log model artifacts.
    :param conda_env: Path to a Conda environment file. If provided, defines an environment for the
                      model. At minimum, it should specify python, tensorflow, and mlflow with
                      appropriate versions.
    """
    return Model.log(artifact_path=artifact_path, flavor=mlflow.tensorflow,
                     tf_saved_model_dir=tf_saved_model_dir, tf_meta_graph_tags=tf_meta_graph_tags,
                     tf_signature_def_key=tf_signature_def_key, conda_env=conda_env)


def save_model(tf_saved_model_dir, tf_meta_graph_tags, tf_signature_def_key, path,
               mlflow_model=Model(), conda_env=None):
    """
    Save a *serialized* collection of Tensorflow graphs and variables as an MLflow model
    to a local path. This method operates on Tensorflow variables and graphs that have been
    serialized in Tensorflow's `SavedModel` format. For more information about the `SavedModel`,
    see the following Tensorflow documentation: https://www.tensorflow.org/guide/saved_model#
    save_and_restore_models.

    :param tf_saved_model_dir: Path to the directory containing serialized Tensorflow variables and
                               graphs in `SavedModel` format.
    :param tf_meta_graph_tags: A list of tags identifying the model's metagraph within the
                               serialized `savedmodel` object. for more information, see the `tags`
                               parameter of the `tf.saved_model.builder.savedmodelbuilder` method:
                               https://www.tensorflow.org/api_docs/python/tf/saved_model/builder/
                               savedmodelbuilder#add_meta_graph
    :param tf_signature_def_key: A string identifying the input/output signature associated with the
                                 model. this is a key within the serialized `savedmodel`'s signature
                                 definition mapping. for more information, see the
                                 `signature_def_map` parameter of the
                                 `tf.saved_model.builder.savedmodelbuilder` method.
    :param path: Local path where the MLflow model is to be saved.
    :param mlflow_model: MLflow model configuration to which this flavor will be added.
    :param conda_env: Path to a Conda environment file. If provided, defines an environment for the
                      model. At minimum, it should specify python, tensorflow, and mlflow with
                      appropriate versions.
    """
    eprint("Validating the specified Tensorflow model by attempting to load it in a new Tensorflow"
           " graph...")
    _validate_saved_model(tf_saved_model_dir=tf_saved_model_dir,
                          tf_meta_graph_tags=tf_meta_graph_tags,
                          tf_signature_def_key=tf_signature_def_key)
    eprint("Validation succeeded!")

    if os.path.exists(path):
        raise MlflowException("Path '{}' already exists".format(path), DIRECTORY_NOT_EMPTY)
    os.makedirs(path)
    root_relative_path = _copy_file_or_tree(src=tf_saved_model_dir, dst=path, dst_dir=None)
    model_dir_subpath = "tfmodel"
    shutil.move(os.path.join(path, root_relative_path), os.path.join(path, model_dir_subpath))

    mlflow_model.add_flavor(FLAVOR_NAME, saved_model_dir=model_dir_subpath,
                            meta_graph_tags=tf_meta_graph_tags,
                            signature_def_key=tf_signature_def_key)

    model_conda_env = None
    if conda_env:
        model_conda_env = os.path.basename(os.path.abspath(conda_env))
        _copy_file_or_tree(src=conda_env, dst=path)

    pyfunc.add_to_model(mlflow_model, loader_module="mlflow.tensorflow", env=model_conda_env)
    mlflow_model.save(os.path.join(path, "MLmodel"))


def _validate_saved_model(tf_saved_model_dir, tf_meta_graph_tags, tf_signature_def_key):
    """
    Validate the Tensorflow SavedModel by attempting to load it in a new Tensorflow graph.
    If the loading process fails, any exceptions thrown by Tensorflow will be propagated.
    """
    validation_tf_graph = tf.Graph()
    validation_tf_sess = tf.Session(graph=validation_tf_graph)
    with validation_tf_graph.as_default():
        _load_model(tf_saved_model_dir=tf_saved_model_dir,
                    tf_sess=validation_tf_sess,
                    tf_meta_graph_tags=tf_meta_graph_tags,
                    tf_signature_def_key=tf_signature_def_key)


def load_model(path, tf_sess, run_id=None):
    """
    Load an MLflow model that contains the Tensorflow flavor from the specified path.

    **This method must be called within a Tensorflow graph context!**

    :param path: The local filesystem path or run-relative artifact path to the model.
    :param tf_sess: The Tensorflow session in which to the load the model.
    :return: A Tensorflow signature definition of type:
             `tensorflow.core.protobuf.meta_graph_pb2.SignatureDef`. This defines the input and
             output tensors for model inference.

    >>> import mlflow.tensorflow
    >>> import tensorflow as tf
    >>> tf_graph = tf.Graph()
    >>> tf_sess = tf.Session(graph=tf_graph)
    >>> with tf_graph.as_default():
    >>>     signature_definition = mlflow.tensorflow.load_model(path="model_path", tf_sess=tf_sess)
    >>>     input_tensors = [tf_graph.get_tensor_by_name(input_signature.name)
    >>>                      for _, input_signature in signature_def.inputs.items()]
    >>>     output_tensors = [tf_graph.get_tensor_by_name(output_signature.name)
    >>>                       for _, output_signature in signature_def.outputs.items()]
    """
    if run_id is not None:
        path = _get_model_log_dir(model_name=path, run_id=run_id)
    m = Model.load(os.path.join(path, 'MLmodel'))
    if FLAVOR_NAME not in m.flavors:
        raise Exception("Model does not have {} flavor".format(FLAVOR_NAME))
    conf = m.flavors[FLAVOR_NAME]
    saved_model_dir = os.path.join(path, conf['saved_model_dir'])
    return _load_model(tf_saved_model_dir=saved_model_dir, tf_sess=tf_sess,
                       tf_meta_graph_tags=conf['meta_graph_tags'],
                       tf_signature_def_key=conf['signature_def_key'])


def _load_model(tf_saved_model_dir, tf_sess, tf_meta_graph_tags, tf_signature_def_key):
    """
    Load a specified Tensorflow model consisting of a Tensorflow meta graph and signature definition
    from a serialized Tensorflow `SavedModel` collection.

    :param tf_saved_model_dir: The local filesystem path or run-relative artifact path to the model.
    :param tf_sess: The Tensorflow session in which to the load the metagraph.
    :param tf_meta_graph_tags: A list of tags identifying the model's metagraph within the
                               serialized `SavedModel` object. For more information, see the `tags`
                               parameter of the `tf.saved_model.builder.SavedModelBuilder` method:
                               https://www.tensorflow.org/api_docs/python/tf/saved_model/builder/
                               SavedModelBuilder#add_meta_graph
    :param tf_signature_def_key: A string identifying the input/output signature associated with the
                                 model. This is a key within the serialized `SavedModel`'s signature
                                 definition mapping. For more information, see the
                                 `signature_def_map` parameter of the
                                 `tf.saved_model.builder.SavedModelBuilder` method.
    :return: A Tensorflow signature definition of type:
             `tensorflow.core.protobuf.meta_graph_pb2.SignatureDef`. This defines input and
             output tensors within the specified metagraph for inference.
    """
    meta_graph_def = tf.saved_model.loader.load(
            sess=tf_sess,
            tags=tf_meta_graph_tags,
            export_dir=tf_saved_model_dir)
    if tf_signature_def_key not in meta_graph_def.signature_def:
        raise MlflowException("Could not find signature def key %s" % tf_signature_def_key)
    return meta_graph_def.signature_def[tf_signature_def_key]


def _load_pyfunc(path):
    """
    Load PyFunc implementation. Called by ``pyfunc.load_pyfunc``. This function loads an MLflow
    model with the Tensorflow flavor into a new Tensorflow graph and exposes it behind the
    `pyfunc.predict` interface.
    """
    tf_graph = tf.Graph()
    tf_sess = tf.Session(graph=tf_graph)
    with tf_graph.as_default():
        signature_def = load_model(path=path, tf_sess=tf_sess, run_id=None)

    return _TFWrapper(tf_sess=tf_sess, tf_graph=tf_graph, signature_def=signature_def)


class _TFWrapper(object):
    """
    Wrapper class that exposes a Tensorflow model for inference via a `predict` function such that
    predict(data: pandas.DataFrame) -> pandas.DataFrame.
    """
    def __init__(self, tf_sess, tf_graph, signature_def):
        """
        :param tf_sess: The Tensorflow session used to evaluate the model.
        :param tf_graph: The Tensorflow graph containing the model.
        :param signature_def: The Tensorflow signature definition used to transform input dataframes
                              into tensors and output vectors into dataframes.
        """
        self.tf_sess = tf_sess
        self.tf_graph = tf_graph
        # We assume that input keys in the signature definition correspond to input DataFrame column
        # names
        self.input_tensor_mapping = {
                tensor_column_name: tf_graph.get_tensor_by_name(tensor_info.name)
                for tensor_column_name, tensor_info in signature_def.inputs.items()
        }
        # We assume that output keys in the signature definition correspond to output DataFrame
        # column names
        self.output_tensors = {
                sigdef_output: tf_graph.get_tensor_by_name(tnsr_info.name)
                for sigdef_output, tnsr_info in signature_def.outputs.items()
        }

    def predict(self, df):
        with self.tf_graph.as_default():
            # Build the feed dict, mapping input tensors to DataFrame column values.
            feed_dict = {
                    self.input_tensor_mapping[tensor_column_name]: df[tensor_column_name].values
                    for tensor_column_name in self.input_tensor_mapping.keys()
            }
            raw_preds = self.tf_sess.run(self.output_tensors, feed_dict=feed_dict)
            pred_dict = {column_name: values.ravel() for column_name, values in raw_preds.items()}
            return pandas.DataFrame(data=pred_dict)
