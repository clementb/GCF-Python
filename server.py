#!/usr/bin/env python3

from flask import Flask, request
from functions import main as function

# This file should not be deployed to gcloud! cd to /functions to deploy

app = Flask(__name__)


@app.route('/', methods=['GET'])
def functions():
    ''' simulates a call to a cloud function '''
    return function.main(request)


if __name__ == '__main__':
    app.run()
