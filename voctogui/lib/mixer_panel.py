from gi.repository import Gtk

from .helpers import with_ui_path

@Gtk.Template(filename=with_ui_path('mixer-panel.ui'))
class MixerPanel(Gtk.Box):
    __gtype_name__ = "VoctoMixerPanel"

