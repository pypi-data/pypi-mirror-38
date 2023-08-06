name = "tsalib"

#import sys
#if sys.version_info < (3, 6, 1):
#    raise RuntimeError("TSAlib requires Python 3.6.1 or later")

from tsalib.ts import dim_var, dim_vars, declare_common_dim_vars
from tsalib.ext import view_transform, permute_transform, expand_transform
