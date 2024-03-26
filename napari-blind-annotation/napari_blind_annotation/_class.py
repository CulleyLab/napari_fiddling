import pathlib

import numpy as np
from magicgui import magicgui, magic_factory
from napari_plugin_engine import napari_hook_implementation
from napari_tools_menu import register_dock_widget
from magicgui.widgets import FileEdit, PushButton
from random import choice
from glob import glob
from tifffile import imread
import os
import napari
from skimage.transform import rotate
from numpy import flipud, fliplr

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return [magic_factory(), RandomFlipRotate]
@register_dock_widget(menu="blind annotation")
class RandomFlipRotate():
    visited_files = []
    print

    def __init__(self, viewer: "napari.viewer.Viewer",
                 raw_images_dir: str = 'raw_images', annotated_dir: str = 'annotated_images'):
        self._viewer = viewer

        # create path selection fields
        self._raw_fileedit = FileEdit(
            mode='d'
        )
        self._annotated_fileedit = FileEdit(
            mode='d'
        )

        # create button to load and rotate
        self._random_rotate_button = PushButton(
            label="Load random image and transform"
        )

        # create button to untransform and save
        self._untransform_save_button = PushButton(
            label="Untransform labels and save"
        )

        # connect callbacks
        # TODO: do I need to connect a callback for the FileEdit?

        super().__init__(
            widgets=[
                self._raw_fileedit,
                self._annotated_fileedit,
                self._random_rotate_button,
                self._untransform_save_button
                ])

napari_experimental_provide_dock_widget()