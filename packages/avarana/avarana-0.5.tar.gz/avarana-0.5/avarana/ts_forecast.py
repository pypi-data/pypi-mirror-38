# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 13:06:35 2018

@author: hrajiv
"""
import pandas as pd
import sys
import numpy as np
import avarana

name='ts_forecast'

def lag(array, start_index, end_index, lag):
    lag_start_index = start_index-lag
    lag_end_index = end_index-lag
    yyy = array[lag_start_index:lag_end_index]
    return yyy

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true[y_true==0] = y_true[y_true>0].min() 
    h1 = np.abs(y_true - y_pred)
    h2 = np.divide(h1, y_true)
    return np.mean(h2)

def tf_mape(y_true, y_pred):
    y_true[y_true==0] = y_true[y_true>0].min() 
    h1 = np.abs(y_true - y_pred)
    h2 = np.divide(h1, y_true)
    return np.mean(h2)

def weighted_absolute_percentage_error(y_true, y_pred): 
    return np.abs(y_true - y_pred).sum()/y_true.sum()

def mape_forecast_ARNN(data, lags=[], verbose=0):
      
    # Used for filenames
    signature = avarana.get_function_name()
    n = max(lags)
    data_len = len(data)
    observed_len = data.last_valid_index() + 1
    
    # Twice the number of periods in year to allow for lag
    train_len = 2*n
    
    if observed_len < train_len:
        print('Not enough training observations. Need a minimum of %i observations' %train_len, file=sys.stderr)
        return None, -1 
    
    # Based on the last non null value
    test_len = data.last_valid_index() - train_len + 1 

    # If there are no observations for forecast 
    if data_len <= train_len:
        print('No data in forecast period', file=sys.stderr)
        return None, -1
     
    # Replace missing with zeros
    data.fillna(0, inplace=True)

    target = data.astype(float).copy()        

    lag_columns = ['X%s' % x for x in lags]
    X_lag_df = pd.DataFrame(columns = lag_columns)
    
    for i in range(len(lags)):
        lag_temp = lag(target.copy(), n, train_len, lags[i])
        X_lag_df[lag_columns[i]] = lag_temp.reset_index(drop=True)

    X = X_lag_df.copy()
    y = target[n:train_len].copy()
    
    X_test_lag_df = pd.DataFrame(columns = lag_columns)    
    for i in range(len(lags)):
        lag_temp = lag(target.copy(), train_len, train_len + test_len, lags[i])
        X_test_lag_df[lag_columns[i]] = lag_temp.reset_index(drop=True)

    X_test = X_test_lag_df.copy()    
    y_test = target[train_len:train_len+test_len].reset_index(drop=True).copy()    
    
    # Model configuration
    mape = -1
    model, predictions, mape = avarana.nnet_regressor(X, y,
                                                      X_test, y_test, 
                                                      hidden_layers=[n],
                                                      activation='relu',
                                                      loss='mape',
                                                      verbose=verbose)
    
    for j in range(train_len, data_len):
        X_fcst_lag_df = pd.DataFrame(columns = lag_columns)    
        for i in range(len(lags)):
            lag_temp = lag(target.copy(), j, j+1, lags[i])
            X_fcst_lag_df[lag_columns[i]] = lag_temp.reset_index(drop=True)        

        X_fcst = X_fcst_lag_df.copy()
        
        Y_fcst = model.predict(X_fcst.values)
        target[j] = Y_fcst[0][0]
    
    
    return target[train_len:data_len].copy(), mape

def mape_forecast_ARNNEXOG(data, target_col, lags=[], verbose=0):
    
    if target_col is None:
        print('Target variable is undefined', file=sys.stderr)
        return None, -1
    
    if target_col not in data.columns:
        print(target_col, ' not found in data', file=sys.stderr)
        return None,-1
    
    # Used for filenames
    signature = avarana.get_function_name()
    if len(lags) == 0:
        print('Lags cannot be empty to ', signature, file=sys.stderr)
        return None, -1
    n = max(lags)
    data_len = len(data)
    observed_len = data[target_col].last_valid_index() + 1
    
    # Twice the number of periods in year to allow for lag
    train_len = 2*n
    
    if observed_len < train_len:
        print('Not enough training observations. Need a minimum of %i observations', train_len, file=sys.stderr)
        return None,-1 
    
    # Based on the last non null value
    test_len = data[target_col].last_valid_index() - train_len + 1 

    # If there are no observations for forecast 
    if data_len <= train_len:
        print('No data in forecast period', file=sys.stderr)
        return None,-1
    
    # Replace missing with zeros
    data.fillna(0, inplace=True)

    target = data[target_col].astype(float).copy()        
    data.drop(target_col, axis=1, inplace=True)
        
    lag_columns = ['X%s' % x for x in lags]
    X_lag_df = pd.DataFrame(columns = lag_columns)
    
    for i in range(len(lags)):
        lag_temp = lag(target.copy(), n, train_len, lags[i])
        X_lag_df[lag_columns[i]] = lag_temp.reset_index(drop=True)

    X = data[n:train_len].reset_index(drop=True).copy()
    Z = pd.concat([X_lag_df,X], axis=1, sort=False)
    X = Z  
    y = target[n:train_len].copy()
    
    X_test_lag_df = pd.DataFrame(columns = lag_columns)    
    for i in range(len(lags)):
        lag_temp = lag(target.copy(), train_len, train_len + test_len, lags[i])
        X_test_lag_df[lag_columns[i]] = lag_temp.reset_index(drop=True)

    X_test = data[train_len:train_len+test_len].reset_index(drop=True).copy()
    Z = pd.concat([X_test_lag_df, X_test], axis=1, sort=False)
    X_test = Z
    
    y_test = target[train_len:train_len+test_len].reset_index(drop=True).copy()    
    
    # Model configuration
    mape = -1
    model, predictions, mape = avarana.nnet_regressor(X, y,
                                                      X_test, y_test, 
                                                      hidden_layers=[n],
                                                      activation='relu',
                                                      loss='mape',
                                                      verbose=verbose)
    for j in range(train_len, data_len):
        X_fcst_lag_df = pd.DataFrame(columns = lag_columns)    
        for i in range(len(lags)):
            lag_temp = lag(target.copy(), j, j+1, lags[i])
            X_fcst_lag_df[lag_columns[i]] = lag_temp.reset_index(drop=True)        

        X_fcst=data[j:j+1].reset_index(drop=True).copy()
        Z = pd.concat([X_fcst_lag_df,X_fcst], axis=1, sort=False)
        X_fcst = Z
        
        Y_fcst = model.predict(X_fcst.values)
        target[j] = Y_fcst[0][0]
    
    
    return target[train_len:data_len].copy(), mape    