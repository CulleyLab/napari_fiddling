import pathlib

import numpy as np
from magicgui import magicgui
from random import choice
from glob import glob
from tifffile import imread, imwrite
import os
import napari
from numpy import flipud, fliplr, rot90

global visited_files

def blind_annotation_widget():
    @magicgui(
        auto_call=False,
        call_button="Save and move to next image",
        raw_dir={"widget_type": 'FileEdit', 'mode': 'd'},
        annotated_dir={"widget_type": 'FileEdit', 'mode': 'd'},
        do_rotation={"widget_type": 'PushButton', 'text': 'Load and transform random image'}
    )
    def widget(raw_dir, annotated_dir, do_rotation):
        image_metadata = viewer.layers['data'].metadata
        horizontal_flip = image_metadata['horizontal_flip']
        vertical_flip = image_metadata['vertical_flip']
        angle = image_metadata['angle']
        target_save_path = image_metadata['target_save_path']

        label_layer = viewer.layers['labels']
        layer_data = label_layer.data

        # undo horizontal flip
        if horizontal_flip == 1:
            un_h_flipped = fliplr(layer_data)
        else:
            un_h_flipped = layer_data

        # undo vertical flip
        if vertical_flip == 1:
            un_v_flipped = flipud(un_h_flipped)
        else:
            un_v_flipped = un_h_flipped

        # undo rotation
        un_rotated = rot90(un_v_flipped, int(-angle/90))

        # debugging - add as a layer
        # viewer.add_labels(data=un_rotated.astype('uint16'), name='untransformed labels', opacity=0.4)

        # now just need to save it to corresponding location in annotated dir
        # let's just use tifffile because I actually cannot deal with napari.
        print(target_save_path)
        # check if directories exist
        if os.path.exists(os.path.dirname(target_save_path)) == False:
            os.makedirs(os.path.dirname(target_save_path))
            print('created directory!')

        imwrite(target_save_path, un_rotated)

        viewer.layers.clear()

        return


    @widget.do_rotation.changed.connect
    def get_random_image_do_rotation(event=None):

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

        print(f"let's analyse the file: {file}")
        # load raw file
        raw = imread(file)

        # apply random rotation
        angle = choice([0, 90, 180, 270])
        print(angle)
        rotated = rot90(raw, int(angle/90))

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
        viewer.add_image(data=h_flipped, name='data', metadata={
            'angle':angle,
            'vertical_flip':vertical_flip,
            'horizontal_flip':horizontal_flip,
            'target_save_path':target_save_path
        })


        # debugging for texting unrotation later
        #viewer.add_image(data=raw, name='before transform', visible=False)

        # add labels layer
        viewer.add_labels(data=np.zeros(h_flipped.shape, dtype='uint16'), name='labels', opacity=0.4)

    return widget


viewer = napari.Viewer()
viewer.window.add_dock_widget(blind_annotation_widget())
visited_files = []
napari.run()

