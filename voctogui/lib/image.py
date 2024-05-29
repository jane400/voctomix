from gi.repository import Gtk, GObject

from .helpers import with_ui_path

@Gtk.Template(filename=with_ui_path('image.ui'))
class UiImage(Gtk.Image):
    """
    GTypeName: VoctoImage
    GPropeties:
      - path-file: str

    This is just here as a wrapper, so we can set the right path
    where the image should be loaded from, VoctoImage:path-file
    redirects to GtkImage:file.

    This uses a Gtk.Template for Cambalance, so it won't throw
    an error, as the class exists from a .ui point of view.
    """

    __gtype_name__ = "VoctoImage"

    _path_file: str

    @GObject.Property(type=str, nick="path-file")
    def path_file(self):
        """Read-write integer property."""

        return self._path_file

    @path_file.setter
    def path_file(self, value):
        self._path_file = value

        self.set_from_file(with_ui_path(self._path_file))