import os
import shutil
import sys
import fnmatch
import numpy as np
from datetime import datetime, time
import unicodedata
import pandas as pd
from pandas.api.types import is_string_dtype
# import custom modules
import nccprops
from ncclogger import formatlogger as log

def encode_string_to_utf(y):
    y = unicodedata.normalize('NFKD',y).encode('ascii', errors='ignore').decode('utf-8')
    return (y)

def encode_numpy_to_utf(y):
    y = y.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return (y)

def format_time(time_string, source):
    try:
        if (source == 'fs'):
            time_split = time_string.split(":")
            return (time(int(time_split[0]), int(time_split[1]), 0))
        elif (source == 'op'):
            time_split = time_string.split(":")
            return (time(int(time_split[0]), int(time_split[1]), 0))
        elif (source == 'fts'):
            try:
                return (datetime.utcfromtimestamp(int(time_string)).strftime('%H:%M:%S'))
            except:
                return (0)
    except Exception:
        return (datetime.now().strftime("%H:%M:%S"))

def format_date(date_string, source):
    try:
        if (source == 'fs'):
            return (datetime.strptime(date_string,'%d %b %Y').date())
        elif (source == 'op'):
            return (datetime.strptime(date_string,'%d %b %Y').date())
        elif (source == 'fts'):
            try:
                return (datetime.utcfromtimestamp(int(date_string)).strftime('%Y-%m-%d'))
            except:
                return (0)
    except Exception:
        return (datetime.today().date()) ## done like this since we have already imported datetime module from datatime package
   

def remove_whitespace_from_df(df):    
    try:
        list_of_columns = df.columns    
        for i in list_of_columns:
            if (is_string_dtype(df[i])):
                if (i not in ('Date','Time')):
                    df[i] = df[i].str.strip()
    except Exception:
        log.error("Exception occurred while attempting to remove whitespaces from dataframe")
  
def remove_special_chars_from_df(df):
    try:
        for col in df.select_dtypes(include=[object]).columns:
            if (col not in ('Date','Time')):      
                df[col] = df[col].str.replace("'", "")
                df[col] = df[col].str.replace("/", "-")
                df[col] = df[col].str.replace("\\", "-")
                df[col] = df[col].str.strip()
    except Exception:
        log.exception("Exception occurred while trying to remove special characters")
            

