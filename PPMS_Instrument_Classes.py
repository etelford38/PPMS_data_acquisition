from PyQt5.QtWidgets import (QGridLayout, QLabel, 
                             QPushButton, QLineEdit, QCheckBox, QComboBox)
import time
import ast
import numpy as np
from qcodes.instrument_drivers.stanford_research.SR860 import SR860
from qcodes.instrument_drivers.tektronix.Keithley_2450 import Keithley2450
from MultiPyVu import MultiVuClient as mvc
from MultiPyVu import MultiVuServer as mvs
import pyvisa as visa
rm = visa.ResourceManager()

##################################################################################################
##################################################################################################
##################################################################################################
class SR860_inst:
    ch_name=['X','Y','R','P']
    fields = ['Frequency','Amplitude','Time constant']
    ch1Display = ['X', 'R']
    ch2Display = ['Y', 'Phase']
    lockin_tc_val = ['10e-6','30e-6','100e-6','300e-6','1e-3','3e-3','10e-3','30e-3','100e-3','300e-3','1','3','10','30','100','300','1e3','3e3','10e3','30e3']
    def __init__(self, name, address, channels):
        self.name=name
        self.gpib=address
        self.ch=ast.literal_eval(channels)
        self.instr=SR860(name, address)        
        print('Connected to SR860 ('+name+')!')
        
    def measure(self):
        msmt=[]
        if self.ch==[True,True,False,False]:
            val=self.instr.get_values('X','Y')
            msmt=[str(val[0]),str(val[1])]
        elif self.ch==[False,False,True,True]:
            val=self.instr.get_values('R','P')
            msmt=[str(val[0]),str(val[1])]
        elif self.ch==[True,False,False,True]:
            val=self.instr.get_values('X','P')
            msmt=[str(val[0]),str(val[1])]
        else:
            if self.ch[0]:
                msmt.append(str(self.instr.X()))
            if self.ch[1]:
                msmt.append(str(self.instr.Y()))
            if self.ch[2]:
                msmt.append(str(self.instr.R()))
            if self.ch[3]:
                msmt.append(str(self.instr.P()))
        return msmt

    def header(self):
        hdr=[]
        for ind in range(len(self.ch)):
            if self.ch[ind]:
                hdr.append(self.name+'_'+self.ch_name[ind])
        return hdr
    
    def control_GUI(self, frame): #Create the apearence for lockins (830 and 860)
        j=0
        label={}
        for i, f in enumerate(self.fields):
            if i in range(len(self.fields)):
                label[f] = QLabel(f)
            else:
                label[f] = None
            j+=1
        freq_entry = QLineEdit(frame)
        amp_entry = QLineEdit(frame)
        tc_entry = QComboBox()
        tc_entry.addItems(self.lockin_tc_val)
        set_button = QPushButton('Set lockin parameters')
        set_button.clicked.connect(lambda: self.set_lockin_param(freq_entry,amp_entry,tc_entry))
        layout = QGridLayout()
        for i, f in enumerate(self.fields):
            if i in range(len(self.fields)):
                layout.addWidget(label[f], i, 0, 1, 1)
        layout.addWidget(freq_entry, 0, 1, 1, 1)
        layout.addWidget(amp_entry, 1, 1, 1, 1)
        layout.addWidget(tc_entry, 2, 1, 1, 1)
        layout.addWidget(set_button, 3, 0, 1, 2)
        layout.setRowStretch(j+2, 2)
        frame.setLayout(layout)
        
    def set_lockin_param(self,freq,amp,tc):
        if len(freq.text()) == 0:
            pass
        else:
            self.instr.frequency(float(freq.text()))
        if len(amp.text()) == 0:
            pass
        else:
            if float(amp.text())>2:
                print("Amplitude out of range, choose something below 2V")
            else:
                self.instr.amplitude(float(amp.text()))
        self.instr.time_constant(float(tc.currentText()))
        print('Amplitude set to:' + str(self.instr.amplitude()))
        print('Frequency set to:' + str(self.instr.frequency()))
        print('Time constant:' + str(self.instr.time_constant()))
