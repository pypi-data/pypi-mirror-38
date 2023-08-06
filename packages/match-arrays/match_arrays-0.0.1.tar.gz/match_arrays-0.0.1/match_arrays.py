'''
Created on 29.11.2017

@author: mschroeder
'''

import numpy as np

def match_arrays(a, b):
    """
    Find occurences of b in a.
    
    Arguments:
        a, b (np.ndarray): Arrays of matching type.
        
    Returns:
        idx_a, idx_b: Indices of matching entries in a and b.
            a[idx_a[i]] == b[idx_b[i]]

    >>> a = np.arange(100)
    >>> b = np.random.permutation(a)
    >>> idx_a, idx_b = match_arrays(a, b)
    >>> assert(np.all(a[idx_a] == b[idx_b]))

    """
    order = np.argsort(a)
    
    sorted_a = a[order]
    
    idx_sorted_a = np.searchsorted(sorted_a, b)
    
    mask = idx_sorted_a < sorted_a.shape[0]
    mask[mask] = sorted_a[idx_sorted_a[mask]] == b[mask]
    
    idx_sorted_a = idx_sorted_a[mask]
    idx_b = np.where(mask)[0]
    
    return order[idx_sorted_a], idx_b