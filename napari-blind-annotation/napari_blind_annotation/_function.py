import pathlib

import numpy as np
from magicgui import magicgui, magic_factory
from random import choice
from glob import glob
from tifffile import imread
import os
import napari
from skimage.transform import rotate
from numpy import flipud, fliplr

global visited_files
def my_widget():
    @magicgui(
        auto_call=False,
        call_button="Save and move to next image",
        raw_dir={"widget_type": 'FileEdit', 'mode': 'd'},
        annotated_dir={"widget_type": 'FileEdit', 'mode': 'd'},
        do_rotation={"widget_type": 'PushButton', 'text': 'Load and transform random image'}
    )
    def widget(raw_dir, annotated_dir, do_rotation, save_labels):
        # TODO: DON'T FORGET YOU NEED TO REVERSE THE ROTATION AND FLIPPING!!!!!!!!!

        print("we ran")
        return


    @widget.do_rotation.changed.connect
    def do_something(event=None):

        # get raw path
        raw_path = str(widget.raw_dir.value)
        raw_path_as_list = raw_path.split(os.sep)
        raw_path = pathlib.Path(raw_path)

        # path names for saving analysed data
        save_path = str(widget.annotated_dir.value)

        found_analysis_file = False

        while found_analysis_file == False:

            # read in a file that hasn't been analysed yet
            if len(visited_files) == 0:
                file = choice(glob(f'{raw_path}/**/*'))
            else:
                while file in visited_files:
                    file = choice(glob(f'{raw_path}/**/*'))

            file_as_list = file.split(os.sep)

            # want to find intermediate folders between raw path and file
            depth_raw = len(raw_path_as_list)
            depth_file = len(file_as_list)

            target_save_path = pathlib.Path(save_path)
            for dir in file_as_list[depth_raw:depth_file]:
                target_save_path = target_save_path.joinpath(pathlib.Path(dir))

            # check if an analysed file already exists at this location
            if target_save_path.exists():
                visited_files.append(file)
                print(f'{file} already analysed!')
            else:
                found_analysis_file = True

        # load raw file
        raw = imread(file)

        # apply random rotation
        angle = choice([0, 90, 180, 270])
        print(angle)
        rotated = rotate(raw, angle)

        # apply random vertical flip
        vertical_flip = choice([0, 1])
        if vertical_flip == 1:
            print('v flipped!')
            v_flipped = flipud(rotated)
        else:
            v_flipped = rotated

        # apply random horizontal flip
        horizontal_flip = choice([0, 1])
        if horizontal_flip == 1:
            print('h flipped!')
            h_flipped = fliplr(v_flipped)
        else:
            h_flipped = v_flipped

        # now want to add h_flipped as an image layer
        viewer.add_image(data=h_flipped, name='data')

        # add labels layer
        viewer.add_labels(data=np.zeros(h_flipped.shape, dtype='uint16'), name='labels', opacity=0.4)

    return widget

viewer = napari.Viewer()
viewer.window.add_dock_widget(my_widget())
visited_files = []
napari.run()

