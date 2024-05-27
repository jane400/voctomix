from gi.repository import Gtk

from .helpers import with_ui_path

@Gtk.Template(filename=with_ui_path('ports-window.ui'))
class PortsWindow(Gtk.Box):
    __gtype_name__ = "VoctoInfoPortsWindow"
    
    ports_store: Gtk.ListStore = Gtk.Template.Child()
    ports_scroll: Gtk.ScrolledWindow = Gtk.Template.Child()
    ports_title: Gtk.Label = Gtk.Template.Child()



@Gtk.Template(filename=with_ui_path('queue-window.ui'))
class QueueWindow(Gtk.Box):
    __gtype_name__ = "VoctoInfoQueueWindow"

    queue_store: Gtk.ListStore = Gtk.Template.Child()
    queue_scroll: Gtk.ScrolledWindow = Gtk.Template.Child()

