from gi.repository import Gtk

from .helpers import with_ui_path

@Gtk.Template(filename=with_ui_path('widgetpreview.ui'))
class WidgetPreview(Gtk.DrawingArea):
    __gtype_name__ = "VoctoPreview"
