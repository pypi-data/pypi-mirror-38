# coding=utf-8
# Copyright 2018 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Splits related API."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
import collections
import operator

import six
from six.moves import zip  # pylint: disable=redefined-builtin

from tensorflow_datasets.core import utils

__all__ = [
    "NamedSplit",
    "Split",
    "SplitDict",
    "SplitGenerator",
    "SplitInfo",
]


@six.add_metaclass(abc.ABCMeta)
class _SplitDescriptorNode(object):
  """Abstract base class for Split compositionality.

  There are three parts to the composition:
    1) The splits are composed (defined, merged, splitted,...) together before
       calling the .as_dataset() function. This is done with the __add__,
       __getitem__, which return a tree of _SplitDescriptorNode (whose leaf are
       the NamedSplit objects)

        split = tfds.TRAIN + tfds.TEST[:50]

    2) The _SplitDescriptorNode is forwarded to the .as_dataset() function to be
       resolved into actual read instruction. This is done by the
       .get_read_instruction() method which takes the real dataset splits
       (name, number of shards,...) and parse the tree to return a
       SplitReadInstruction() object

        read_instruction = split.get_read_instruction(self.info.splits)

    3) The SplitReadInstruction is then used in the tf.data.Dataset pipeline
       to define which files to read and how to skip samples within file.

        files_to_read = read_instruction.split_info_list
        slice_per_file = read_instruction.slice_list

  """

  @abc.abstractmethod
  def get_read_instruction(self, split_dict):
    """Parse the descriptor tree and compile all read instructions together.

    Args:
      split_dict: (dict) The dict[split_name, SplitInfo] of the dataset

    Returns:
      split_read_instruction (SplitReadInstruction)
    """
    raise NotImplementedError("Abstract method")

  def __eq__(self, other):
    """Equality: tfds.Split.TRAIN == 'train'."""
    if isinstance(other, (NamedSplit, six.string_types)):
      return False
    raise NotImplementedError(
        "Equality is not implemented between merged/sub splits.")

  def __add__(self, other):
    """Merging: tfds.Split.TRAIN + tfds.Split.TEST."""
    return _SplitMerged(self, other)

  def __getitem__(self, slice_value):
    """Synthetic subsplit: tfds.Split.TRAIN[30:50]."""
    return _SubSplit(self, slice_value)


class _SplitMerged(_SplitDescriptorNode):
  """Represent two split descriptors merged together."""

  def __init__(self, split1, split2):
    self._split1 = split1
    self._split2 = split2

  def get_read_instruction(self, split_dict):
    read_instruction1 = self._split1.get_read_instruction(split_dict)
    read_instruction2 = self._split2.get_read_instruction(split_dict)
    return read_instruction1 + read_instruction2


class _SubSplit(_SplitDescriptorNode):
  """Represent a sub split of a split descriptor."""

  def __init__(self, split, slice_value):
    self._split = split
    self._slice_value = slice_value

  def get_read_instruction(self, split_dict):
    return self._split.get_read_instruction(split_dict)[self._slice_value]


class NamedSplit(_SplitDescriptorNode):
  """Descriptor corresponding to a named split (train, test,...).

  Each descriptor can be composed with other using addition or slice. Ex:

    split = tfds.Split.TRAIN[0:25] + tfds.Split.TEST

  The resulting split will correspond to 25% of the train split merged with
  100% of the test split.

  Warning:
    A split cannot be added twice, so the following will fail:

      split = tfds.Split.TRAIN[:25] + tfds.Split.TRAIN[75:]
      split = tfds.Split.TEST + tfds.Split.ALL

  Warning:
    The slices can be applied only one time. So the following are valid:

      split = tfds.Split.TRAIN[0:25] + tfds.Split.TEST[0:50]
      split = (tfds.Split.TRAIN + tfds.Split.TEST)[0:50]

    But not:

      split = tfds.Split.TRAIN[0:25][0:25]
      split = (tfds.Split.TRAIN[:25] + tfds.Split.TEST)[0:50]

  """

  def __init__(self, name):
    self._name = name

  def __str__(self):
    return self._name

  def __eq__(self, other):
    """Equality: tfds.Split.TRAIN == 'train'."""
    if isinstance(other, NamedSplit):
      return self._name == other._name   # pylint: disable=protected-access
    elif isinstance(other, _SplitDescriptorNode):
      return False
    elif isinstance(other, six.string_types):  # Other should be string
      return self._name == other
    else:
      raise ValueError("Equality not supported between split {} and {}".format(
          self, other))

  def get_read_instruction(self, split_dict):
    return SplitReadInstruction(split_dict[self._name])


class NamedSplitAll(NamedSplit):

  def __init__(self):
    super(NamedSplitAll, self).__init__("all")

  def get_read_instruction(self, split_dict):
    # Merge all dataset split together
    read_instructions = [SplitReadInstruction(s) for s in split_dict.values()]
    return six.moves.reduce(operator.add, read_instructions)


