"""Fractal drawing primitives"""
import io
from flask import Response, Blueprint
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('agg')

bp = Blueprint('plot', __name__, url_prefix='/plot')

@bp.route('/fractals.png')
def fractals_png():
    """Create example fractals"""
    fig = julia(480, 320)
    return Response(fig.getvalue(), mimetype='image/png')

# pylint: disable=invalid-name

def julia(m, n):
    """Draws Julia fractal, see example in
    https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib"""
    scale = 300  # Scale.
    x = np.linspace(-m / scale, m / scale, num=m).reshape((1, m))
    y = np.linspace(-n / scale, n / scale, num=n).reshape((n, 1))
    Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    C = np.full((n, m), -0.42 + 0.6j)
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