##################################################################################################
##################################################################################################
##################################################################################################
class K2450_inst:
    ch_name=['V','I']
    KGUI_field = ['Output', 'Source Mode', 'Sense Mode','Sense Range', 'Source Range', 'Sweep To']
    keithley2450_range = ['--VOLTAGE MODE--','20e-3','200e-3','2','20','200','--CURRENT MODE--','10e-9','100e-9','1e-6','10e-6','100e-6','1e-3','10e-3','100e-3','1']
    keithley2450_comp = ['--READ CURRENT MODE--','10e-9','100e-9','1e-6','10e-6', '100e-6','1e-3', '10e-3', '100e-3', '1','--READ VOLTAGE MODE--','210e-3','2.1','21','210']

    def __init__(self, name, address, channels):
        self.name=name
        self.gpib=address
        self.ch=ast.literal_eval(channels)
        self.instr=Keithley2450(name, address)        
        self.param_K1 = [self.instr.output_enabled(),self.instr.source.function(),self.instr.sense.function()]
        print('Connected to K2450 ('+name+')!')
        
    def measure(self):
        msmt=[]
        if self.ch[0]:
            if self.instr.source.function()=='voltage':
                msmt.append(str(self.instr.source.voltage()))
            else:
                msmt.append(str(self.instr.sense.voltage()))
        if self.ch[1]:
            if self.instr.source.function()=='current':   
                msmt.append(str(self.instr.source.current()))
            else:
                msmt.append(str(self.instr.sense.current()))
        return msmt

    def header(self):
        hdr=[]
        for ind in range(len(self.ch)):
            if self.ch[ind]:
                hdr.append(self.name+'_'+self.ch_name[ind])
        return hdr
    
    def set_val(self, val, mode=0): #Make compatible with current
        if mode==0:
            if self.instr.source.function()=='current':
                self.instr.source.currrent(val)
            else:
                self.instr.source.voltage(val)
        elif mode==1:
            self.instr.source.voltage(val)
        elif mode==2:
            self.instr.source.current(val)
            
    def now_at(self, mode=0):
        if mode==0:
            if self.instr.source.function()=='current':
                return self.instr.source.currrent()
            else:
                return self.instr.source.voltage()
        elif mode==1:
            return self.instr.source.voltage()
        elif mode==2:
            return self.instr.source.current()
    
    def sweep_val(self,val, step, rate):
        if self.instr.source.function()=='current':
            m=2
        else:
            m=1
        v0=self.now_at(mode=m)
        sweep=np.linspace(v0,val,int(step+1))
        for v in sweep:
            self.set_val(v, mode=m)
        self.set_val(val, mode=m)
    
    def control_GUI(self, frame):#Apearence for Keithley control panel
        j=0
        label={}
        for i, f in enumerate(self.KGUI_field):
            label[f] = QLabel(f)
            j+=1
        out_entry = None
        out_button = QPushButton('ON' if self.param_K1[0] == True else 'OFF')
        out_button.setStyleSheet("background-color: #008B45;" if self.param_K1[0] == True else "background-color: #CD4F39;")
        out_button.clicked.connect(lambda: self.set_output(out_button))
        mode_entry = None
        mode_button = QPushButton('VOLT' if self.param_K1[1] in ['VOLT','voltage'] else 'CURR')
        mode_button.clicked.connect(lambda: self.set_mode(mode_button,out_button))
        read_entry = None
        read_button = QPushButton('VOLT' if self.param_K1[2] in ['VOLT','voltage'] else 'CURR')
        read_button.clicked.connect(lambda: self.set_read(read_button))
        comp_entry = QComboBox()
        comp_entry.addItems(self.keithley2450_comp)
        comp_button = QPushButton('Set')
        comp_button.clicked.connect(lambda: self.set_compliance(comp_entry))
        range_entry = QComboBox()
        range_entry.addItems(self.keithley2450_range)
        range_button = QPushButton('Set')
        range_button.clicked.connect(lambda: self.set_range(range_entry))
        sweep_entry = QLineEdit(frame)
        sweepTime_entry = QLineEdit(frame)
        sweep_button = QPushButton('Set')
        sweep_button.clicked.connect(lambda: self.sweep_to(sweepTime_entry,sweep_entry))
        layout = QGridLayout()
        for i, f in enumerate(self.KGUI_field):
            layout.addWidget(label[f], i, 0, 1, 1)
        layout.addWidget(out_entry, 0, 1, 1, 2)
        layout.addWidget(out_button, 0, 3, 1, 1)
        layout.addWidget(mode_entry, 1, 1, 1, 2)
        layout.addWidget(mode_button, 1, 3, 1, 1)
        layout.addWidget(read_entry, 2, 1, 1, 2)
        layout.addWidget(read_button, 2, 3, 1, 1)
        layout.addWidget(comp_entry, 3, 1, 1, 2)
        layout.addWidget(comp_button, 3, 3, 1, 1)
        layout.addWidget(range_entry, 4, 1, 1, 2)
        layout.addWidget(range_button, 4, 3, 1, 1)
        layout.addWidget(QLabel('value'), 5, 1, 1, 1)
        layout.addWidget(QLabel('number of points'), 5, 2, 1, 1)
        layout.addWidget(sweep_entry, 6, 1, 1, 1)
        layout.addWidget(sweepTime_entry, 6, 2, 1, 1)
        layout.addWidget(sweep_button, 6, 3, 1, 1)
        layout.setRowStretch(j+2, 3)
        frame.setLayout(layout)
        
    def set_output(self,button):
        if self.instr.output_enabled()==True:
            self.instr.output_enabled(False)
            button.setText('OFF')
            button.setStyleSheet("background-color: #CD4F39;")
            print("Output:"+str(self.instr.output_enabled()))
        else:
            self.instr.output_enabled(True)
            button.setText('ON')
            button.setStyleSheet("background-color: #008B45;")
            print("Output:"+str(self.instr.output_enabled()))
    
    def set_mode(self,val,out):
        if self.instr.source.function() == 'current':
            val.setText('VOLT')
            self.instr.source.function('voltage')
            out.setText('OFF')
            out.setStyleSheet("background-color: #CD4F39;")
            print("Source:"+str(self.instr.source.function()))
        else:
            val.setText('CURR')
            self.instr.source.function('current')
            out.setText('OFF')
            out.setStyleSheet("background-color: #CD4F39;")
            print("Source:"+str(self.instr.source.function()))
    
    def set_compliance(self, val):
        value = float(val.currentText())
        if self.instr.source.function() == 'current':
            self.instr.sense.range(value)
            print("Sense Range:"+str(self.instr.sense.range()))
        else:
            self.instr.sense.range(value)
            print("Sense Range:"+str(self.instr.sense.range()))
    
    def set_range(self, val):
        value = float(val.currentText())
        if self.instr.source.function() == 'current':
            self.instr.source.range(value)
            print("Source Range:"+str(self.instr.source.range()))
        else:
            self.instr.source.range(value)
            print("Source Range:"+str(self.instr.source.range()))
    
    def sweep_to(self,ste,val):
        value = float(val.text())
        step = float(ste.text())
        self.sweep_val(value, step, .1)
    
    def set_read(self,val):
        if self.instr.sense.function() == 'current':
            self.instr.sense.function('voltage')
            val.setText('VOLT')
            print("Measure:"+str(self.instr.sense.function()))
        elif self.instr.sense.function() == 'voltage':
            self.instr.sense.function('current')
            val.setText('CURR')
            print("Measure:"+str(self.instr.sense.function()))
