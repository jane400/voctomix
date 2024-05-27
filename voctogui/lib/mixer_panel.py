from gi.repository import Gtk

from .helpers import with_ui_path

@Gtk.Template(filename=with_ui_path('mixer-panel.ui'))
class MixerPanel(Gtk.Box):
    __gtype_name__ = "VoctoMixerPanel"

    audio_box = Gtk.Template.Child()

    toolbar_preview_composite: Gtk.Toolbar = Gtk.Template.Child()
    toolbar_preview_a: Gtk.Toolbar = Gtk.Template.Child()
    toolbar_preview_b: Gtk.Toolbar = Gtk.Template.Child()
    toolbar_preview_mod: Gtk.Toolbar = Gtk.Template.Child()

    frame_preview_b: Gtk.Frame = Gtk.Template.Child()
    box_preview_modify: Gtk.Frame = Gtk.Template.Child()

    preset_box: Gtk.Box = Gtk.Template.Child()
    preset_toolbar: Gtk.Toolbar = Gtk.Template.Child()

    box_insert: Gtk.Box = Gtk.Template.Child()
    insert_store: Gtk.ListStore = Gtk.Template.Child(name="insert-store")
    inserts: Gtk.ComboBox = Gtk.Template.Child()
    insert: Gtk.CheckButton = Gtk.Template.Child()
    update_inserts: Gtk.Button = Gtk.Template.Child(name="update-inserts")
    insert_auto_off = Gtk.CheckButton = Gtk.Template.Child(name="insert-auto-off")

    overlay_description = Gtk.Label = Gtk.Template.Child(name="overlay-description")

    toolbar_mix: Gtk.Toolbar = Gtk.Template.Child()
    toolbar_mix1: Gtk.Toolbar = Gtk.Template.Child()

    # TODO: split this out
    toolbar_blinder: Gtk.Toolbar = Gtk.Template.Child()
    stream_live: Gtk.RadioToolButton = Gtk.Template.Child()
    stream_blind: Gtk.RadioToolButton = Gtk.Template.Child()
    box_blinds: Gtk.Frame = Gtk.Template.Child()

