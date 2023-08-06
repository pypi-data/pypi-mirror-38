import numpy as np
from sklearn.metrics import log_loss


def consistency(era_valid, Y_valid, Y_proba):
    """Compute the percentage of Eras/Folds below -LogLoss(.5)
    """
    eras = np.unique(era_valid)
    n = len(eras)
    losses = np.ones(shape=(n,))
    for i, e in enumerate(eras):
        idx_era = era_valid == e
        losses[i] = log_loss(
            Y_valid[idx_era].astype(float),
            Y_proba[idx_era].astype(float))

    return sum(losses < -np.log(.5)) / float(n), losses
