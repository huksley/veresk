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

## Running

```
pip install pipenv
pipenv install
pipenv run app
```

## Licenses

- See LICENSE.md, with the exception of:
- `app/plot.py, `def julia`: (C) Tom Roelandts, https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib
- `app/static/icon.svg`: fractal by Bohdan Burmich from the Noun Project (see https://thenounproject.com/term/fractal/224056/)

## Links

- https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/
- https://numpy.org/doc/stable/user/quickstart.html
- https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
- https://github.com/lovasoa/mandelbrot
- https://tomroelandts.com/articles/how-to-compute-colorful-fractals-using-numpy-and-matplotlib
- https://www.researchgate.net/publication/242295595_Visualising_Infinity_on_a_Mobile_Device#pf2
- https://en.wikipedia.org/wiki/Julia_set
