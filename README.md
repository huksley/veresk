# Veresk

## Introduction

This app gives you ability to create different images of fractals.

What is a fractal? It is a picture produced my mathematical expression which have recursive nature with unlimited zooming capabilities.

As image generation controlled by expression, changing the expression even in the slighest manner will result in a sometimes complete different image.

See [Wikipedia](https://en.wikipedia.org/wiki/Fractal) page for more introduction.

## Example

![](app/static/preview.png)

This example is a [Julia set](https://en.wikipedia.org/wiki/Julia_set) generated with base complex number `c = -0.37 + 0.6*i`

Julia set is a subset of well-known [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set).

## Requirements

This app requires MongoDB instance available (running in the docker or in the cloud) by setting MONGO_URI environment variable:

```
MONGO_URI=mongodb://localhost/test
```

## Running locally

You need to have Python 3.7 installed.

```
pip install pipenv
pipenv install
MONGO_URI=mongodb://localhost/test FLASK_SECRET_KEY=123 GITHUB_OAUTH_CLIENT_ID= GITHUB_OAUTH_CLIENT_SECRET= CACHE_BUCKET= pipenv run python -m app
```

Your app will be available at http://localhost:8080

## Deploying

This project uses [chamber CLI](https://github.com/segmentio/chamber), [AWS](https://aws.amazon.com/), [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and [Serverless framework](https://serverless.com) to deploy to the cloud. This result in a highly available, cost-effective, secure and environment to host and serve hobby projects.

### Configure MongoDB instance

Create MongoDB instance using cloud service (for example MongoDB atlas).

You will get URL in the form of:

```
mongodb+srv://username:password@server.mongodb.net/db
```

### Create AWS account in the cloud

The way this app uses AWS services, hosting this app will cost you 0.1$ monthly or less, depending on the traffic. Make sure you are protecting your AWS account as the malicious actions of other parties or mistakes can result in a large bill. Read more [here](https://medium.com/@ruslanfg/wip-introduction-to-aws-665d4e9af0c2) about getting started in AWS.

### Configuring other resources in the cloud

To run successfully full fledged version of the app, number of parameters needs to be set using AWS Parameter Store as `/veresk/NAME_OF_VARIABLE` key. Encrypt using default key (do not use custom KMS key).

* MONGO_URI - URL to previously configured MongoDB instance
* FLASK_SECRET_KEY - Private key for your Flask app
* GITHUB_OAUTH_CLIENT_ID - Credentials for GitHub login (create app in Developer settings)
* GITHUB_OAUTH_CLIENT_SECRET - Credentials for GitHub login
* CACHE_BUCKET - Create and give access to S3 bucket to store image cache

### Deploy instance to the cloud

You need to have NodeJS 11+, python 3.7+, pipenv and NPM installed.

```
npm install
pip install pipenv
pipenv install
pipenv run deploy
```

## Licenses

- See LICENSE.md, with the exception of:
- `app/plot.py`, `def julia`: (C) Tom Roelandts, https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib
- `app/static/icon.svg`: fractal by Bohdan Burmich from the Noun Project (see https://thenounproject.com/term/fractal/224056/)

## Links

- https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/
- https://numpy.org/doc/stable/user/quickstart.html
- https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
- https://github.com/lovasoa/mandelbrot
- https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib
- https://www.researchgate.net/publication/242295595_Visualising_Infinity_on_a_Mobile_Device#pf2
- https://en.wikipedia.org/wiki/Julia_set
