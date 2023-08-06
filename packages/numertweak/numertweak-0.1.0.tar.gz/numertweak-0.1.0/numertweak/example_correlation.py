from zipfile import ZipFile
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import gc


def example_correlation(tnam, Y_proba, path="./", filetype="zip", zipdir=""):
    """Load given example predictions

    Parameters:
    -----------
    tnam : str
        bernie, charles, elizabeth, jordan, ken

    Y_proba : np.ndarray
        Own probability predictions for "tnam"

    path : str
        relative path of the data file

    filetype : str
        "zip" or "csv"

    zipfolder : str
        location of the "example_predictions_target_<tnam>.csv" file
        within the zip file (Only applicable if filetype="zip")

    Returns:
    --------
    excorr : float
         Pearson correlation coefficient

    Example
    -------
        from numertweak import example_correlation
        excorr = example_correlation(tnam, Y_proba, path=path)
    """
    filename = 'example_predictions_target_' + tnam + '.csv'
    if filetype is "zip":
        # unzip test set
        with ZipFile(path + "numerai_datasets.zip") as zipptr:
            with zipptr.open(zipdir + filename) as csvex:
                dfex = pd.read_csv(csvex)
    elif filetype is "csv":
        dfex = pd.read_csv(path + filename)
    else:
        raise Exception("filetype must be 'zip' or 'csv'.")

    # combine dataset
    tmp = np.c_[dfex.values[:, 1], Y_proba].astype(float)

    # destroy dataframe
    del dfex
    gc.collect()

    # compute correlation
    return pearsonr(tmp[:, 0], tmp[:, 1])[0]
