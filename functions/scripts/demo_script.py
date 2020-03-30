#!/usr/bin/env python3

''' Required for all scripts '''
import pandas as pd
from flask import Flask, make_response, abort
from flask import current_app as app

''' Custom '''
# import requests


def run(script_args):
    ''' Your function logic 

    Get query arguments using `script_args['key']`

    Use `app.logger.error()` to log errors

    Must throw exceptions

    Must return a dataframe (can be empty) or a boolean

    '''

    data = [[500, 250], [150, 550], [325, 850]]

    result = pd.DataFrame(data, columns=['col1', 'col2'])
    
    '''
    Empty DataFrame response example
    '''
    #result = pd.DataFrame(columns=['col1', 'col2'])
    
    '''
    Boolean response example
    '''
    
    #result = True
    
    return result
