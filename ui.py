import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils import readFile
from alignment import alignStrings

class alignmentWin:


    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("AlignmentsUI.glade")
        builder.connect_signals(self)
        window = builder.get_object("winAlign")
        window.set_default_size(1000, 1000)
        self.btnAlign = builder.get_object("btnAlign")
        self.rbGlobal = builder.get_object("rbGlobal")
        self.rbLocal = builder.get_object("rbLocal")
        self.rbGlobal.connect("toggled",self.onRBSelected, "global")
        self.rbLocal.connect("toggled", self.onRBSelected, "local")
        self.cbNWC = builder.get_object("cbNWC")
        self.cbNWR = builder.get_object("cbNWR")
        self.fcStrA = builder.get_object("fcStrA")
        self.fcStrA.add_button("Cancel", 1)
        self.fcStrA.add_button("OK", 2)
        self.fcStrB = builder.get_object("fcStrB")
        self.fcStrB.add_button("Cancel", 1)
        self.fcStrB.add_button("OK", 2)
        self.txtStrA = builder.get_object("txtStrA")
        self.txtStrB = builder.get_object("txtStrB")
        self.spMatch = builder.get_object("spMatch")
        self.spMismatch = builder.get_object("spMismatch")
        self.spGapPenalty = builder.get_object("spGapPenalty")

        window.show_all()
        self.strAvalid = False
        self.strBvalid = False
        self.isSW = False
        self.isNW = True
        self.isNWR = False
        self.isNWC = False
        self.fileNameA = ""
        self.fileNameB = ""

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
        if len(widget.get_text()) > 1000 \
                or widget.get_text() == "" \
                or not widget.get_text().isalpha():
            return False
        else:
            return True

    def onRBSelected(self, widget, rb):
        self.isNWR = False
        self.isNWC = False
        self.cbNWC.set_active(False)
        self.cbNWR.set_active(False)
        if rb == "local":
            self.isSW = True
            self.isNW = False
            self.cbNWC.set_sensitive(False)
            self.cbNWR.set_sensitive(False)
        else:
            self.isNW = True
            self.isSW = False
            self.cbNWC.set_sensitive(True)
            self.cbNWR.set_sensitive(True)

    def onCheckboxSelectedR(self, widget):
        if widget.get_active():
            self.isNWR = True
        else:
            self.isNWR = False

    def onCheckboxSelectedC(self, widget):
        if widget.get_active():
            self.isNWC = True
        else:
            self.isNWC = False

    def onFileSelectedA(self, widget):
        if widget.get_filename():
            self.fileNameA = widget.get_filename()

    def onFileSelectedB(self, widget):
        if widget.get_filename():
            self.fileNameB = widget.get_filename()

    def onResponseA(self, widget, response):
        self.txtStrA.set_text(readFile(self.fileNameA))
        return True

    def onResponseB(self, widget, response):
        self.txtStrB.set_text(readFile(self.fileNameB))
        return False

    def onExecuteAlignment(self, widget):
        print("Now to align")
        alignStrings(self.spMatch.get_value_as_int(), self.spMismatch.get_value_as_int(),self.spGapPenalty.get_value_as_int(),
                     self.txtStrA.get_text(), self.txtStrB.get_text(), self.isNW, self.isNWC, self.isNWR, self.isSW)

if __name__=="__main__":
    window = alignmentWin()
    Gtk.main()