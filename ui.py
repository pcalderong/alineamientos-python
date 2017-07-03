import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
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
        self.cbNWF = builder.get_object("cbNWF")
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
        self.labelStringA = builder.get_object("lblStringV")
        self.labelStringB = builder.get_object("lblStringW")
        self.labelScoring = builder.get_object("lblScoring")
        self.labelScoringMax = builder.get_object("lblScoringMax")
        self.layoutTable = builder.get_object("fixedTable")
        self.bxAlignment = builder.get_object("bxAlignments")
        window.show_all()
        self.strAvalid = False
        self.strBvalid = False
        self.isSW = False
        self.isNW = True
        self.isNWR = False
        self.isNWC = False
        self.isNWF = False
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
        self.isNWF = False
        self.cbNWC.set_active(False)
        self.cbNWR.set_active(False)
        self.cbNWF.set_active(False)
        if rb == "local":
            self.isSW = True
            self.isNW = False
            self.cbNWC.set_sensitive(False)
            self.cbNWR.set_sensitive(False)
            self.cbNWF.set_sensitive(True)
        else:
            self.isNW = True
            self.isSW = False
            self.cbNWC.set_sensitive(True)
            self.cbNWR.set_sensitive(True)
            self.cbNWF.set_sensitive(True)

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

    def onCheckboxSelectedF(self, widget):
        if widget.get_active():
            self.isNWF = True
        else:
            self.isNWF = False

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
        self.onCleanLayout()
        print("Now to align")
        results = alignStrings(self.spMatch.get_value_as_int(), self.spMismatch.get_value_as_int(),self.spGapPenalty.get_value_as_int(),
                     self.txtStrB.get_text(), self.txtStrA.get_text(), self.isNW, self.isNWC, self.isNWR, self.isNWF, self.isSW)
        self.labelStringA.set_text(results[2][0])
        self.labelStringB.set_text(results[2][1])
        self.labelScoringMax.set_text(str(results[2][2]))
        self.printMatrix(results[0], results[1], self.txtStrB.get_text(), self.txtStrA.get_text())
        for x in results[3]:
            label = Gtk.Label()
            label.set_markup("<span>" + x[0] +" --- " + x[1] +"    Scoring: "+str(x[2])+"</span>")
            self.bxAlignment.pack_start(label, True, True, 1)
            label.show()
    def onCleanLayout(self):
        for i in self.bxAlignment:
            self.bxAlignment.remove(i)
        for l in self.layoutTable:
            self.layoutTable.remove(l)

    def printMatrix(self, matrix, arrows, stringA, stringB):
        x = 140
        y = 20
        for i in range(len(stringB)+1):
            label = Gtk.Label()
            text = "-"
            if i > 0:
                text = stringB[i - 1]
            label.set_markup("<span color='#13719f'>" + text + "</span>")
            self.layoutTable.put(label, x, y)
            label.show()
            x += 75
        y += 25
        x = 75

        for i in range(len(stringA)+1):
            label = Gtk.Label()
            text = "-"
            if i > 0:
                text = stringA[i-1]
            label.set_markup("<span color='#ff8847'>" + text + "</span>")
            self.layoutTable.put(label, x, y)
            label.show()
            x += 50
            for j in range(len(stringB)+1):
                if i>0:
                    y -= 35
                if "d" in arrows[i][j]:
                    labelD = Gtk.Label()
                    if "w" in arrows[i][j]:
                        labelD.set_markup("<span color='#f03845'>&#8598;</span>")
                    else:
                        labelD.set_markup("<span color='#aaaaaa'>&#8598;</span>")
                    labelD.set_width_chars(1)
                    self.layoutTable.put(labelD, x , y)
                    labelD.show()
                if "u" in arrows[i][j]:
                    labelU = Gtk.Label()
                    if "w" in arrows[i][j]:
                        labelU.set_markup("<span color='#f03845'>&#8593;</span>")
                    else:
                        labelU.set_markup("<span color='#aaaaaa'>&#8593;</span>")
                    labelU.set_width_chars(1)
                    if j>0:
                        self.layoutTable.put(labelU, x + 35, y)
                    else:
                        self.layoutTable.put(labelU, x+10, y)
                    labelU.show()
                if i>0:
                    y += 35
                if "l" in arrows[i][j]:
                    labelL = Gtk.Label()
                    if "w" in arrows[i][j]:
                        labelL.set_markup("<span color='#f03845'>&#8592;</span>")
                    else:
                        labelL.set_markup("<span color='#aaaaaa'>&#8592;</span>")
                    labelL.set_width_chars(1)
                    self.layoutTable.put(labelL, x, y)
                    labelL.show()
                if j>0:
                    x += 25
                label = Gtk.Label()
                if "w" in arrows[i][j]:
                    label.set_markup("<span color='#f03845'>" + str(matrix[i][j]) + "</span>")
                else:
                    label.set_markup("<span color='#aaaaaa'>" + str(matrix[i][j]) + "</span>")
                label.set_width_chars(5)
                self.layoutTable.put(label, x, y)
                label.show()
                x += 50
            y += 75
            x = 75

if __name__=="__main__":
    window = alignmentWin()
    Gtk.main()