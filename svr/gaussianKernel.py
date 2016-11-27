# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 16:32:03 2016

@author: ding_wensi
"""

import numpy as np


def gaussianKernel(X1, X2, sigma=0.1):
    m = X1.shape[0]
    n = X2.shape[0]
    K = np.zeros((m, n))

    # ====================== YOUR CODE HERE =======================
    # Instructions: Calculate the Gaussian kernel (see the assignment
    #				for more details).
    for i in range(m):
        K[i, :] = np.exp(-np.linalg.norm(X1[i, :] - X2, axis=1)
                         ** 2 / (2 * (sigma**2)))
    # =============================================================

    return K
