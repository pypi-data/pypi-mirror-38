from zipfile import ZipFile
import pandas as pd
import numpy as np
import gc


def load_data_train(path="./", filetype="zip", zipdir=""):
    """Load the training set

    Parameters:
    -----------
    path : str
        relative path of the data file

    filetype : str
        "zip" or "csv"

    zipfolder : str
        location of the "numerai_training_data.csv" file
        within the zip file (Only applicable if filetype="zip")

    Return:
    -------
    X_train
    Y_train
    era_id
    y_names

    Example
    -------
        X_train, Y_train, era_id, y_names = load_data_train(path)
    """
    filename = "numerai_training_data.csv"
    if filetype is "zip":
        # unzip training set
        with ZipFile(path + "numerai_datasets.zip") as zipptr:
            with zipptr.open(zipdir + filename) as csv1:
                df1 = pd.read_csv(csv1)
    elif filetype is "csv":
        df1 = pd.read_csv(path + filename)
    else:
        raise Exception("filetype must be 'zip' or 'csv'.")

    # export only X_train = df1[x_cols].values
    x_cols = list(df1.filter(regex="feature").columns)
    X_train = df1[x_cols].values.astype(np.float32)

    # to export Y_train = df1[y_cols].values
    y_cols = list(df1.filter(regex="target_").columns)
    Y_train = df1[y_cols].values.astype(np.uint8)  # don't use "np.bool_"

    # extract era IDs
    era_id = np.array([np.uint8(s[3:]) for s in df1['era']])

    # export the tournament names
    y_names = [s[7:] for s in y_cols]

    # destroy dataframe
    del df1
    gc.collect()

    return X_train, Y_train, era_id, y_names
