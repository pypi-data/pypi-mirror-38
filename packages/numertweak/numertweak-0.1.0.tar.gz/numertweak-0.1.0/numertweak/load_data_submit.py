from zipfile import ZipFile
import pandas as pd
import numpy as np
import gc


def load_data_submit(path="./", filetype="zip", zipdir=""):
    """Load Tournament/Submit data set

    Parameters:
    -----------
    path : str
        relative path of the data file

    filetype : str
        "zip" or "csv"

    zipfolder : str
        location of the "numerai_tournament_data.csv" file
        within the zip file (Only applicable if filetype="zip")

    Return:
    -------
    X_submit
    ids_submit
    pd_index
    Y_valid
    era_valid
    idx_valid

    Example
    -------
        from numertweak import load_data_submit
        X_test, Y_valid, idx_valid = load_data_submit(path)
    """
    filename = "numerai_tournament_data.csv"
    if filetype is "zip":
        # unzip test set
        with ZipFile(path + "numerai_datasets.zip") as zipptr:
            with zipptr.open(zipdir + filename) as csv2:
                df2 = pd.read_csv(csv2)
    elif filetype is "csv":
        df2 = pd.read_csv(path + filename)
    else:
        raise Exception("filetype must be 'zip' or 'csv'.")

    # export only X_test = df2[x_cols].values
    x_cols = list(df2.filter(regex="feature").columns)
    X_submit = df2[x_cols].values.astype(np.float32)
    ids_submit = df2['id'].values
    pd_index = df2.index.values

    # index which predictions Y_pred[idx_valid]
    # can be compared with the validation set
    idx_valid = df2['data_type'] == 'validation'

    # to export Y_valid = df2[y_cols].values[idx_valid]
    # don't use "np.bool_". use uint8 instead
    y_cols = list(df2.filter(regex="target_").columns)
    Y_valid = df2[y_cols].values[idx_valid].astype(np.uint8)
    era_valid = df2['era'].values[idx_valid]

    # destroy dataframe
    del df2
    gc.collect()

    # done
    return X_submit, ids_submit, pd_index, Y_valid, era_valid, idx_valid
