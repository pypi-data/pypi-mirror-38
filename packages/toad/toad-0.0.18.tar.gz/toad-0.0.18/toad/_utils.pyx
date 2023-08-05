import numpy as np
cimport numpy as np

cpdef np_count(np.ndarray arr, value, default = None):
    print('1111111')
    # c = (arr == value).sum()
    #
    # if default is not None and c == 0:
    #     return default
    #
    # return c
