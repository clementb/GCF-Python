# GCF-Python

This utility is a simple tool that allows running Google Cloud Functions using the Python runtime via a local Flask app. You can then deploy the function *as-is* to Google Cloud.

## What it's for

It's mostly a prototyping utility used to interact with other APIs or perform light data transformations. Its authentication method should not be used alone if you're running your Cloud Functions in production ([read more](https://cloud.google.com/functions/docs/securing/authenticating)).

The Functions created with this utility can return a Pandas DataFrame or a boolean, and can, therefore, be used to run simple tests or retrieve and format data for basic use cases.

Don't forget limitations around [Cloud Functions](https://cloud.google.com/functions/docs/resources).

## Prepare your Python environment on Ubuntu

1. Use `venv` to setup a Python 3.7 environment
2. Install `Pandas`, `Flask`
3. `flask run`

### Run a function on your local environment

Before running `flask run`, make sure you set the relevant environment variables.

#### Flask

- `export FLASK_APP=server.py` 
- `export FLASK_ENV=development`
 
#### Your function 

- `export GCFP_TOKEN='securetoken'`
    - `securetoken` is a required value that you will pass in your Cloud Function http calls. You can generate one using `openssl rand -base64 256`. Note that this value is required even if your Cloud Function requires authentication at the Google Cloud level.

## Basic API call

Url encode `securetoken` and call:

`http://127.0.0.1:5000/?gcfp_token={{urlencoded_securetoken}}&param1=value1&param2=value2&script_name=demo_script`

### Load different scripts

One thing you can do, is re-use the same function to invoke different custom scripts.

1. Create your custom script using `demo_script.py` as a template
2. Call that script my passing its name in your call's `script_name` parameter

## Deploy a function to gcloud

- Make sure to be in `/functions` and have `gcloud` installed when running this command (see [gcloud quick start](https://cloud.google.com/sdk/docs/quickstart-linux)).
- This command is using some defaults, be careful, it has `--allow-unauthenticated` and you should remove this flag if you want to rely on Google Cloud authentication

`gcloud functions deploy {{function_name}} --entry-point main --runtime python37 --trigger-http --allow-unauthenticated --region europe-west2 --set-env-vars=GCFP_TOKEN='{{securetoken}}' --memory=128MB --timeout=120`

# Errors

Errors will show in your CLI with more details. The API returns generic HTTP codes

- `403 Forbidden`: This is likely due to using the wrong gcfp_token, not using a gcfp_token, or having no token environment variable set for that function
- `500 Internal Server Error`: This is likely due to an error loading the custom script


# Limitations

- Supports only one gcfp token
- Limited use cases