from light import Light
from material import Material
from camera import Camera
import transform
import vectors

__all__ = ['Light', 'Material', 'Camera', 'transform', 'vectors', 'resource_path']


def resource_path(file_name):
    import os
    path = os.path.abspath(os.path.dirname(__file__))
    relpath = '../icons/' + str(file_name)
    path = os.path.join(path, relpath)
    return path

