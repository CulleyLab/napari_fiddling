import pathlib
from magicgui import magicgui, magic_factory

import napari

def _load_transform(widget):
    @widget.do_rotation.clicked.connect
    def load_transform():
        print('button pressed, bebe')
        print(widget.raw_dir.value)

@magicgui(
    auto_call=True,
    raw_dir={"widget_type": 'FileEdit', 'mode': 'd'},
    annotated_dir={"widget_type": 'FileEdit', 'mode': 'd'},
    do_rotation={"widget_type": 'PushButton', 'text': 'Load and transform random image'}
)
def blah(raw_dir, annotated_dir, do_rotation):
    print(do_rotation)
    print(raw_dir)
    print('blah')

# @magicgui(fn={'mode': 'd'}, call_button='Store raw image parent directory', labels=False)
# def raw_folder_widget(fn=pathlib.Path.home()):
#     return
#
# @magicgui(fn={'mode': 'd'}, call_button='Store annotated images directory', labels=False)
# def annotated_folder_widget(fn=pathlib.Path.home()):
#     return

viewer = napari.Viewer()
viewer.window.add_dock_widget(blah)

# viewer.window.add_dock_widget(raw_folder_widget, area='right')
# viewer.window.add_dock_widget(annotated_folder_widget, area='right')

napari.run()
#
# print(raw_folder_widget.fn.value)
# print(annotated_folder_widget.fn.value)
