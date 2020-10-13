import pandas as pd
import numpy as np
import acquire

def handle_missing_values(df, prop_required_column, prop_required_row):
    columns_to_keep = []
    columns = df.columns
    for col in columns:   
        if df[col].notnull().sum()/df.shape[0] >= prop_required_column:
            columns_to_keep.append(col)
    df = df[columns_to_keep]
    df['row_to_keep'] = df.notnull().sum(axis=1)/df.shape[1] >= prop_required_row
    df = df.loc[df['row_to_keep'] == True]
    df.drop(columns= ['row_to_keep'], inplace = True)
    return df