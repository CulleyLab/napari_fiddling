import numpy as np
import napari
import time
from napari.utils.events import Event


viewer = napari.Viewer()
layer = viewer.add_image(np.random.random((512, 512)))
time_list = []

@viewer.bind_key('s')
def show_total_time(viewer):
    total_time = 0
    for t in time_list:
        total_time += t
    print(total_time)

def get_time(t_start, t_stop):
    print(f'mouse drag lasted {t_stop-t_start}')
    time_list.append(t_stop-t_start)
    return 

def my_callback(event):
    if isinstance(event.value, napari.layers.Labels):
        layer = viewer.layers['Labels']

        @layer.mouse_drag_callbacks.append
        def time_drag(layer, event):
            if isinstance(layer, napari.layers.Labels):
                t_start = time.time()
                yield
                while event.type == 'mouse_move':
                    # the yield statement allows the mouse UI to keep working while
                    # this loop is executed repeatedly
                    yield
                get_time(t_start, time.time())
        

viewer.layers.events.inserted.connect(my_callback)
napari.run()