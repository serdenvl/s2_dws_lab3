import numpy
from PIL import Image

import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.axes

from enum import Enum, auto


class Task1Function(Enum):
    sin = numpy.sin
    cos = numpy.cos


class Task1Orientation(Enum):
    horizontal = auto()
    vertical = auto()


def handle_image(image: Image.Image, function: Task1Function, orientation: Task1Orientation,
                 period: float, period_is_percentage: bool) -> Image.Image:
    def handle_matrix(matrix: numpy.ndarray, is_horizontal: bool) -> numpy.ndarray:
        if not is_horizontal:
            t = lambda m: numpy.transpose(m, (1, 0, -1))
            return t(handle_matrix(t(matrix), True))

        height, width = matrix.shape[:2]
        arg_matrix = numpy.arange(width).reshape((1, -1))  # [[0 1 2 ...]]
        arg_matrix = numpy.repeat(arg_matrix, height, axis=0)  # [[0 1 2 ...] [0 1 2 ...] ...]

        period_ = period if not period_is_percentage else period*width/100

        f_matrix = function.value(arg_matrix * 2 * numpy.pi / period_)
        zeroize = numpy.vectorize(lambda x: x if x > 0 else 0, otypes=[f_matrix.dtype])
        
        p_matrix = zeroize(+f_matrix)
        n_matrix = zeroize(-f_matrix)

        for i in (0, 1, 2):
            matrix[:, :, i] += (1-matrix[:, :, i])*p_matrix
            matrix[:, :, i] -= (matrix[:, :, i]-0)*n_matrix
        return matrix

    image = numpy.asarray(image.convert('RGB')) / 255
    image = handle_matrix(image, orientation == Task1Orientation.horizontal)
    image = (image * 255).astype(numpy.uint8)

    return Image.fromarray(image)


def color_histogram(file_path, *images) -> Image.Image:
    def image_to_data(image):
        return numpy.asarray(image.convert('RGB')).reshape((-1, 3))

    datas = map(image_to_data, images)

    fig = pyplot.Figure()
    for (i, d) in enumerate(datas):
        for c in (0, 1, 2):
            sub = fig.add_subplot(3, len(images), 1 + i + c * len(images))

            d: numpy.ndarray
            sub: matplotlib.axes.Axes

            sub.set_xlim(0, 255)
            sub.set_ylim(0, d.shape[0])
            sub.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(d.shape[0]))
            sub.hist(d[:, c], color=('red', 'green', 'blue')[c], histtype='barstacked')

    fig.savefig(file_path)
    return Image.open(file_path)
