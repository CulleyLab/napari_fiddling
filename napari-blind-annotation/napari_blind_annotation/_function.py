import pathlib
from magicgui import magicgui, magic_factory

import napari

def my_widget():
    @magicgui(
        auto_call=True,
        raw_dir={"widget_type": 'FileEdit', 'mode': 'd'},
        annotated_dir={"widget_type": 'FileEdit', 'mode': 'd'},
        do_rotation={"widget_type": 'PushButton', 'text': 'Load and transform random image'}
    )
    def widget(raw_dir, annotated_dir, do_rotation):
        print('something changed')

    @widget.do_rotation.changed.connect
    def do_something(event=None):
        raw_dir = pathlib.Path(widget.raw_dir.value)
        # select a random file


        print(widget.raw_dir.value)

    return widget


viewer = napari.Viewer()
viewer.window.add_dock_widget(my_widget())

napari.run()

