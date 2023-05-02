import numpy as np
from PyQt5.QtTest import QTest
keithley2450_comp = ['--READ CURRENT MODE--','10e-9','100e-9','1e-6','10e-6', '100e-6','1e-3', '10e-3', '100e-3', '1','--READ VOLTAGE MODE--','210e-3','2.1','21','210']

class Commands:
    def __init__(self,instr):
        self.instr = instr
        
    def set_lockin_param(self,ref,display1,display2,freq,amp,tc):
        if self.instr.amplitude() < 0.004:
            amp_start = 0.004
        elif self.instr.amplitude() > 5:
            amp_start = 5
        else:
            amp_start = self.instr.amplitude()
        if ref.isChecked()==True:
            if self.instr.get_idn()['model'] == 'SR830':
                self.instr.reference_source('internal')
            else:
                pass
        else:
            if self.instr.get_idn()['model'] == 'SR830':
                self.instr.reference_source('external')
            else:
                pass
        if self.instr.get_idn()['model'] == 'SR830':
            self.instr.ch1_display(display1.currentText())
            self.instr.ch2_display(display2.currentText())
        if len(freq.text()) == 0:
            pass
        else:
            self.instr.frequency(float(freq.text()))
        if len(amp.text()) == 0:
            pass
        else:
            if float(amp.text())>5:
                amplitude = 5
            elif float(amp.text())<0.004:
                amplitude = 0.004
            else:
                amplitude = float(amp.text())
            L = np.linspace(amp_start,amplitude, 21)
            for amp in L:
                self.instr.amplitude(amp)
                QTest.qWait(0.1*1000)
        print('Setting time constant:' + tc.currentText())
        self.instr.time_constant(float(tc.currentText()))
                
    def inc_sens_lockin(self):
        print('Sensitivity set to' + str(self.instr.sensitivity()))
        self.instr.increment_sensitivity()
        
    def dec_sens_lockin(self):
        print('Sensitivity set to' + str(self.instr.sensitivity()))
        self.instr.decrement_sensitivity()
        
    def set_output(self,val):
        if 'keithley' in str(self.instr):
            if self.instr.get_idn()['model'] == '2400':
                if self.instr.output()==True:
                    self.instr.output(False)
                    val.setText('OFF')
                    val.setStyleSheet("background-color: #CD4F39;")
                else:
                    self.instr.output(True)
                    val.setText('ON')
                    val.setStyleSheet("background-color: #008B45;")
            elif self.instr.get_idn()['model'] == '2450':
                if self.instr.output_enabled() == True:
                    self.instr.output_enabled(False)
                    val.setText('OFF')
                    val.setStyleSheet("background-color: #CD4F39;")
                else:
                    self.instr.output_enabled(True)
                    val.setText('ON')
                    val.setStyleSheet("background-color: #008B45;")
            else:
                pass
        else:
            pass

    def set_mode(self,val,out):
        if 'keithley' in str(self.instr):
            if self.instr.get_idn()['model'] == '2400':
                if self.instr.mode()=='CURR':
                    val.setText('VOLT')
                    self.instr.mode('VOLT')
                    out.setText('OFF')
                    out.setStyleSheet("background-color: #CD4F39;")
                    
                else:
                    val.setText('CURR')
                    self.instr.mode('CURR')
                    out.setText('OFF')
                    out.setStyleSheet("background-color: #CD4F39;")
            elif self.instr.get_idn()['model'] == '2450':
                if self.instr.source.function() == 'current':
                    val.setText('VOLT')
                    self.instr.source.function('voltage')
                    out.setText('OFF')
                    out.setStyleSheet("background-color: #CD4F39;")
                else:
                    val.setText('CURR')
                    self.instr.source.function('current')
                    out.setText('OFF')
                    out.setStyleSheet("background-color: #CD4F39;")
        else:
            pass
        
    def set_read(self,val):
        if self.instr.sense.function() == 'current':
            self.instr.sense.function('voltage')
            val.setText('VOLT')
        elif self.instr.sense.function() == 'voltage':
            self.instr.sense.function('current')
            val.setText('CURR')

    def set_compliance(self,val):
        value = float(val.currentText())
        index = val.currentIndex()
        value2 =float( keithley2450_comp[index])
        if 'keithley' in str(self.instr):
            if self.instr.get_idn()['model'] == '2400':
                if self.instr.mode() == 'CURR':
                    self.instr.compliancev(value)
                else:
                    self.instr.compliancei(value)
            else:
                self.instr.sense.range(value2)
                self.instr.source.limit(value)
            
    def set_range(self,val):
        value = float(val.currentText())
        if 'keithley' in str(self.instr):
            if self.instr.get_idn()['model'] == '2400':
                if self.instr.mode() == 'CURR':
                    self.instr.rangei(value)
                else:
                    self.instr.rangev(value)
            else:
                self.instr.source.range(value)
        
    def sweep_to(self,ste,val):
        value = float(val.text())
        step = float(ste.text())
        if 'keithley' in str(self.instr):
            if self.instr.get_idn()['model'] == '2400':
                if self.instr.mode()=='CURR':
                    for i in np.linspace(self.instr.curr(),value,step):
                        self.instr.curr(i)
                        QTest.qWait(0.1*1000)
                else:
                    for i in np.linspace(self.instr.volt(),value,step):
                        self.instr.volt(i)
                        QTest.qWait(0.1*1000)
            else:
                if self.instr.source.function()=='current':
                    for i in np.linspace(self.instr.source.current(),value,step):
                        self.instr.source.current(i)
                        QTest.qWait(0.1*1000)
                else:
                    for i in np.linspace(self.instr.source.voltage(),value,step):
                        self.instr.source.voltage(i)
                        QTest.qWait(0.1*1000)
