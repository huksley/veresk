import io
import random
from flask import Response, Blueprint
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('agg')

bp = Blueprint('plot', __name__, url_prefix='/plot')


@bp.route('/example.png')
def example_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@bp.route('/fractals.png')
def fractals_png():
    fig = julia(480, 320)
    return Response(fig.getvalue(), mimetype='image/png')


def julia(m, n):
    """Draws Julia fractal, see https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib"""
    s = 300  # Scale.
    x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
    y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))
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
    plt.close
    bytes_image.seek(0)
    return bytes_image


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