##################################################################################################
##################################################################################################
##################################################################################################
class K6221_inst:
    ch_name=['V','I']
    KGUI_fields = ['Compliance (V)', 'Source Current (A)']

    def __init__(self, name, address, channels):
        self.name=name
        self.gpib='GPIB0::'+str(address)+'::INSTR'
        self.ch=ast.literal_eval(channels)
        self.instr=rm.open_resource(address)
        print('Connected to Keithley 6221: ' + str(self.instr))
        self.instr.write('*RST')
        self.instr.write('SOUR:CURR:COMP 10') #arms with 1 nanoamp to start
        self.instr.write('SOUR:DELT:HIGH 1e-9') #arms with 1 nanoamp to start
        self.instr.write('SOUR:DELT:ARM')
        self.instr.write('INIT:IMM')
        time.sleep(5)
        self.instr.write('SYST:COMM:SER:SEND "SENS:VOLT:RANG:AUTO ON"')
        print('Connected to K6221 ('+name+')!')
        
    def measure(self):
        msmt=[]
        if self.ch[0]:
            msmt.append(str(self.instr.query("SENS:DATA:LATest?").split(',')[0]))
        if self.ch[1]:
            msmt.append(str(self.instr.query("SOUR:DELT:HIGH?").split('\n')[0]))
        return msmt

    def header(self):
        hdr=[]
        for ind in range(len(self.ch)):
            if self.ch[ind]:
                hdr.append(self.name+'_'+self.ch_name[ind])
        return hdr
    
    def control_GUI(self, frame): #Create the apearence for keithley 6221
        j=0
        label={}
        for i, f in enumerate(self.KGUI_fields):
            if i in range(len(self.KGUI_fields)):
                label[f] = QLabel(f)
            else:
                label[f] = None
            j+=1 
        compliance_entry = QLineEdit(frame)
        compliance_button = QPushButton('Set')
        compliance_button.clicked.connect(lambda: self.set_compliance(compliance_entry.text()))
        source_entry = QLineEdit(frame)
        source_button = QPushButton('Set')
        source_button.clicked.connect(lambda: self.set_current(source_entry.text()))
        layout = QGridLayout()
        for i, f in enumerate(self.KGUI_fields):
            if i in range(len(self.KGUI_fields)):
                layout.addWidget(label[f], i, 0, 1, 1)
        layout.addWidget(compliance_entry, 0, 1, 1, 2)
        layout.addWidget(compliance_button, 0, 3, 1, 1)
        layout.addWidget(source_entry, 1, 1, 1, 2)
        layout.addWidget(source_button, 1, 3, 1, 1)
        layout.setRowStretch(j+2, 2)
        frame.setLayout(layout)
        
    def set_current(self, current):
        temp=self.instr.query('SOUR:CURR:COMP?')
        self.instr.write('*RST')
        self.instr.write('SOUR:DELT:HIGH '+str(current))
        self.instr.write('SOUR:CURR:COMP '+ str(temp))
        self.instr.write('SOUR:DELT:ARM')
        self.instr.write('INIT:IMM')
        time.sleep(5)
        self.instr.write('SYST:COMM:SER:SEND "SENS:VOLT:RANG:AUTO ON"')
        print('Output current is ' + str(self.instr.query('SOUR:DELT:HIGH?').split('\n')[0]) + ' A')
        print('Compliance is ' + str(self.instr.query('SOUR:CURR:COMP?').split('\n')[0]) + ' V')
        
    def set_compliance(self, comp):
        temp=self.instr.query('SOUR:DELT:HIGH?')
        self.instr.write('*RST')
        self.instr.write('SOUR:DELT:HIGH '+str(temp))
        self.instr.write('SOUR:CURR:COMP '+ str(comp))
        self.instr.write('SOUR:DELT:ARM')
        self.instr.write('INIT:IMM')
        time.sleep(5)
        self.instr.write('SYST:COMM:SER:SEND "SENS:VOLT:RANG:AUTO ON"')
        print('Compliance is ' + str(self.instr.query('SOUR:CURR:COMP?').split('\n')[0]) + ' V')
        print('Output current is ' + str(self.instr.query('SOUR:DELT:HIGH?').split('\n')[0]) + ' A')
