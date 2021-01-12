import hashlib
import os

from gi.repository import Caja, GObject, Gtk


class HashSumPropertyPage(GObject.GObject, Caja.PropertyPageProvider):
    value_labels = {}

    def __init__(self):
        pass

    def get_property_pages(self, files):
        if len(files) != 1:
            return

        file = files[0]
        if file.get_uri_scheme() != "file":
            return

        if file.is_directory():
            return

        filename = file.get_location().get_path()

        if os.path.getsize(filename) > 10 * 1024 * 1024:
            return

        self.property_label = Gtk.Label("HashSums")
        self.property_label.show()

        self.vbox = Gtk.VBox(homogeneous=False, spacing=0)
        self.vbox.show()

        for algo in ["MD5Sum", "SHA-1", "SHA-256", "SHA-512"]:
            hbox = Gtk.HBox(homogeneous=False, spacing=10)
            hbox.show()

            label = Gtk.Label("%s:" % algo)
            label.show()
            hbox.pack_start(label, False, False, 0)

            self.value_labels[algo] = Gtk.Label()
            self.value_labels[algo].set_selectable(True)
            self.value_labels[algo].show()
            hbox.pack_start(self.value_labels[algo], False, False, 0)
            self.vbox.pack_start(hbox, False, False, 0)

        md5sum = hashlib.md5()
        sha1sum = hashlib.sha1()
        sha256sum = hashlib.sha256()
        sha512sum = hashlib.sha512()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5sum.update(chunk)
                sha1sum.update(chunk)
                sha256sum.update(chunk)
                sha512sum.update(chunk)
        f.close()

        self.value_labels["MD5Sum"].set_text(md5sum.hexdigest())
        self.value_labels["SHA-1"].set_text(sha1sum.hexdigest())
        self.value_labels["SHA-256"].set_text(sha256sum.hexdigest())
        self.value_labels["SHA-512"].set_text(sha512sum.hexdigest())

        return (
            Caja.PropertyPage(
                name="CajaPython::hash_sum", label=self.property_label, page=self.vbox
            ),
        )
