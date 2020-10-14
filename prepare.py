import pandas as pd
import numpy as np
import acquire

def handle_missing_values(df, prop_required_column=.5, prop_required_row=.5):
    '''
    This function takes in a DataFrame (df), a minium for prop_required_column [0:1] with deafult of .5, 
    and a minimum value [0:1] for prop_required_row with a default of .5.
    
    It will first drop columns who's missing data is less than prop_required_column value.
    It will then drop the rows who's missing data is lower than the prop_required_row.
    '''
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

def prep_zillow():
    '''
    Loads zillow data and then fliters it where propertylandusetypeid is 261, 262, or 273.
    Drops unnecessary id columns and any duplicated columns.    
    Creates a has_basement column where basementsqft > 0.
    Drops columns where the percentage of missing data is over 25%
    Drop columns where the percentage of missing data is over 25%
    '''
    df = acquire.load_zillow_data()
    df = df[df.propertylandusetypeid.isin([261, 262, 273])]
    df.drop(columns = ['buildingclasstypeid', 'typeconstructiontypeid', 'storytypeid',
        'propertylandusetypeid', 'heatingorsystemtypeid',
        'architecturalstyletypeid', 'airconditioningtypeid', 'id', 'parcelid'], inplace = True)
    df.drop(columns = [c for c in df.columns if c.endswith('.1')], inplace = True)
    df['has_basement'] = df['basementsqft'] > 0
    df.replace({True:1, False:0}, inplace = True)
    