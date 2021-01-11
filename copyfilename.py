# This Python caja extension only consider files/folders with a symlink
# upper/lower case name. For those, the following is featured:
# - an emblem on the icon,
# - contextual menu entry.
# - a list view "Symlink" column,
# - a property page,
# - A top area widget.

import os
import pickle
import urllib

from gi.repository import Caja, Gdk, GObject, Gtk
from gi.repository.Gio import FileType


class CopyFileName(
    GObject.GObject,
    Caja.InfoProvider,
    Caja.ColumnProvider,
    Caja.MenuProvider,
    Caja.PropertyPageProvider,
    Caja.LocationWidgetProvider,
):

    emblem = "favorite-symbolic.symbolic"  # Use one of the stock emblems.

    def _copy(self, _, cajafile):
        path = cajafile.get_location().get_path()
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(path, -1)

    # Caja.MenuProvider (right-click on file).
    def get_file_items(self, window, cajafiles):
        menuitems = []
        if len(cajafiles) == 1:
            for cajafile in cajafiles:
                menuitem = Caja.MenuItem(
                    name="CopyFileName::FileMenu",
                    label="Copy Path",
                    tip="",
                    icon="",
                )
                menuitem.connect("activate", self._copy, cajafile)
                menuitems.append(menuitem)

        return menuitems
