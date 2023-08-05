# -*- coding: utf-8 -*-
#import pandas as pd
import mr_clean.core.functions.basics as basics
from mr_clean.core.functions.scrub import smart_scrub
from mr_clean.core.functions.colnames import smart_colnames
import pandas as pd
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
    """
    global DEBUG
    df = df.copy()
    DEBUG = debug
    # Change colnames
    df.columns = smart_colnames(df)
    print_('Changed colnames to {}'.format(df.columns))
    # Remove extra whitespace
    print_("Removing extra whitespace...")
    obj_col_list = df.select_dtypes(include = 'object').columns
    for col_name in obj_col_list:
        df[col_name] = basics.col_strip(df,col_name)
        print_(f"  Stripped extra whitespace from '{col_name}'")

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
    # df = df.replace(r'^\s+$', pd.np.nan,regex=True) # Removing whitespace-only cells
    # df = df.replace('',pd.np.nan) # removing empty string cells
    as_cat = df[col_name].astype('category')
    as_num = pd.to_numeric(df[col_name], errors = 'coerce')
    as_dt = pd.to_datetime(df[col_name], errors = 'coerce', infer_datetime_format = True)

    dtypes = ['category','number','datetime']

    new_cols = [as_cat,as_num,as_dt]

    error_rates = [col.isnull().sum() for col in new_cols]
    prior_rate = df[col_name].isnull().sum()
    error_rates = [rate-prior_rate for rate in error_rates]
    error_rates[0] = len(new_cols[0].value_counts())+1
    error_rate*=df.shape[0] # Rows
    lowest_rate = min(error_rates)

    for index in range(3):
        if error_rates[index] <= error_rate and \
            error_rates[index] <= lowest_rate:
                df[col_name] = new_cols[index]
                return dtypes[index]
