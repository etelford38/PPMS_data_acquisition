"""
#Authors: Written by Maelle Kapfer (mak2294@columbia.edu) and modified by Jordan Pack (j.pack@columbia.edu), Evan Telford (ejt2133@columbia.edu), and Christie Koay (csk2172@columbia.edu)
#Latest-update: April 27 2023
"""
from PPMS_Instrument_Classes import SR860_inst, K2450_inst, K6221_inst, K6517B_inst, Dynacool_inst

class Instruments:
    
    def __init__(self):
        self.dic={}
        self.list_names=[];self.list_instr=[];self.list_gpib=[];self.list_ch=[]
        self.instr=[]
        self.lockins=[]
        self.not_lockins=[]
        self.read_file()
        for ind in range(len(self.list_names)):
            gpib='GPIB0::'+self.list_gpib[ind]+'::INSTR'
            if self.list_instr[ind]=='SR860':
                li860=SR860_inst(self.list_names[ind],gpib,self.list_ch[ind])
                self.instr.append(li860)
                self.lockins.append(li860)    
            elif self.list_instr[ind]=='Keithley 2450':
                k=K2450_inst(self.list_names[ind],gpib,self.list_ch[ind])
                self.instr.append(k)
                self.not_lockins.append(k)
            elif self.list_instr[ind]=='Keithley 6221':
                k=K6221_inst(self.list_names[ind],gpib,self.list_ch[ind])
                self.instr.append(k)
                self.lockins.append(k)
            elif self.list_instr[ind]=='Keithley 6517B':
                k=K6517B_inst(self.list_names[ind],gpib,self.list_ch[ind])
                self.instr.append(k)
                self.lockins.append(k)
            elif self.list_instr[ind]=='Dynacool':
                k=Dynacool_inst(self.list_names[ind],gpib,self.list_ch[ind])
                self.instr.append(k)
                self.lockins.append(k)
            else:
                pass
        self.hdr=self.header()

    def header(self):
        hdr=[]
        for inst in self.instr:
            hdr.extend(inst.header())
        return hdr
    
    def measure(self):
        msmt=[]
        for inst in self.instr:
            msmt.extend(inst.measure())
            
        return msmt
    
    def read_file(self):
        with open('Instruments.txt', 'rt') as f:
            for line in f:
                if line.startswith('Name')==True:
                    self.list_names.append(line.split('=')[1].rstrip())
                elif line.startswith('Instrument')==True:
                    self.list_instr.append(line.split('=')[1].rstrip())
                elif line.startswith('GPIB')==True:
                    self.list_gpib.append(line.split('=')[1].rstrip())
                elif line.startswith('channels')==True:
                    self.list_ch.append(line.split('=')[1].rstrip())
                else:
                    pass
                
    def get_instr(self, name):
        return self.instr[self.list_names.index(name)]
        
