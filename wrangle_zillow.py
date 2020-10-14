import pandas as pd
import numpy as np
import acquire
from sklearn.model_selection import train_test_split

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
    Drops rows where unit count is more than 1  
    Drops columns where the percentage of missing data is 40% or more.
    Drop columns where the percentage of missing data is 60% or more.
    Splits the data into train, validate, test sets for modelings
    Imputes missing continuous/discrete with median/mode respectively
    '''
    df = acquire.load_zillow_data()
    df = df[df.propertylandusetypeid.isin([261, 262, 273])]
    df.drop(columns = ['buildingclasstypeid', 'typeconstructiontypeid', 'storytypeid',
        'propertylandusetypeid', 'heatingorsystemtypeid',
        'architecturalstyletypeid', 'airconditioningtypeid', 'id', 'parcelid'], inplace = True)
    df.drop(columns = [c for c in df.columns if c.endswith('.1')], inplace = True)
    df = df[df.unitcnt == 1.0]
    df.replace({True:1, False:0}, inplace = True)
    df['heatingorsystemdesc'].fillna('None', inplace=True)
    df = handle_missing_values(df, .6, .6)
    df.drop(columns=['calculatedbathnbr', 'unitcnt', 'fullbathcnt', 'propertyzoningdesc'], inplace = True)
    
    train_validate, test = train_test_split(df, test_size=.2, random_state=369)
    train, validate = train_test_split(train_validate, test_size=.25, random_state=369)
    
    med_cols = [
    "taxamount",
    "calculatedfinishedsquarefeet",
    "structuretaxvaluedollarcnt",
    "lotsizesquarefeet",
    "buildingqualitytypeid"
    ]

    for col in med_cols:
        median = train[col].median()
        train[col].fillna(median, inplace=True)
        validate[col].fillna(median, inplace=True)
        test[col].fillna(median, inplace=True)
        
    mod_cols = [
    "yearbuilt",
    "regionidzip",
    'regionidcity']

    for col in mod_cols:
        mode = int(train[col].mode())# I had some friction when this returned a float (and there were no decimals anyways)
        train[col].fillna(value=mode, inplace=True)
        validate[col].fillna(value=mode, inplace=True)
        test[col].fillna(value=mode, inplace=True)
    
    mode = str(train['censustractandblock'].mode())
    train['censustractandblock'].fillna(value=mode, inplace=True)
    validate['censustractandblock'].fillna(value=mode, inplace=True)
    test['censustractandblock'].fillna(value=mode, inplace=True)


    return train, validate, test

    