class Split(object):
  """`Enum` for dataset splits.

  Datasets are typically split into different subsets to be used at various
  stages of training and evaluation.

  * `TRAIN`: the training data.
  * `VALIDATION`: the validation data. If present, this is typically used as
    evaluation data while iterating on a model (e.g. changing hyperparameters,
    model architecture, etc.).
  * `TEST`: the testing data. This is the data to report metrics on. Typically
    you do not want to use this during model iteration as you may overfit to it.
  * `ALL`: Special value corresponding to all existing split of a dataset
    merged together
  """
  TRAIN = NamedSplit("train")
  TEST = NamedSplit("test")
  VALIDATION = NamedSplit("validation")
  # All is a special Split which correspond to all split merged together
  ALL = NamedSplitAll()


# Similar to SplitInfo, but contain an additional slice info
SlicedSplitInfo = collections.namedtuple("SlicedSplitInfo", [
    "split_info",
    "slice_value",
])


class SplitReadInstruction(object):
  """Object containing the reading instruction for the dataset.

  Similarly to SplitDescriptor nodes, this object can be composed with itself,
  but the resolution happens instantaneously, instead of keeping track of the
  tree, such as all instuctions are compiled and flattened in a single
  SplitReadInstruction object containing the list of files and slice to use.

  Once resolved, the instructions can be accessed with:

    read_instructions.get_list_sliced_split_info()  # List of splits to use

  """

  def __init__(self, split_info=None):
    self._splits = utils.NonMutableDict(
        error_msg="Overlap between splits. Split {key} has been added with "
        "itself.")

    if split_info:
      self.add(SlicedSplitInfo(split_info=split_info, slice_value=None))

  def add(self, sliced_split):
    """Add a SlicedSplitInfo the read instructions."""
    # TODO(epot): Check that the number of samples per shard % 100 == 0
    # Otherwise the slices value may be unbalanced and not exactly reflect the
    # requested slice.
    self._splits[sliced_split.split_info.name] = sliced_split

  def __add__(self, other):
    """Merging split together."""
    # Will raise error if a split has already be added (NonMutableDict)
    # TODO(epot): If a split is already added but there is no overlapp between
    # the slices, should merge the slices (ex: [:10] + [80:])
    split_instruction = SplitReadInstruction()
    split_instruction._splits.update(self._splits)   # pylint: disable=protected-access
    split_instruction._splits.update(other._splits)   # pylint: disable=protected-access
    return split_instruction

  def __getitem__(self, slice_value):
    """Sub-splits."""
    # Will raise an error if a split has already been sliced
    split_instruction = SplitReadInstruction()
    for v in self._splits.values():
      if v.slice_value is not None:
        raise ValueError(
            "Trying to slice Split {} which has already been sliced".format(
                v.split_info.name))
      v = v._asdict()
      v["slice_value"] = slice_value
      split_instruction.add(SlicedSplitInfo(**v))
    return split_instruction

  def get_list_sliced_split_info(self):
    return list(sorted(self._splits.values(), key=lambda x: x.split_info.name))


def slice_to_percent_mask(slice_value):
  """Convert a python slice [15:50] into a list[bool] mask of 100 elements."""
  if slice_value is None:
    slice_value = slice(None)
  # Select only the elements of the slice
  selected = set(list(range(100))[slice_value])
  # Create the binary mask
  return [i in selected for i in range(100)]


# TODO(afrozm): Replace by the proto object.
# Could also add the number of sample here such as the user can do
# num_train_sample = builder.info.splits[tfds.Split.TRAIN].num_sample
SplitInfo = collections.namedtuple("SplitInfo", ["name", "num_shards"])


class SplitDict(utils.NonMutableDict):
  """Split info object."""

  def __init__(self):
    super(SplitDict, self).__init__(error_msg="Split {key} already present")

  def __getitem__(self, key):
    return super(SplitDict, self).__getitem__(str(key))

  def __setitem__(self, key, value):
    raise ValueError("Cannot add elem. Use .add() instead.")

  def add(self, split_info):
    """Add the split info."""
    super(SplitDict, self).__setitem__(str(split_info.name), split_info)

  # TODO(afrozm): Replace by proto
  def from_json_data(self, split_data):
    """Restore the splits info from the written metadata file."""
    self.clear()
    for s in split_data:
      self.add(SplitInfo(name=s["name"], num_shards=s["num_shards"]))

  def to_json_data(self):
    """Export the metadata for json export."""
    return [
        {"name": str(s.name), "num_shards": s.num_shards}
        for s in self.values()
    ]


class SplitGenerator(object):
  """Defines the split info for the generator.

  This should be used as returned value of
  `GeneratorBasedDatasetBuilder._split_generators`.
  See `GeneratorBasedDatasetBuilder._split_generators` for more info and example
  of usage.

  Args:
    name (str/list[str]): Name of the Split for which the generator will create
      the samples. If a list is given, the generator samples will be distributed
      among the splits proportionally to the num_shards
    num_shards (int/list[int]): Number of shards between which the generated
      samples will be written. If name is a list, then num_shards should be a
      list with the same number of element.
    gen_kwargs (dict): Kwargs to forward to the ._generate_samples() of the
      generator builder

  """

  def __init__(self, name, num_shards=1, gen_kwargs=None):
    self.gen_kwargs = gen_kwargs or {}

    if isinstance(name, list):
      split_zip = zip(name, num_shards)
    else:
      split_zip = [(name, num_shards)]

    self.split_info_list = [
        SplitInfo(name=str(n), num_shards=k) for n, k in split_zip
    ]
