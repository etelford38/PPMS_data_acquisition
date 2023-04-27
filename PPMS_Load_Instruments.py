from PyQt5.QtWidgets import (QApplication,  QDialog, 
                             QGridLayout, QVBoxLayout,  QLabel, 
                             QPushButton, QStyleFactory,  
                             QFrame, QMenu, QToolButton, QMessageBox)
from PPMS_GUI_Functions import GUI_functions
import sys
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtGui import QPalette, QColor
from PPMS_Instruments import Instruments
import pyvisa as visa
rm = visa.ResourceManager()
dic_instr=[]
GUI = GUI_functions(dic_instr)

class Main_LoadInstr(QDialog):
    def __init__(self, parent=None):
        super (Main_LoadInstr, self).__init__(parent)
        self.setGeometry(50,50,300,200) #Set size of GUI
        #Apearence parameters
        self.originalPalette = QApplication.palette()
        self.font = QtGui.QFont()
        self.font.setFamily('Helvetica')
        self.font.setPointSize(16)
        self.font.setBold(True)
        self.font.setItalic(True)
        self.check_value={}
        self.color_value={}
        self.label_value={}
        self.edit_value={}
        self.instr_select={}
        self.ch_selector={}
        self.ch_menu={}
        self.dic={}
        self.list_instr=[]
        self.list_gpib_old=[]
        self.list_gpib_new=[]
        self.list_print=''
        self.my_instrument=[]
        self.sr860_ch=['X','Y','R','Theta']
        self.k2450_ch=['V','I']
        self.k6221_ch=['V','I']
        self.k6517B_ch=['R']
        self.Dynacool_ch=['T','B']
        self.ch_record=[]
        self.nspots=5
        self.createGroup()
        #Sets position of each group in the GUI
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.Group,0, 0, 1, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("RoyLab - Load Instruments") #Title of the GUI window
        QApplication.setStyle(QStyleFactory.create('Fusion')) #Style of the GUI
 
    def createGroup(self):
        self.Group = QFrame()
        gpib_Label = QLabel('GPIB address')
        name_Label = QLabel('Instrument Name')
        for i in range(self.nspots):
            self.check_value[i],self.instr_select[i],self.label_value[i],self.edit_value[i] = GUI.LoadInstr_GUI()
            self.ch_selector[i]=QToolButton()
            self.ch_menu[i]=QMenu()
            self.ch_selector[i].setMenu(self.ch_menu[i])
            self.ch_selector[i].setPopupMode(QToolButton.InstantPopup)
            self.edit_value[i].setDisabled(True)
            self.instr_select[i].setDisabled(True)
            self.label_value[i].setDisabled(True)
            self.check_value[i].toggled.connect(self.instr_select[i].setEnabled)
            self.check_value[i].toggled.connect(self.edit_value[i].setEnabled)
            self.check_value[i].toggled.connect(self.edit_value[i].clear)
            self.check_value[i].toggled.connect(self.label_value[i].setEnabled)
            self.check_value[i].toggled.connect(self.label_value[i].clear)
            self.instr_select[i].currentIndexChanged.connect(lambda state, idx=i: self.changeMenu(self.instr_select[idx].currentText(), self.ch_menu[idx], idx))
            self.ch_record.append([]) 
        resourceButton = QPushButton('See available resources')
        resourceButton.clicked.connect(self.SeeInstr)
        testButton = QPushButton('Test Connections')
        testButton.clicked.connect(self.testConnect)
        exitButton = QPushButton('CLOSE')
        exitButton.clicked.connect(self.QuitApp)
        addButton = QPushButton('Add Instrument')
        addButton.clicked.connect(self.addrow)
        self.layout = QGridLayout()
        self.layout.addWidget(gpib_Label, 0, 3, 1, 1)
        self.layout.addWidget(name_Label, 0, 2, 1, 1)
        for i in range(self.nspots):
            self.layout.addWidget(self.check_value[i], i+1, 0, 1, 1)
            self.layout.addWidget(self.instr_select[i], i+1, 1, 1, 1)
            self.layout.addWidget(self.label_value[i], i+1, 2, 1, 1)
            self.layout.addWidget(self.edit_value[i], i+1, 3, 1, 1)
            self.layout.addWidget(self.ch_selector[i], i+1, 4, 1, 1)
        layout2 = QGridLayout()
        layout2.addWidget(resourceButton,1,0,1,1)
        layout2.addWidget(testButton,1,1,1,1)
        layout2.addWidget(exitButton,1,2,1,1)
        layout2.addWidget(addButton,1,3,1,1)
        mainlayout = QVBoxLayout()
        mainlayout.addLayout(self.layout)
        mainlayout.addLayout(layout2)
        self.Group.setLayout(mainlayout)
        
    def changeMenu(self, instrument, menu, idx):
        menu.clear()
        self.ch_record[idx]=[]
        ind=0
        if instrument=='SR860':
            self.ch_record[idx]=[False, False, False, False]
            for i in self.sr860_ch:
                action = menu.addAction(i)
                action.setCheckable(True)
                action.triggered.connect(lambda state, x=idx, y=ind: self.addch(x,y))
                ind+=1
        elif instrument=='Keithley 2450':
            for i in self.k2450_ch:
                self.ch_record[idx]=[False, False]
                action = menu.addAction(i)
                action.setCheckable(True)
                action.triggered.connect(lambda state, x=idx, y=ind: self.addch(x,y))
                ind+=1
        elif instrument=='Keithley 6221':
            for i in self.k6221_ch:
                self.ch_record[idx]=[False, False]
                action = menu.addAction(i)
                action.setCheckable(True)
                action.triggered.connect(lambda state, x=idx, y=ind: self.addch(x,y))
                ind+=1
        elif instrument=='Keithley 6517B':
            for i in self.k6517B_ch:
                self.ch_record[idx]=[False]
                action = menu.addAction(i)
                action.setCheckable(True)
                action.triggered.connect(lambda state, x=idx, y=ind: self.addch(x,y))
                ind+=1
        elif instrument=='Dynacool':
            for i in self.Dynacool_ch:
                self.ch_record[idx]=[False, False]
                action = menu.addAction(i)
                action.setCheckable(True)
                action.triggered.connect(lambda state, x=idx, y=ind: self.addch(x,y))
                ind+=1
    
    def addch(self, ins_id, ch_id):
        self.ch_record[ins_id][ch_id]=not self.ch_record[ins_id][ch_id]
        return
    
    def testConnect(self):
        self.write_file()        
        ins=Instruments()
        print(ins.header())
    
    def addrow(self):
        i=self.nspots
        self.check_value[i],self.instr_select[i],self.label_value[i],self.edit_value[i] = GUI.LoadInstr_GUI()
        self.ch_selector[i]=QToolButton()
        self.ch_menu[i]=QMenu()
        self.ch_selector[i].setMenu(self.ch_menu[i])
        self.ch_selector[i].setPopupMode(QToolButton.InstantPopup)
        self.edit_value[i].setDisabled(True)
        self.check_value[i].toggled.connect(self.instr_select[i].setEnabled)
        self.check_value[i].toggled.connect(self.edit_value[i].setEnabled)
        self.check_value[i].toggled.connect(self.edit_value[i].clear)
        self.check_value[i].toggled.connect(self.label_value[i].setEnabled)
        self.check_value[i].toggled.connect(self.label_value[i].clear)
        self.instr_select[i].currentIndexChanged.connect(lambda state, idx=i: self.changeMenu(self.instr_select[idx].currentText(), self.ch_menu[idx], idx))
        self.ch_record.append([])
        self.layout.addWidget(self.check_value[i], i+1, 0, 1, 1)
        self.layout.addWidget(self.instr_select[i], i+1, 1, 1, 1)
        self.layout.addWidget(self.label_value[i], i+1, 2, 1, 1)
        self.layout.addWidget(self.edit_value[i], i+1, 3, 1, 1)
        self.layout.addWidget(self.ch_selector[i], i+1, 4, 1, 1)
        self.nspots+=1
    
    def write_file(self):
        f = open('Instruments.txt', 'r+')
        f.truncate(0)
        for ind in range(self.nspots):
            if self.check_value[ind].isChecked():
                seq=[]
                seq.append('Name='+self.label_value[ind].text()+'\n')
                seq.append('Instrument='+self.instr_select[ind].currentText()+'\n')
                seq.append('GPIB='+self.edit_value[ind].text()+'\n')
                seq.append('channels='+str(self.ch_record[ind])+'\n')
                seq.append('\n')
                f.writelines(seq)
        f.close()
        
    def SeeInstr(self):
        rm = visa.ResourceManager()
        instrL=[]
        for i,f in enumerate(rm.list_resources()):
            if 'GPIB' in f:
                instr = rm.open_resource(f)
                try:
                    instr.query('*IDN?')
                    instrL.append(instr)
                except:
                    pass
        self.my_instrument=[]
        self.list_print=''
        for i,f in enumerate(instrL):
            self.my_instrument.append(f)
            self.list_print+= str(f).split('::')[1]+'\t'
            self.list_print+=str(self.my_instrument[i].query('*IDN?').split(',')[0])+' '+str(self.my_instrument[i].query('*IDN?').split(',')[1])+'\n'
        warning = QMessageBox()
        warning.setIcon(QMessageBox.Information)
        warning.setWindowTitle("Available resources")
        warning.setText(str(self.list_print))
        warning.setStandardButtons(QMessageBox.Ok)
        warning.exec()        
        
    def QuitApp(self):
        self.close()
        
    
#Lines to call the app and run it      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QtCore.Qt.black)
    palette.setColor(QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QPalette.Text, QtCore.Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    gallery = Main_LoadInstr()
    gallery.show()
    app.exec_()