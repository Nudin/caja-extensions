import os

from gi.repository import Caja, GObject, Gtk
from gi.repository.Gio import FileType


class Symlink(
    GObject.GObject,
    Caja.InfoProvider,
    Caja.ColumnProvider,
    Caja.MenuProvider,
    Caja.PropertyPageProvider,
    Caja.LocationWidgetProvider,
):
    @staticmethod
    def _file_is_symlink(cajafile):
        path = cajafile.get_location().get_path()
        if os.path.islink(path):
            return True
        return False

    @staticmethod
    def _file_is_in_symlink(cajafile):
        path = cajafile.get_location().get_path()
        if os.path.realpath(path) != path:
            return True
        return False

    @staticmethod
    def _read_symlink(cajafile):
        return os.path.realpath(cajafile.get_location().get_path())

    def _show(self, _, cajafile):
        window = Gtk.MessageDialog(
            title=cajafile.get_name(),
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Target of symlink:",
        )
        window.format_secondary_text(self._read_symlink(cajafile))
        window.get_message_area().get_children()[1].set_selectable(True)
        window.run()
        window.destroy()

    def _open(self, _, cajafile):
        realpath = self._read_symlink(cajafile)
        if cajafile.get_file_type() == FileType.DIRECTORY:
            goto_dir = realpath
        else:
            goto_dir = os.path.dirname(realpath)
        os.system("caja '" + goto_dir + "' &")

    # Caja.MenuProvider (right-click on file).
    def get_file_items(self, _window, cajafiles):
        menuitems = []
        if len(cajafiles) == 1:
            for cajafile in cajafiles:
                if self._file_is_symlink(cajafile):
                    menuitem = Caja.MenuItem(
                        name="Symlink::FileMenu",
                        label="Symlink: Show real path",
                        tip="",
                        icon="info",
                    )
                    menuitem.connect("activate", self._show, cajafile)
                    menuitems.append(menuitem)

                    menuitem_open = Caja.MenuItem(
                        name="Symlink::FileMenu2",
                        label="Symlink: Open real folder",
                        tip="",
                        icon="folder-open",
                    )
                    menuitem_open.connect("activate", self._open, cajafile)
                    menuitems.append(menuitem_open)

        return menuitems

    # Caja.LocationWidgetProvider (bar on top, when inside directory).
    def get_widget(self, uri, _window):
        cajafile = Caja.FileInfo.create_for_uri(uri)
        if not self._file_is_in_symlink(cajafile):
            return None
        label = Gtk.Label("In symlink directory " + self._read_symlink(cajafile))
        label.set_selectable(True)
        label.show()
        return label
