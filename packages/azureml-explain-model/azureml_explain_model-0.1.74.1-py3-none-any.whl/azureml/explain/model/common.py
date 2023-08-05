# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines common constants and methods used by the model explanation package."""

import logging
import numpy as np

module_logger = logging.getLogger(__name__)
module_logger.setLevel(logging.INFO)

# Define common constants used in the package
MAX_NUM_BLOCKS = "max_num_blocks"
BLOCK_SIZE = "block_size"
NUM_FEATURES = "num_features"
NUM_BLOCKS = "num_blocks"

# Validate shap version
new_shap_api = True
minimum_shap_version = '0.20.0'
maximum_shap_version = '0.24.0'

try:
    import pkg_resources
    from distutils.version import StrictVersion
    shap_version = pkg_resources.get_distribution("shap").version
    new_shap_api = StrictVersion(shap_version) >= StrictVersion(minimum_shap_version)
    if not new_shap_api:
        module_logger.warning(
            "An older version of SHAP than the mimimum requirement %s is used", minimum_shap_version)
    if StrictVersion(shap_version) > StrictVersion(maximum_shap_version):
        module_logger.warning(
            "A newer version of SHAP than the supported version %s is used", maximum_shap_version)
except ImportError:
    module_logger.debug("Failed to determine the version of SHAP")


def _sort_features(features, order):
    return np.array(features)[order]


# sorts a single dimensional feature list according to order
def _sort_feature_list_single(features, order):
    return list(map(lambda x: features[x], order))


# returns a list of lists, where each internal list is the feature list sorted according to the order of a single class
def _sort_feature_list_multiclass(features, order):
    return [list(map(lambda x: features[x], order_i)) for order_i in order]


# do the equivalent of a numpy array slice on a two-dimensional list
def _two_dimensional_slice(lst, end_index):
    return list(map(lambda x: x[:end_index], lst))
