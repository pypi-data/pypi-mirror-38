import sys

if sys.version_info[0] == 2:
    from .society2 import core_value_decode, core_value_encode
else:
    from .society3 import core_value_encode, core_value_decode
