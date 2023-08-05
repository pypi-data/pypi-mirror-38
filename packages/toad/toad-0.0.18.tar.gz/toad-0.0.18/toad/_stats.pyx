from libc.math cimport log

cpdef double _WOE(double y_prob, double n_prob):
    """get WOE of a group

    Args:
        y_prob: the probability of grouped y in total y
        n_prob: the probability of grouped n in total n
    """
    
    return log(y_prob / n_prob)
