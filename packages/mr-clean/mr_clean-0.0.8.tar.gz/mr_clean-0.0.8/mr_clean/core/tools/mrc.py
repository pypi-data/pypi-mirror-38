# -*- coding: utf-8 -*-
#import pandas as pd
import mr_clean.core.functions.basics as basics
from mr_clean.core.functions.scrub import smart_scrub
from mr_clean.core.functions.colnames import smart_colnames
import pandas as pd
import numpy as np
#import mr_clean.core.stats.summary as stats

DEBUG = True

def clean(df,error_rate = 0,debug = True):
    """ Superficially cleans data, i.e. changing simple things about formatting.
    Parameters:
    df - DataFrame
        DataFrame to clean
    error_rate - float {0 <= error_rate <= 1}, default 0
        Maximum amount of errors/inconsistencies caused explicitly by cleaning, expressed
        as a percentage of total dataframe rows (0 = 0%, .5 = 50%, etc.)
        Ex: na values from coercing a column of data to numeric
    debug - Boolean, default True
        Whether or not to display print statements while cleaning
    """
    global DEBUG
    df = df.copy()
    DEBUG = debug
    # Change colnames
    df.columns = smart_colnames(df)
    print_(f'Changed colnames to {df.columns}')

    print_(f'Removed empty strings and None')

    # Remove extra whitespace
    print_("Removing extra whitespace...")
    obj_col_list = df.select_dtypes(include = 'object').columns
    for col_name in obj_col_list:
        df[col_name] = basics.col_strip(df,col_name)
        print_(f"  Stripped extra whitespace from '{col_name}'")
    # df = df.replace('',pd.np.nan).fillna(value=pd.np.nan) # empty string and None should be NaN

    # Coerce columns if possible
    print_("Coercing column datatypes where possible...")
    for col_name in obj_col_list:
        new_dtype = coerce_col(df,col_name,error_rate)
        if new_dtype is not None:
            print_(f"Coerced '{col_name}' to datatype '{new_dtype}'")

    # Scrub columns
    print_("Scrubbing object columns...")
    obj_col_list = df.select_dtypes(include = 'object').columns
    for col_name in obj_col_list:
        scrubf, scrubb = smart_scrub(df,col_name,error_rate)
        if scrubf is not None or scrubb is not None:
            print_(f"Scrubbed '{scrubf}' from the front and '{scrubb}' from the back of column '{col_name}'")

    # Coerice columns if possible
    print_("Coercing column datatypes where possible...")
    for col_name in obj_col_list:
        new_dtype = coerce_col(df,col_name,error_rate)
        if new_dtype is not None:
            print_(f"Coerced '{col_name}' to datatype '{new_dtype}'")
    return df

def print_(*args, **kwargs):
    global DEBUG
    if DEBUG == True:
        print(*args, **kwargs)

def coerce_col(df,col_name,error_rate):
    """ Change column datatype according to contents of column.
    Parameters:
    df - DataFrame
        DataFrame to edit
    col_name - str
        String that represents a column name
    error_rate - float
        Maximum amount of errors/inconsistencies caused explicitly by this function
    """
    data = df[col_name].replace(r'^\s*$', pd.np.nan,regex=True).fillna(value=pd.np.nan) # Removing whitespace and None
    as_cat = data.astype('category')
    as_num = pd.to_numeric(data, errors = 'coerce')
    as_dt = pd.to_datetime(data, errors = 'coerce', infer_datetime_format = True)

    # Setting up lists
    dtypes = ['number','datetime','category']
    new_cols = [as_num,as_dt]

    # Get error rates
    error_rates = [col.isnull().sum() for col in new_cols]
    prior_rate = data.isnull().sum()

    # Get additional error solely from coercion to numeric/dt
    error_rates = [rate-prior_rate for rate in error_rates]

    # TODO Come up with a good equation to model category error rate
    # Maybe average category size? IDK yet
    # Also want error rate of as_cat to always be non-negative
    # So that numeric data isn't coerced to categorical
    error_rates.append() = len(as_cat.value_counts())

    # Get error rate as a number of rows
    error_rate*=df.shape[0] # Rows

    # Get minimun error
    min_index = np.argmin(error_rates)[0]

    # If coercing doesn't work, return None
    if error_rates[min_index] > error_rate:
        return None

    df[col_name] = new_cols[min_index]
    return dtypes[min_index]