##################################################################################################
##################################################################################################
##################################################################################################
class K6517B_inst:
    ch_name=['R']
    KGUI_fields = ['Output', 'Source (V)', 'Limit (V)']

    def __init__(self, name, address, channels):
        self.name=name
        self.gpib='GPIB0::'+str(address)+'::INSTR'
        self.ch=ast.literal_eval(channels)
        self.instr=rm.open_resource(address)
        print('Connected to Keithley 6517B: ' + str(self.instr))
        #Turns on meter-connect. This is essential!
        self.instr.write(':syst:KEY 28')
        self.instr.write(':syst:KEY 19') 
        self.instr.write(':syst:KEY 10') 
        self.instr.write(':syst:KEY 10') 
        self.instr.write(':syst:KEY 10') 
        self.instr.write(':syst:KEY 18') 
        self.instr.write(':syst:KEY 10') 
        self.instr.write(':syst:KEY 18') 
        self.instr.write(':syst:KEY 11') 
        #turns on zero check if not already enabled
        zero_checked=self.instr.query(':syst:ZCH?')
        if int(zero_checked) == True:
            pass
        else:
            self.instr.write(':syst:KEY 23') #presses Z-CHK key - step 1
        #set tool in resistance mode
        self.instr.write(':syst:KEY 29') #press R key - step 2
        #set voltage output mode to automatic
        self.instr.write(':SENS:RES:VSC MAN')
        #set voltage output range
        voltage=0
        self.instr.write('RES:MAN:VSO:RANG '+str(voltage))
        self.instr.write('RES:MAN:VSO:AMPL '+str(voltage))
        #enable Z-CHK
        self.instr.write(':syst:KEY 23') #presses Z-CHK key - step 1
        #turn output on
        self.instr.write('OUTP OFF')
        #set resistance range
        self.instr.write('SENS:RES:MAN:CRAN:AUTO ON')
        #prints confirmation
        # print('Configured in ' + str(self.instr.query('CONF?')) + ' mode') #read configured measurement type
        print('Connected to K6517B ('+name+')!')
        
    def measure(self):
        msmt=[]
        if self.ch[0]:
            temp=str(self.instr.query(':SENS:DATA:FRESH?').split(',')[0][:-4])
            msmt.append(temp[0:-4])
        return msmt

    def header(self):
        hdr=[]
        for ind in range(len(self.ch)):
            if self.ch[ind]:
                hdr.append(self.name+'_'+self.ch_name[ind])
        return hdr
    
    def control_GUI(self, frame): #Create the apearence for keithley 6221
        j=0
        label={}
        for i, f in enumerate(self.KGUI_fields):
            if i in range(len(self.KGUI_fields)):
                label[f] = QLabel(f)
            else:
                label[f] = None
            j+=1
        out_entry = None
        out_button = QPushButton('ON' if int(self.instr.query('OUTP?')) == int(1) else 'OFF')
        out_button.setStyleSheet("background-color: #008B45;" if int(self.instr.query('OUTP?')) == int(1) else "background-color: #CD4F39;")
        out_button.clicked.connect(lambda: self.set_output(out_button))
        compliance_entry = QLineEdit(frame)
        compliance_button = QPushButton('Set')
        compliance_button.clicked.connect(lambda: self.set_compliance(compliance_entry.text()))
        source_entry = QLineEdit(frame)
        source_button = QPushButton('Set')
        source_button.clicked.connect(lambda: self.set_voltage(source_entry.text()))
        layout = QGridLayout()
        for i, f in enumerate(self.KGUI_fields):
            if i in range(len(self.KGUI_fields)):
                layout.addWidget(label[f], i, 0, 1, 1)
        layout.addWidget(out_entry, 0, 1, 1, 2)
        layout.addWidget(out_button, 0, 3, 1, 1)
        layout.addWidget(compliance_entry, 2, 1, 1, 2)
        layout.addWidget(compliance_button, 2, 3, 1, 1)
        layout.addWidget(source_entry, 1, 1, 1, 2)
        layout.addWidget(source_button, 1, 3, 1, 1)
        layout.setRowStretch(j+2, 2)
        frame.setLayout(layout)
        
    def set_compliance(self, comp):
        self.instr.write('SOUR:VOLT:LIM:AMPL ' + str(comp))
        self.instr.write('SOUR:VOLT:LIM:STAT ON')
        if int(self.instr.query('SOUR:VOLT:LIM:STAT?'))==1:
            print('Compliance is ON')
        else:
            print('Compliance is OFF')
        print('Compliance is ' + str(self.instr.query('SOUR:VOLT:LIM:AMPL?').split('\n')[0])+' V')
        print('Output voltage is ' + str(self.instr.query('SOUR:VOLT?').split('\n')[0])+' V')
        
    def set_voltage(self,volt):
        self.instr.write('RES:MAN:VSO:RANG ' + str(volt))
        self.instr.write('RES:MAN:VSO:AMPL ' + str(volt))
        print('Output voltage is ' + str(self.instr.query('RES:MAN:VSO:AMPL?').split('\n')[0])+' V')
        print('Output voltage range is ' + str(self.instr.query('RES:MAN:VSO:RANG?').split('\n')[0])+' V')
            
    def set_output(self,button):
        if int(self.instr.query('OUTP?')) == int(1):
            self.instr.write('OUTP OFF')
            button.setText('OFF')
            button.setStyleSheet("background-color: #CD4F39;")
            print("Output:"+ ' ON' if int(self.instr.query('OUTP?').split('\n')[0])==True else 'Output:'+' OFF')
        else:
            self.instr.write('OUTP ON')
            button.setText('ON')
            button.setStyleSheet("background-color: #008B45;")
            print("Output:"+ ' ON' if int(self.instr.query('OUTP?').split('\n')[0])==True else 'Output:'+' OFF')
