import os
import sys
import tkinter as tk

import gobject
import gst

def on_sync_message(bus, message, window_id):
    if not message.structure is None:
        if message.structure.get_name() == 'prepare-xwindow-id':
            image_sink = message.src
            image_sink.set_property('force-aspect-ratio', True)
            image_sink.set_xwindow_id(window_id)

gobject.threads_init()

window = tk.Tk()
window.geometry('500x400')

video = tk.Frame(window, bg='#000000')
video.pack(side=tk.BOTTOM, anchor=tk.S, expand=tk.YES, fill=tk.BOTH)

window_id = video.winfo_id()

player = gst.element_factory_make('playbin2', 'player')
player.set_property('video-sink', None)
player.set_property('uri', 'file://%s' % (os.path.abspath("C:/Users/24707/InsidersProjects/Python/Thesis/Videos/Right.mp4")))
player.set_state(gst.STATE_PLAYING)

bus = player.get_bus()
bus.add_signal_watch()
bus.enable_sync_message_emission()
bus.connect('sync-message::element', on_sync_message, window_id)

window.mainloop()