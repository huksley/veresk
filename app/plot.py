"""Fractal drawing primitives"""
import io
import threading
import os
from flask import Response, Blueprint, request
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import boto3
import botocore

s3 = boto3.resource('s3')
lock = threading.Lock()
matplotlib.use('agg')

bp = Blueprint('plot', __name__, url_prefix='/plot')

# pylint: disable=invalid-name


@bp.route('/fractals.png')
def fractals_png():
    """Create fractal response from cache or newly generated image"""
    complex_real = float(request.args.get('complex_real', -0.42))
    complex_imaginary = float(request.args.get('complex_imaginary', 0.6))

    if os.environ["CACHE_BUCKET"] == "":
        try:
            binary = fractals_generate_png(complex_real, complex_imaginary)
        except ValueError as e:
            print("Failed to create", e)
            return ("Internal server error", 500)
        resp = Response(binary, mimetype='image/png')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Cache-Control'] = "public, max-age=31536000"
        return resp

    key = "cache/img" + str(complex_real) + "x" + \
        str(complex_imaginary) + ".png"
    print("Checking cache, bucket", os.environ["CACHE_BUCKET"], "key", key)
    try:
        s3.Object(os.environ["CACHE_BUCKET"], key).load()
        bucket = s3.Bucket(os.environ["CACHE_BUCKET"])
        obj = bucket.Object(key)
        print("Sending cached, bucket", os.environ["CACHE_BUCKET"], "key", key)
        resp = Response(io.BytesIO(
            obj.get()['Body'].read()), mimetype='image/png')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Cache-Control'] = "public, max-age=31536000"
        return resp
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            obj = s3.Object(os.environ["CACHE_BUCKET"], key)
            try:
                binary = fractals_generate_png(complex_real, complex_imaginary)
            except ValueError as e:
                print("Failed to create", e)
                return ("Internal server error", 500)
            obj.put(Body=binary)
            resp = Response(binary, mimetype='image/png')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Cache-Control'] = "public, max-age=31536000"
            return resp
        print("AWS error", e.response['Error']['Code'])
        return ("Internal server error", 500)


def fractals_generate_png(complex_real, complex_imaginary):
    """Generate fractal binary data"""
    m = 480*2
    n = 320*2
    print("Creating fractal, m", m, "n", n, "complex_real",
          complex_real, "complex_imaginary", complex_imaginary)
    with lock:
        fig = julia(m, n, complex_real, complex_imaginary)
    binary = fig.getvalue()
    return binary


def julia(m, n, complex_real, complex_imaginary):
    """Draws Julia fractal, see example in
    https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib"""
    scale = 600  # Scale.
    x = np.linspace(-m / scale, m / scale, num=m).reshape((1, m))
    y = np.linspace(-n / scale, n / scale, num=n).reshape((n, 1))
    Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    C = np.full((n, m), complex(complex_real, complex_imaginary))
    M = np.full((n, m), True, dtype=bool)
    N = np.zeros((n, m))
    for i in range(256):
        Z[M] = Z[M] * Z[M] + C[M]
        M[np.abs(Z) > 2] = False
        N[M] = i
    im = np.flipud(255 - N)
    fig = plt.figure()
    fig.set_size_inches(m / 100, n / 100)
    ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1)
    ax.set_xticks([])
    ax.set_yticks([])
    bytes_image = io.BytesIO()
    plt.imshow(im, cmap='hot')
    plt.savefig(bytes_image, format="png")
    plt.close()
    bytes_image.seek(0)
    return bytes_image
