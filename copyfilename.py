from gi.repository import Caja, Gdk, GObject, Gtk


class CopyFileName(
    GObject.GObject,
    Caja.InfoProvider,
    Caja.ColumnProvider,
    Caja.MenuProvider,
    Caja.PropertyPageProvider,
    Caja.LocationWidgetProvider,
):

    emblem = "favorite-symbolic.symbolic"  # Use one of the stock emblems.

    @staticmethod
    def _copy(_, cajafile):
        path = cajafile.get_location().get_path()
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(path, -1)

    # Caja.MenuProvider (right-click on file).
    def get_file_items(self, _window, cajafiles):
        menuitems = []
        if len(cajafiles) == 1:
            for cajafile in cajafiles:
                menuitem = Caja.MenuItem(
                    name="CopyFileName::FileMenu",
                    label="Copy Path",
                    tip="",
                    icon="edit-copy",
                )
                menuitem.connect("activate", self._copy, cajafile)
                menuitems.append(menuitem)

        return menuitems
