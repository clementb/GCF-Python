#!/usr/bin/env python3

from flask import Flask, abort, jsonify, make_response
from flask import current_app as app
from importlib import import_module
import urllib.parse
import os


def main(request):
    ''' This is the function executed by gcloud (the entry point) '''
    gcfp_token = urllib.parse.unquote(request.args.get('gcfp_token'))
    app.logger.error(gcfp_token)
    script_name = request.args.get('script_name')
    script_args = request.args.to_dict()

    if 'gcfp_token' in script_args:
        del script_args['gcfp_token']

    if security(gcfp_token) == True:
        try:
            result = launch_script(script_name, script_args)
        except ImportError:
            app.logger.error("Error: could not import script")
            return abort(make_response(jsonify(message='Internal Server Error'), 500))
        except:
            # triggered when the custom script fails
            app.logger.error("Error: the script returned an error")
            return abort(make_response(jsonify(message='Internal Server Error'), 500))

        if type(result) == bool:
            response = bool_response(result)
        else:
            if not result.empty:
                response = file_response(result, script_name)
            else:
                response = abort(make_response(
                    jsonify(message='No Data'), 200))
    else:
        response = security(gcfp_token)
    return response


def security(gcfp_token):
    ''' Checks we have a gcfp_token that matches the one set in the environment variable '''
    if os.environ.get('GCFP_TOKEN') is not None:
        set_gcfp_token = os.environ.get('GCFP_TOKEN')
    else:
        app.logger.error("Forbidden: gcfp_token not configured")
        return abort(make_response(jsonify(message='Forbidden'), 403))

    if gcfp_token != set_gcfp_token:
        app.logger.error("Forbidden: gcfp_token incorrect")
        return abort(make_response(jsonify(message='Forbidden'), 403))
    else:
        return True


def launch_script(script_name, script_args):
    ''' Launches a specific script '''
    if __name__ == 'functions.main':
        script_path = 'functions.scripts.' + script_name
    else:
        script_path = 'scripts.' + script_name

    custom_script = import_module(script_path)

    return custom_script.run(script_args)  # type: ignore


def file_response(df, script_name):
    ''' Preps a DataFrame in a CSV response'''
    response = make_response(df.to_csv(index=False, float_format='%.6f'))
    response.headers['Content-Disposition'] = 'attachment; filename=export_{}.csv' . format(
        script_name)
    response.headers['Content-Type'] = 'text/csv'
    return response


def bool_response(bool):
    ''' Boolean response '''
    response = make_response(jsonify(bool), 200)

    return response
