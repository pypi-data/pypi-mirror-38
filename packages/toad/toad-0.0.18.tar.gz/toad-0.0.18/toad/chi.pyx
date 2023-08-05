import numpy as np
cimport cython

from cython.parallel import prange

ctypedef fused number:
    int
    double
    long

cdef int DEFAULT_BINS = 20

def fillna(feature, by = -1):
    # copy array
    copied = np.copy(feature)

    copied[np.isnan(copied)] = by
    return copied


def ChiMerge(feature, target, n_bins = None, min_samples = None, min_threshold = None, nan = -1):
    """Chi-Merge

    Args:
        feature (array-like): feature to be merged
        target (array-like): a array of target classes
        n_bins (int): n bins will be merged into
        min_samples (number): min sample in each group, if float, it will be the percentage of samples
        min_threshold (number): min threshold of chi-square

    Returns:
        array: array of split points
    """

    # set default break condition
    if n_bins is None and min_samples is None and min_threshold is None:
        n_bins = DEFAULT_BINS

    if min_samples and min_samples < 1:
        min_samples = len(feature) * min_samples


    feature = fillna(feature, by = nan)

    target_unique = np.unique(target)
    feature_unique = np.unique(feature)
    len_f = len(feature_unique)
    len_t = len(target_unique)
    grouped = np.zeros((len_f, len_t))
    # grouped[:,1] = feature_unique
    for i in range(len_f):
        tmp = target[feature == feature_unique[i]]
        for j in range(len_t):
            grouped[i,j] = (tmp == target_unique[j]).sum()


    while(True):
        # Calc chi square for each group
        l = len(grouped) - 1
        chi_list = np.zeros(l)
        chi_min = np.inf
        chi_ix = []
        for i in range(l):
            couple = grouped[i:i+2,:]
            total = np.sum(couple)
            cols = np.sum(couple, axis = 0)
            rows = np.sum(couple, axis = 1)

            e = np.zeros(couple.shape)
            for j in range(couple.shape[0]):
                for k in range(couple.shape[1]):
                    e[j,k] = rows[j] * cols[k] / total

            chi = np.sum(np.nan_to_num((couple - e) ** 2 / e))
            chi_list[i] = chi

            if chi == chi_min:
                chi_ix.append(i)
                continue

            if chi < chi_min:
                chi_min = chi
                chi_ix = [i]

        # break loop when the minimun chi greater the threshold
        if min_threshold and chi_min > min_threshold:
            break

        # get indexes of the groups who has the minimun chi
        min_ix = np.array(chi_ix)

        # get the indexes witch needs to drop
        drop_ix = min_ix + 1


        # combine groups by indexes
        retain_ix = min_ix[0]
        last_ix = retain_ix
        for ix in min_ix:
            # set a new group
            if ix - last_ix > 1:
                retain_ix = ix

            # combine all contiguous indexes into one group
            grouped[retain_ix] = grouped[retain_ix] + grouped[ix + 1]
            last_ix = ix


        # drop binned groups
        grouped = np.delete(grouped, drop_ix, axis = 0)
        feature_unique = np.delete(feature_unique, drop_ix)

        # break loop when reach n_bins
        if n_bins and len(grouped) <= n_bins:
            break

        # break loop if min samples of groups is greater than threshold
        if min_samples and np.sum(grouped.values, axis = 1).min() > min_samples:
            break

    return feature_unique[1:]
