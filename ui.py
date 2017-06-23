import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class alignmentWin:


    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("AlignmentsUI.glade")
        builder.connect_signals(self)
        window = builder.get_object("winAlign")
        window.set_default_size(1000, 1000)
        self.btnAlign = builder.get_object("btnAlign")
        window.show_all()
        self.strAvalid = False
        self.strBvalid = False

    def onChangeStrA(self, widget):
        widget.set_text(widget.get_text().upper())
        self.strAvalid = self.validateTxt(widget)
        if self.strAvalid and self.strBvalid:
            self.btnAlign.set_sensitive(True)
        else:
            self.btnAlign.set_sensitive(False)

    def onChangeStrB(self, widget):
        widget.set_text(widget.get_text().upper())
        self.strBvalid = self.validateTxt(widget)
        if self.strAvalid and self.strBvalid:
            self.btnAlign.set_sensitive(True)
        else:
            self.btnAlign.set_sensitive(False)

    def validateTxt(self, widget):
        if len(widget.get_text()) > 25 \
                or widget.get_text() == "" \
                or not widget.get_text().isalpha():
            return False
        else:
            return True



if __name__=="__main__":
    window = alignmentWin()
    Gtk.main()