##################################################################################################
##################################################################################################
##################################################################################################
class Dynacool_inst:
    ch_name=['T', 'B']
    KGUI_fields = ['T_control','B_control']
    KGUI_fields2= ['Setpoint (K or Oe)', 'Rate (K/min or Oe/s)']

    def __init__(self, name, address, channels):
        self.name=name
        self.gpib='127.0.0.1'
        self.ch=ast.literal_eval(channels)
        self.server=mvs.MultiVuServer()
        self.server.open()
        self.client = mvc.MultiVuClient(host='127.0.0.1')
        self.client.open()
        print('Connected to PPMS Dynacool')
        
    def measure(self):
        msmt=[]
        if self.ch[0]:
            temperature, status = self.client.get_temperature()
            msmt.append(str(temperature))
        if self.ch[1]:
            field, status = self.client.get_field() #get field and status
            msmt.append(str(field))
        return msmt

    def header(self):
        hdr=[]
        for ind in range(len(self.ch)):
            if self.ch[ind]:
                hdr.append(self.name+'_'+self.ch_name[ind])
        return hdr
    
    def close(self):
        self.client.close_client()
        self.server.close()
        
    def control_GUI(self, frame):
        j=0
        l=0
        label={}
        label2={}
        for i, f in enumerate(self.KGUI_fields):
            if i in range(len(self.KGUI_fields)):
                label[f] = QLabel(f)
            else:
                label[f] = None
            j+=1
            
        for i, f in enumerate(self.KGUI_fields2):
            if i in range(len(self.KGUI_fields2)):
                label2[f] = QLabel(f)
            else:
                label2[f] = None
            l+=1
        Tset_entry = QLineEdit(frame)
        Tset_rate = QLineEdit(frame)
        Tset_button = QPushButton('Set')
        Tset_button.clicked.connect(lambda: self.client.set_temperature(Tset_entry.text(),Tset_rate.text(),self.client.temperature.approach_mode.fast_settle))
        Bset_entry = QLineEdit(frame)
        Bset_rate = QLineEdit(frame)
        Bset_button = QPushButton('Set')
        Bset_button.clicked.connect(lambda: self.client.set_field(Bset_entry.text(), Bset_rate.text(),self.client.field.approach_mode.linear))
        layout = QGridLayout()
        for i, f in enumerate(self.KGUI_fields):
            if i in range(len(self.KGUI_fields)):
                layout.addWidget(label[f], i+1, 0, 1, 1)
        for i, f in enumerate(self.KGUI_fields2):
            if i in range(len(self.KGUI_fields2)):
                layout.addWidget(label2[f], 0, i+1, 1, 1)        
        layout.addWidget(Tset_entry, 1, 1, 1, 1)
        layout.addWidget(Tset_rate, 1, 2, 1, 1)
        layout.addWidget(Tset_button, 1, 3, 1, 1)
        layout.addWidget(Bset_entry, 2, 1, 1, 1)
        layout.addWidget(Bset_rate, 2, 2, 1, 1)
        layout.addWidget(Bset_button, 2, 3, 1, 1)
        layout.setRowStretch(j+2, 4)
        frame.setLayout(layout)
##################################################################################################
##################################################################################################
##################################################################################################