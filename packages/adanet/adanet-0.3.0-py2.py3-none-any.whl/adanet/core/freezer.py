"""An AdaNet ensemble freezer in Tensorflow.

Copyright 2018 The AdaNet Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from adanet.core.ensemble import WeightedSubnetwork
from adanet.core.subnetwork import Subnetwork
import tensorflow as tf

_COLOCATION_ATTR_KEY = u"_class"
_COLOCATION_ATTR_PREFIX = b"loc:@"


class _EnsembleFreezer(object):
  """Stateless object that saves, and loads a frozen AdaNet ensemble."""

  class Keys(object):
    """Collection keys for freezing ensemble fields.

    The following frozen keys are defined:

    * `BIAS`: Ensemble bias term `Tensor`.
    * `COMPLEXITY`: subnetwork complexity `Tensor`.
    * `LAST_LAYER`: subnetwork's last layer `Tensor`.
    * `LOGITS`: subnetwork's mixture-weighted logits `Tensor`.
    * `NAME`: subnetwork's name `Tensor`.
    * `PERSISTED_TENSORS`: subnetwork persisted `Tensors`.
    * `PERSISTED_TENSORS_SEPARATOR`: Separator symbol for persisted tensor keys.
    * `WEIGHT`: the mixture weight `Tensor` of each subnetwork.
    """

    BIAS = "bias"
    COMPLEXITY = "complexity"
    LAST_LAYER = "last_layer"
    LOGITS = "logits"
    NAME = "name"
    PERSISTED_TENSORS = "persisted_tensors"
    PERSISTED_TENSORS_SEPARATOR = "|"
    WEIGHT = "weight"

  def wrapped_features(self, features):
    """Wraps each feature `Tensor` in one with a similar name as its key.

    For `SparseTensor` features, it replaces the feature with a new
    `SparseTensor` composed of the original's wrapped indices, values, and
    dense_shape `Tensor`s.

    Args:
      features: Dictionary of wrapped `Tensor` objects keyed by feature name.

    Returns:
      A dictionary of wrapped feature `Tensor`s.
    """

    if features is None:
      return features

    result = {}
    for key, feature in features.items():
      if isinstance(feature, tf.SparseTensor):
        feature = tf.SparseTensor(
            indices=self._wrapped_tensor(
                feature.indices, name="{}_indices".format(key)),
            values=self._wrapped_tensor(
                feature.values, name="{}_values".format(key)),
            dense_shape=self._wrapped_tensor(
                feature.dense_shape, name="{}_dense_shape".format(key)))
      else:
        feature = self._wrapped_tensor(feature, key)
      result[key] = feature
    return result

  def _wrapped_tensor(self, tensor, name):
    """Doubly wraps the given tensor with the given name."""

    wrapped_name = self._wrapped_name(name)
    unwrapped_name = self._unwrapped_name(wrapped_name)
    tensor = tf.identity(tensor, name=unwrapped_name)
    return tf.identity(tensor, name=wrapped_name)

  def _wrapped_name(self, name):
    """Returns the wrapped name."""

    return "wrapped_{}".format(name)

  def _unwrapped_name(self, wrapped_name):
    """Returns the unwrapped name."""

    return "un" + wrapped_name

  def freeze_ensemble(self, filename, weighted_subnetworks, bias, features):
    """Freezes an ensemble of subnetworks' weights and persists its subgraph.

    Specifically, this method prunes all nodes from the current graph definition
    unrelated to the ensemble's `WeightedSubnetwork`s' subgraphs. A subgraph is
    defined as any ops that contribute to their outputs, complexity, and side
    inputs.

    These tensors-to-keep are added to named graph collections, so that the
    `WeightedSubnetworks` can be easily restored with only the information
    stored in the pruned graph and the checkpoint. This graph is serialized and
    written to disk as a `MetaGraphDef` proto.

    This method should only be called up to once per graph.

    Args:
      filename: String filename for the `MetaGraphDef` proto to be written.
      weighted_subnetworks: List of `WeightedSubnetwork` instances to freeze.
      bias: The ensemble's `Tensor` bias vector.
      features: Dictionary of wrapped `Tensor` objects keyed by feature name.
        Ops for unused features will not be pruned.

    Returns:
      A `MetaGraphDef` proto of the frozen ensemble.
    """

    names = [
        # item() is needed to convert from ndarray,
        # and decode() is needed to convert from b-string in python3.
        tf.contrib.util.constant_value(w.name).item().decode()
        for w in weighted_subnetworks
    ]
    # A destination node is a node in the output DAG that will have only
    # incoming edges. Marking these nodes to keep will cause all upstream nodes
    # that are connected by some path of directed edges to the destination node
    # to be marked to keep.
    destination_nodes = set()
    collection_set = {
        tf.GraphKeys.GLOBAL_VARIABLES, tf.GraphKeys.LOCAL_VARIABLES,
        tf.GraphKeys.TABLE_INITIALIZERS
    }

    variables_to_save = []
    for name in names:
      variables_to_save += tf.get_collection(
          tf.GraphKeys.GLOBAL_VARIABLES,
          scope=r"adanet/iteration_\d+/ensemble_{}/".format(name))
    variables_to_save += tf.get_collection(
        tf.GraphKeys.GLOBAL_VARIABLES, scope=r"adanet/iteration_\d+/step")
    variables = tf.get_collection_ref(tf.GraphKeys.GLOBAL_VARIABLES)
    del variables[:]
    for var in set(variables_to_save):
      tf.add_to_collection(tf.GraphKeys.GLOBAL_VARIABLES, var)
      destination_nodes.add(var.op.name)
      if var.op.type == "VarHandleOp":
        destination_nodes.add(var.op.name + "/Read/ReadVariableOp")
      else:
        destination_nodes.add(var.op.name + "/read")
      destination_nodes.add(var.initializer.name)
      destination_nodes.add(var.initial_value.op.name)

    for index, weighted_subnetwork in enumerate(weighted_subnetworks):
      self._freeze_weighted_subnetwork(
          weighted_subnetwork=weighted_subnetwork,
          index=index,
          collection_set=collection_set,
          destination_nodes=destination_nodes)

    self._freeze_bias(bias, collection_set, destination_nodes)

    # Save feature `Tensor`s so that they can be input-mapped upon loading in
    # case the ensemble doesn't yet use them in its sub-graph.
    for feature in features.values():
      if isinstance(feature, tf.SparseTensor):
        destination_nodes.add(feature.indices.op.name)
        destination_nodes.add(feature.values.op.name)
        destination_nodes.add(feature.dense_shape.op.name)
      else:
        destination_nodes.add(feature.op.name)

    # We need to add the variable initializers to the destination nodes, or they
    # will not be initializable upon loading.
    for local_var in tf.local_variables():
      destination_nodes.add(local_var.op.name)
      destination_nodes.add(local_var.op.name + "/read")
      destination_nodes.add(local_var.initializer.name)
      destination_nodes.add(local_var.initial_value.op.name)

    # We need to add the table initialization ops to the destination nodes, or
    # they will not be initializable upon loading.
    for table_init_op in tf.get_collection(tf.GraphKeys.TABLE_INITIALIZERS):
      destination_nodes.add(table_init_op.name)

    pruned_graph_def = prune_graph(
        input_graph_def=tf.get_default_graph().as_graph_def(),
        output_node_names=list(destination_nodes))
    return tf.train.export_meta_graph(
        filename=filename,
        graph_def=pruned_graph_def,
        collection_list=list(collection_set),
        clear_devices=True,
        clear_extraneous_savers=True,
        as_text=False)

  def _freeze_bias(self, bias, collection_set, destination_nodes):
    """Freezes the bias `Tensor`.

    Args:
      bias: The ensemble's `Tensor` bias vector.
      collection_set: Set of string names of collections to keep.
      destination_nodes: Set of string names of ops to keep.
    """

    self._clear_collection(self.Keys.BIAS)
    destination_nodes.add(bias.op.name)
    tf.add_to_collection(self.Keys.BIAS, bias)
    collection_set.add(self.Keys.BIAS)

  def _freeze_weighted_subnetwork(self, index, weighted_subnetwork,
                                  collection_set, destination_nodes):
    """Freezes a `WeightedSubnetwork`.

    Stores a `WeightedSubnetwork`'s ops in collections so that they can be
    easily restored into a `WeightedSubnetwork` instance.

    Args:
      index: Index of the `WeightedSubnetwork` in the `Ensemble`.
      weighted_subnetwork: The `WeightedSubnetwork` to freeze.
      collection_set: Set of string names of collections to keep.
      destination_nodes: Set of string names of ops to keep.
    """

    tensors_to_persist = {
        self.Keys.NAME: weighted_subnetwork.name,
        self.Keys.WEIGHT: weighted_subnetwork.weight,
        self.Keys.LOGITS: weighted_subnetwork.logits,
    }
    for field, tensor in tensors_to_persist.items():
      collection_key = self._weighted_subnetwork_collection_key(index, field)
      self._clear_collection(collection_key)
      self._keep_tensors(
          collection_set=collection_set,
          destination_nodes=destination_nodes,
          collection_key=collection_key,
          tensor=tensor)
    self._freeze_subnetwork(
        subnetwork=weighted_subnetwork.subnetwork,
        index=index,
        collection_set=collection_set,
        destination_nodes=destination_nodes)

  def _freeze_subnetwork(self, index, subnetwork, collection_set,
                         destination_nodes):
    """Freezes a `Subnetwork`.

    Stores a `Subnetwork`'s ops in collections so that they can be easily
    restored into a `Subnetwork` instance.

    Args:
      index: Index of the `Subnetwork` in the `Ensemble`.
      subnetwork: The `Subnetwork` to freeze.
      collection_set: Set of string names of collections to keep.
      destination_nodes: Set of string names of ops to keep.
    """

    tensors_to_persist = {
        self.Keys.COMPLEXITY: subnetwork.complexity,
        self.Keys.LAST_LAYER: subnetwork.last_layer,
        self.Keys.LOGITS: subnetwork.logits,
    }
    tensors_to_persist = self._persist_persisted_tensors(
        prefix=self.Keys.PERSISTED_TENSORS,
        persisted_tensors=subnetwork.persisted_tensors,
        tensors_to_persist=tensors_to_persist)

    for field, tensor in tensors_to_persist.items():
      collection_key = self._subnetwork_collection_key(index, field)
      self._clear_collection(collection_key)
      self._keep_tensors(
          collection_set=collection_set,
          destination_nodes=destination_nodes,
          collection_key=collection_key,
          tensor=tensor)

  def _clear_collection(self, collection_key):
    """Empties the collection with the given key."""

    collection = tf.get_collection_ref(collection_key)
    del collection[:]

  def _keep_tensors(self, collection_set, destination_nodes, collection_key,
                    tensor):
    """Marks a `Tensor` to be kept.

    This `Tensor` is added to the appropriate lists and collection so that it
    and its subgraph are not pruned before freezing.

    Args:
      collection_set: Set of string names of collections to keep.
      destination_nodes: Set of string names of ops to keep.
      collection_key: String key of the collection to add tensor.
      tensor: `Tensor` to keep. Its name is added to the destination_nodes list
        and it is added to the collection identified by collection_key.
    """

    if not isinstance(tensor, tf.Variable):
      tensor = tf.convert_to_tensor(tensor)
    destination_nodes.add(tensor.op.name)
    tf.add_to_collection(collection_key, tensor)
    collection_set.add(collection_key)

  def _persist_persisted_tensors(self, prefix, persisted_tensors,
                                 tensors_to_persist):
    """Flattens nested persisted_tensors entries into the tensors_to_persist.

    Recursively calls itself for each nested persisted tensor entry.

    Args:
      prefix: String prefix to prepend to each persisted tensor key.
      persisted_tensors: Dictionary of tensors to persist.
      tensors_to_persist: Flat dictionary of string key to `Tensor` that will be
        persisted.

    Returns:
      Dictionary copy of tensors_to_persist with persisted tensors included.

    Raises:
      ValueError: If persisted tensor keys include the persisted tensor
      separator symbol.
    """

    tensors_to_persist = tensors_to_persist.copy()
    for key, value in persisted_tensors.items():
      if self.Keys.PERSISTED_TENSORS_SEPARATOR in key:
        raise ValueError("Persisted tensor keys cannot contain '{}'.".format(
            self.Keys.PERSISTED_TENSORS_SEPARATOR))
      persisted_key = "{prefix}{separator}{key}".format(
          prefix=prefix,
          separator=self.Keys.PERSISTED_TENSORS_SEPARATOR,
          key=key)
      if isinstance(value, dict):
        tensors_to_persist = self._persist_persisted_tensors(
            persisted_key, value, tensors_to_persist)
        continue
      tensors_to_persist[persisted_key] = value
    return tensors_to_persist

  def load_frozen_ensemble(self, filename, features):
    """Loads ensemble `WeightedSubnetworks` and bias from a `MetaGraphDef`.

    This methods imports the graph of a frozen ensemble into the default graph
    and reconstructs it `WeightedSubnetworks` and bias. The frozen features
    are replaced with those given in the arguments.

    This method should only be called up to once per graph.

    Args:
      filename: String filename of the serialized `MetaGraphDef`.
      features: Dictionary of wrapped `Tensor` objects keyed by feature name.

    Returns:
      A three-tuple consisting of:
        - a list of frozen `WeightedSubnetworks` instances,
        - a bias term `Tensor`,
        - a `Saver` instance. This is used to restore the weights of the frozen
          ensemble from the checkpoint file.
    """

    # Wrapped features need to be unwrapped so that the inner `Tensor` can be
    # replaced with the new feature `Tensors`. Due to b/74595432, the wrapper
    # cannot be replaced itself.
    input_map = {}
    for feature in features.values():
      if isinstance(feature, tf.SparseTensor):
        input_map[self._unwrapped_name(feature.indices.name)] = feature.indices
        input_map[self._unwrapped_name(feature.values.name)] = feature.values
        input_map[self._unwrapped_name(
            feature.dense_shape.name)] = feature.dense_shape
      else:
        input_map[self._unwrapped_name(feature.name)] = feature

    # Import subnetwork's meta graph into default graph. Since there are no
    # variables to restore, import_meta_graph does not create a `Saver`.
    saver = tf.train.import_meta_graph(
        meta_graph_or_file=filename, input_map=input_map, clear_devices=True)

    weighted_subnetworks = []
    index = 0
    while True:
      weighted_subnetwork = self._reconstruct_weighted_subnetwork(index)
      if weighted_subnetwork is None:
        break
      weighted_subnetworks.append(weighted_subnetwork)
      index += 1

    bias_collection = tf.get_collection(self.Keys.BIAS)
    assert len(bias_collection) == 1
    bias_tensor = bias_collection[-1]
    return weighted_subnetworks, bias_tensor, saver

  def _reconstruct_weighted_subnetwork(self, index):
    """Reconstructs a `WeightedSubnetwork` from the graph's collections.

    Args:
      index: Integer index of the subnetwork in a list of subnetworks.

    Returns:
      A frozen `WeightedSubnetwork` instance or `None` if there is no
        `WeightedSubnetwork` frozen at index.
    """

    name = None
    weight = None
    logits = None
    for key in tf.get_default_graph().get_all_collection_keys():
      prefix = self._weighted_subnetwork_collection_key(index, "")
      if prefix not in key:
        continue

      # Verify that each frozen collection is of size one, as each collection
      # should have been cleared before adding a tensor to freeze.
      frozen_collection = tf.get_collection(key)
      assert len(frozen_collection) == 1
      frozen_tensor = frozen_collection[-1]

      field = self._weighted_subnetwork_collection_key_field(key, index)
      if field is None:
        continue
      if field == self.Keys.NAME:
        name = frozen_tensor
        continue
      if field == self.Keys.LOGITS:
        logits = frozen_tensor
        continue
      if field == self.Keys.WEIGHT:
        weight = frozen_tensor
        continue

    # No weighted subnetwork found at given index.
    if name is None and weight is None and logits is None:
      return None

    subnetwork = self._reconstruct_subnetwork(index)
    return WeightedSubnetwork(
        name=name, logits=logits, weight=weight, subnetwork=subnetwork)

  def _reconstruct_subnetwork(self, index):
    """Reconstructs a `Subnetwork` from the graph's collections.

    Args:
      index: Integer index of the subnetwork in a list of subnetworks.

    Returns:
      A frozen `Subnetwork` instance.

    Raises:
      ValueError: If a field in the frozen collection does not belong to a
        subnetwork. This should not happen if the collection was created by
        `freeze_ensemble`.
    """

    last_layer = None
    logits = None
    complexity = None
    persisted_tensors = {}
    for key in tf.get_default_graph().get_all_collection_keys():
      prefix = self._subnetwork_collection_key(index, "")
      if prefix not in key:
        continue

      # Verify that each frozen collection is of size one, as each collection
      # should have been cleared before adding a tensor to freeze.
      frozen_collection = tf.get_collection(key)
      assert len(frozen_collection) == 1
      frozen_tensor = frozen_collection[-1]

      field = self._subnetwork_collection_key_field(key, index)
      if field is None:
        continue
      if field == self.Keys.LAST_LAYER:
        last_layer = frozen_tensor
        continue
      if field == self.Keys.LOGITS:
        logits = frozen_tensor
        continue
      if field == self.Keys.COMPLEXITY:
        complexity = frozen_tensor
        continue
      if field.startswith(self.Keys.PERSISTED_TENSORS):
        # Remove persisted tensors prefix plus separator.
        prefix_length = len(self.Keys.PERSISTED_TENSORS)
        prefix_length += len(self.Keys.PERSISTED_TENSORS_SEPARATOR)
        field = field[prefix_length:]
        persisted_tensors = self._reconstruct_persisted_tensor(
            field, frozen_tensor, persisted_tensors)
        continue

      # This line should not be hit if the frozen graph was created with
      # freeze_ensemble.
      raise ValueError("'{}' in not a valid field.".format(field))

    return Subnetwork(
        last_layer=last_layer,
        logits=logits,
        complexity=complexity,
        persisted_tensors=persisted_tensors)

  def _reconstruct_persisted_tensor(self, field, frozen_tensor,
                                    persisted_tensors):
    """Reconstructs a flattened persisted tensor from its field.

    Args:
      field: String field name. Nested fields are separated with the side inputs
        separator symbol.
      frozen_tensor: The frozen tensor to add to the persisted tensors.
      persisted_tensors: Dictionary of string keys to persisted tensor
        `Tensors`.

    Returns:
      A copy of persisted tensors with the frozen tensor.
    """

    persisted_tensors = persisted_tensors.copy()
    nested_persisted_tensors = persisted_tensors
    fields = field.split(self.Keys.PERSISTED_TENSORS_SEPARATOR)
    for i in range(len(fields) - 1):
      key = fields[i]
      if key not in nested_persisted_tensors:
        nested_persisted_tensors[key] = {}
      nested_persisted_tensors = nested_persisted_tensors[key]
    nested_persisted_tensors[fields[-1]] = frozen_tensor
    return persisted_tensors

  def _weighted_subnetwork_collection_key(self, index, field):
    """Returns the collection key for the given arguments.

    Args:
      index: Integer index of the weighted subnetwork in a list.
      field: String name of one of the weighted subnetwork's fields.

    Returns:
      String collection key.
    """

    return "{}/weighted_subnetwork/{}".format(index, field)

  def _weighted_subnetwork_collection_key_field(self, collection_key, index):
    """Returns a weighted subnetwork's field name from the given arguments.

    Args:
      collection_key: String name of the collection where the field `Tensor` is
        stored during freezing.
      index: Integer index of the weighted subnetwork in a list.

    Returns:
      String name of one of the weighted subnetwork's fields.
    """

    prefix = "{}/weighted_subnetwork/".format(index)
    if not collection_key.startswith(prefix):
      return None
    return collection_key.replace(prefix, "")

  def _subnetwork_collection_key(self, index, field):
    """Returns the collection key for the given arguments.

    Args:
      index: Integer index of the subnetwork in a list of subnetworks.
      field: String name of one of the subnetwork's fields.

    Returns:
      String collection key.
    """

    return "{}/weighted_subnetwork/subnetwork/{}".format(index, field)

  def _subnetwork_collection_key_field(self, collection_key, index):
    """Returns a subnetwork's field name from the given arguments.

    Args:
      collection_key: String name of the collection where the field `Tensor` is
        stored during freezing.
      index: Integer index of the subnetwork in a list of subnetworks.

    Returns:
      String name of one of the subnetwork's fields.
    """

    prefix = "{}/weighted_subnetwork/subnetwork/".format(index)
    if not collection_key.startswith(prefix):
      return None
    return collection_key.replace(prefix, "")


def prune_graph(input_graph_def, output_node_names):
  """Extracts a subgraph, and removes some nodes.

  Removes nodes with "global_step" and "current_iteration" in their names.
  Recursively keeps nodes that are colocated with any nodes in the output graph.

  Args:
    input_graph_def: GraphDef object holding the network.
    output_node_names: List of name strings for the result nodes of the graph.

  Returns:
    GraphDef containing a simplified version of the original.
  """

  output_graph_def = tf.GraphDef()
  node_names_in_output_graph = set()

  def _find_colocated_node_names(input_node):
    """Returns colocated node names specified in input_node proto."""

    colocated_node_names = set()
    if input_node.attr and _COLOCATION_ATTR_KEY in input_node.attr:
      colo_strings = input_node.attr[_COLOCATION_ATTR_KEY].list.s
      for colo_string in colo_strings:
        if colo_string.startswith(_COLOCATION_ATTR_PREFIX):
          colocated_node_name = (
              colo_string[len(_COLOCATION_ATTR_PREFIX):].decode("ascii"))
          colocated_node_names.add(colocated_node_name)
    return colocated_node_names

  def _copy_node_to_output_graph(input_node):
    """Copies node to output_graph_def; updates node_names_in_output_graph."""

    output_node = tf.NodeDef()
    output_node.CopyFrom(input_node)
    output_graph_def.node.extend([output_node])
    node_names_in_output_graph.add(output_node.name)

  missing_node_names = output_node_names
  graph_library = None
  graph_versions = None

  while missing_node_names:
    subgraph = tf.graph_util.extract_sub_graph(input_graph_def,
                                               missing_node_names)
    if graph_library is None:
      graph_library = subgraph.library
    if graph_versions is None:
      graph_versions = subgraph.versions
    colocated_node_names_seen = set()
    for node in subgraph.node:
      if "global_step" in node.name or "current_iteration" in node.name:
        continue
      _copy_node_to_output_graph(node)
      colocated_node_names_seen |= _find_colocated_node_names(node)
    missing_node_names = list(colocated_node_names_seen -
                              node_names_in_output_graph)

  output_graph_def.library.CopyFrom(graph_library)
  output_graph_def.versions.CopyFrom(graph_versions)
  return output_graph_def
