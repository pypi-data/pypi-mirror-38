#!/home/athena/anaconda3/bin/python3.7
from PIL import Image
import cv2
import numpy as np
from svgpathtools import svg2paths
from tkinter import END
import mpmath as mp
import warnings

mp.mp.dps = 40


def get_coeffs_from_image(
        filename: str, *,
        min_coeff: int = -3,
        max_coeff: int = 3,
        textwidget=None,
        out_buffer=None) -> dict:
    if filename[-4:] == ".svg":
        paths, _ = svg2paths(filename)

        if len(paths) < 1:
            raise ValueError(".svg image does not contain path data")

        svg_poly1ds = []

        for seg in paths[0]:
            svg_poly1ds.append(seg.poly())
        del seg

        poly_coeffs = []

        for svg_poly1d in svg_poly1ds:
            poly_coeffs.append(np.flip(svg_poly1d.c.conjugate()))
        del svg_poly1d

        array_deg_arrays = []
        for coeffs_array in poly_coeffs:
            new_array = np.asarray(coeffs_array, dtype=np.complex128)
            for i in range(len(coeffs_array)):
                new_array[i] *= ((1/(2*np.pi)) * (1/len(poly_coeffs))) ** i
            del i
            array_deg_arrays.append(new_array)
        del coeffs_array

        polynomials = []
        for deg_array in array_deg_arrays:
            polynomials.append(MPMathPolynomial(deg_array))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fourier_coeffs = {}
            for i in range(min_coeff, max_coeff + 1):
                if textwidget:
                    textwidget.master.update_idletasks()
                coeff = get_fourier_coeff(
                        polynomial_piecewise, i, polynomials)
                if textwidget:
                    textwidget.insert(END, f"Fourier coeff. of index {i} "
                                      f"is {complex(coeff):.7f}\n")
                    textwidget.master.update_idletasks()
                if out_buffer:
                    print(f"Fourier coeff. of index {i} "
                          f"is {complex(coeff):.7f}", file=out_buffer)
                fourier_coeffs[i] = complex(coeff)
            del i

        return fourier_coeffs
    else:
        open_cv_image = np.array(Image.open(filename).convert('RGB'))
        imgray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(imgray, 0, 255)
        _, contours, *__ = cv2.findContours(
                edges,
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)
        point_arrays = []
        for contour in contours:
            point_arrays = point_arrays + list(contour)
        points = []
        for point_array in point_arrays:
            points = points + list(point_array)
        points = [list(point) for point in points]
        complex_points = [complex(point[0], point[1]) for point in points]
        polynomials = []
        for i in range(0, len(complex_points) - 1):
            deg_array = [complex_points[i],
                         complex_points[i + 1] - complex_points[i]]
            polynomials.append(MPMathPolynomial(deg_array))
            del deg_array
        del i

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fourier_coeffs = {}
            for i in range(min_coeff, max_coeff + 1):
                if textwidget:
                    textwidget.master.update_idletasks()
                coeff = get_fourier_coeff(
                        polynomial_piecewise, i, polynomials)
                if textwidget:
                    textwidget.insert(END, f"Fourier coeff. of index {i} "
                                      f"is {complex(coeff):.7f}\n")
                    textwidget.master.update_idletasks()
                if out_buffer:
                    print(f"Fourier coeff. of index {i} "
                          f"is {complex(coeff):.7f}")
                fourier_coeffs[i] = complex(coeff)
            del i

        return fourier_coeffs


class MPMathPolynomial:
    def __init__(self, deg_array):
        self.deg_array = deg_array

    def __call__(self, x):
        output = mp.mpc(0, 0)
        for i in range(len(self.deg_array)):
            mp_coeff = mp.mpc(self.deg_array[i].real,
                              self.deg_array[i].imag)
            output += mp_coeff * (x ** i)
        return output


def polynomial_piecewise(x, polys):
    num_polys = len(polys)
    for i in range(num_polys):
        if i*2*mp.pi/num_polys <= x < (i+1)*2*mp.pi/num_polys:
            return polys[i](x - i*2*mp.pi/num_polys)
    del i
    return 0


def get_fourier_coeff(function, index, polys):
    def get_integrand(func, n):
        return lambda t: mp.exp(t*(-1j)*n)*func(t, polys)
    return (1/(2*mp.pi))*mp.quad(
            get_integrand(function, index),
            mp.linspace(0, 2*mp.pi, 4))


def fourierfunc(t, coeffs):
    output = 0
    for index, coeff in coeffs.items():
        output += coeff*np.exp(1j*index*t)
    del index
    del coeff
    return output


if __name__ == "__main__":
    import sys
    coeffs = get_coeffs_from_image("dragon.svg", out_buffer=sys.stdout)
    pass
