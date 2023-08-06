from light import Light
from material import Material
from camera import Camera
import transform
import vectors

__all__ = ['Light', 'Material', 'Camera', 'transform', 'vectors', 'resource_path']


def resource_path(file_name):
    import os
    if os.path.isdir('icons'):
        path = 'icons/' + str(file_name)
    else:
        path = 'lldbvis/icons/' + str(file_name)
    return path

