import pathlib

import numpy as np
from magicgui import magicgui
from random import choice
from glob import glob
from tifffile import imread, imwrite
import os
import napari
from numpy import flipud, fliplr, rot90

global all_image_files
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

    @widget.raw_dir.changed.connect
    def update_all_files_list():
        self = widget
        if not hasattr(self, 'all_image_files'):
            self.all_image_files = []

        # wipe previous list of files
        self.all_image_files = []

        # walk through directory
        for root, dirs, files in os.walk(widget.raw_dir.value):
            for file in files:
                if file.endswith(".tif"):
                    widget.all_image_files.append(os.path.join(root, file))

        print(f'there are {len(self.all_image_files)} tif images in this directory')
        return widget

    @widget.annotated_dir.changed.connect
    def update_unanalysed_files_list():
        self = widget
        if not hasattr(self, 'unanalysed_files'):
            self.unanalysed_files = []

        # walk through annotated directory
        analysed_files_list = []
        save_path = widget.annotated_dir.value

        for root, dirs, files in os.walk(widget.annotated_dir.value):
            for file in files:
                if file.endswith(".tif"):
                   analysed_files_list.append(os.path.join(root, file))

        # now, want to map analysed files to corresponding raw data path
        unanalysed_image_list = widget.all_image_files.copy()

        # get path depth of raw dir
        depth_images_path = len(str(widget.raw_dir.value).split(os.sep))

        for image_file in widget.all_image_files:

            # create equivalent analysed file path
            target_annotated_path = make_target_save_path(widget, image_file)

            # loop through already analysed and see if there's a match
            for annotated_file in analysed_files_list:
                if str(annotated_file) == str(target_annotated_path):
                    unanalysed_image_list.remove(image_file)
                    break

        print(f'{len(analysed_files_list)} images were already analysed.')
        print(f'{len(unanalysed_image_list)} images need to be analysed.')
        # update attribute
        widget.unanalysed_files = unanalysed_image_list

        return widget

    @widget.do_rotation.changed.connect
    def get_random_image_do_rotation(event=None):

        # select random file from unanalysed list and remove it
        file = choice(widget.unanalysed_files)
        widget.unanalysed_files.remove(file)
        print(f'{len(widget.unanalysed_files)} remain unanalysed.')

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
            'target_save_path':make_target_save_path(widget, file)
        })


        # debugging for texting unrotation later
        #viewer.add_image(data=raw, name='before transform', visible=False)

        # add labels layer
        viewer.add_labels(data=np.zeros(h_flipped.shape, dtype='uint16'), name='labels', opacity=0.4)

    return widget

def make_target_save_path(widget, file):
    # get folder depth of raw path
    depth_images_path = len(str(widget.raw_dir.value).split(os.sep))
    file_as_list = file.split(os.sep)

    target_save_path = pathlib.Path(widget.annotated_dir.value)
    for intermediate_dir in file_as_list[depth_images_path:len(file_as_list) + 1]: # why the +1
        target_save_path = target_save_path.joinpath(pathlib.Path(intermediate_dir))

    return target_save_path


viewer = napari.Viewer()
viewer.window.add_dock_widget(blind_annotation_widget())
all_image_files = []
visited_files = []
napari.run()

