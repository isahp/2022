import numpy as np
import pandas as pd
import pyanp.limitmatrix as lm
import pyanp.rowsens as rowsens

def scale_mat(unscaled_mat, cluster_mat, nnodes):
    if len(nnodes) != len(cluster_mat):
        raise Exception("Must have the number of items in nnodes same as dimensions of cluster_mat")
    scaled = np.array(unscaled_mat)
    row_offset=0
    for crow in range(len(cluster_mat)):
        col_offset=0
        row_nodes=nnodes[crow]
        for ccol in range(len(cluster_mat)):
            col_nodes=nnodes[ccol]
            for row in range(row_offset, row_offset+row_nodes):
                for col in range(col_offset, col_offset+col_nodes):
                    scaled[row,col]*=cluster_mat[crow,ccol]
            col_offset+=col_nodes
        row_offset+=row_nodes
    return scaled

def lmsynth(scaled_mat, alts):
    '''
    Calculates the limit matrix and extracts the priorites for the listed alternative indices
    '''
    limit_mat = lm.calculus(scaled_mat)
    lp = lm.priority_from_limit(limit_mat)[alts]
    return lp / lp.sum()

def influence_priority(scaled_mat, row, p, alts, **kwargs):
    '''
    kwargs is the same as rowsensitivity.row_adjust() takes
    Does row sensitivity first
    Then lmsynth()
    '''
    sens = rowsens.row_adjust(scaled_mat, row, p, **kwargs)
    return lmsynth(sens, alts)
