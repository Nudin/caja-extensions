import os
import pickle
import urllib

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

    emblem = "favorite-symbolic.symbolic"  # Use one of the stock emblems.

    def _file_is_symlink(self, cajafile):
        path = cajafile.get_location().get_path()
        if os.path.islink(path):
            return True
        return False

    def _file_is_in_symlink(self, cajafile):
        path = cajafile.get_location().get_path()
        if os.path.realpath(path) != path:
            return True
        return False

    def _read_symlink(self, cajafile):
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
    def get_file_items(self, window, cajafiles):
        menuitems = []
        if len(cajafiles) == 1:
            for cajafile in cajafiles:
                if self._file_is_symlink(cajafile):
                    menuitem = Caja.MenuItem(
                        name="Symlink::FileMenu",
                        label="Symlink: Show real path",
                        tip="",
                        icon="",
                    )
                    menuitem.connect("activate", self._show, cajafile)
                    menuitems.append(menuitem)

                    menuitem_open = Caja.MenuItem(
                        name="Symlink::FileMenu2",
                        label="Symlink: Open real folder",
                        tip="",
                        icon="",
                    )
                    menuitem_open.connect("activate", self._open, cajafile)
                    menuitems.append(menuitem_open)

        return menuitems

    # Caja.PropertyPageProvider implementation.
    #  def get_property_pages(self, cajafiles):
    #      pages = []
    #      if len(cajafiles) == 1:
    #          for cajafile in cajafiles:
    #              if self._file_is_in_symlink(cajafile):
    #                  page_label = Gtk.Label("Symlink")
    #                  page_label.show()
    #                  vbox = Gtk.VBox(homogeneous=False, spacing=4)
    #                  vbox.show()
    #                  name_label = Gtk.Label(cajafile.get_name())
    #                  name_label.show()
    #                  comment_label = Gtk.Label("Is a symlink (or in a symlink)")
    #                  comment_label.show()
    #                  path_label = Gtk.Label(self._read_symlink(cajafile))
    #                  path_label.set_selectable(True)
    #                  # path_label.select_region(0, 0)
    #                  path_label.show()
    #                  vbox.pack_start(name_label, False, False, 0)
    #                  vbox.pack_start(comment_label, False, False, 0)
    #                  vbox.pack_start(path_label, False, False, 0)
    #                  pages.append(
    #                      Caja.PropertyPage(
    #                          name="Symlink::PropertyPage", label=page_label, page=vbox
    #                      )
    #                  )

    #      return pages

    # Caja.LocationWidgetProvider (bar on top, when inside directory).
    def get_widget(self, uri, window):
        cajafile = Caja.FileInfo.create_for_uri(uri)
        if not self._file_is_in_symlink(cajafile):
            return None
        label = Gtk.Label("In symlink directory " + self._read_symlink(cajafile))
        label.set_selectable(True)
        label.show()
        return label
