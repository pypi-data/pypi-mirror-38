####################################################################################################
# neuropythy/util/__init__.py
# This file defines the general tools that are available as part of neuropythy.

from .core import (ObjectWithMetaData, to_affine, simplex_summation_matrix,
                   simplex_averaging_matrix, is_image, curry,
                   zinv, zdiv, times, divide, zdivide, plus, minus,
                   library_path, address_data, is_address, AutoDict,
                   curve_spline, curve_intersection, CurveSpline)
from .conf import (config, to_credentials, detect_credentials, load_credentials)


