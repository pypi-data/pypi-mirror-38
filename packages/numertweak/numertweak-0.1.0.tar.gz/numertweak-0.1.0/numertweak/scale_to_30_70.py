import numpy as np


# scale_to_30_70(Y_probs)
def scale_to_30_70(x):
    c = x - .5
    m = np.max(np.abs(c))
    return c * .2 / m + .5
