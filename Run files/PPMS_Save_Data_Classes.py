"""
#Authors: Written by Maelle Kapfer (mak2294@columbia.edu) and modified by Jordan Pack (j.pack@columbia.edu), Evan Telford (ejt2133@columbia.edu), and Christie Koay (csk2172@columbia.edu)
#Latest-update: April 27 2023
"""

import numpy as np
import datetime
import os

class Savetxt:
    def __init__(self,head,title,directory,notes):
        self.notes = notes
        self.head = head
        self.title = title
        self.directory = directory
        self.full_title = self.directory + '/'  + self.title + '.dat' #+ datetime.datetime.now().strftime("%y%m%d_%H") + 'h'
        if os.path.exists(self.full_title):
            mod=1
            while os.path.exists(self.full_title):
                self.full_title=self.directory + '/' +  self.title +'_'+str(mod)+ '.dat' #datetime.datetime.now().strftime("%y%m%d_%H") + 'h' +
                mod=mod+1
        df=open(self.full_title,'w')
        df.write(self.notes+'\n')
        df.write(self.head+'\n')
        df.close()
        
    def save_txt(self,X,Y):
        data = np.column_stack((X,Y))
        return np.savetxt(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d_%H") + 'h' + self.title + '.dat', data, header=self.head,comments='',delimiter=',')

    def save_txt3D(self,X,A, Y):
        data = np.column_stack((X,A,Y))
        return np.savetxt(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d_%H") + 'h' + self.title + '.dat', data, header=self.head,comments='',delimiter=',')

    def save_line(self,dat):
        df=open(self.full_title,'a')
        line=",".join(dat)+'\n'
        df.write(line)
        df.close()
    
    def save_txt_mean(self,X,Y,err):
        data = np.column_stack((X,Y,err))
        return np.savetxt(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d_%H") + 'h' + self.title + '.dat', data, header=self.head,comments='',delimiter=',')

    def save_txt_all(self,param):
        i=0;data=[]
        while i<len(param):
            data.append((param[i]))
            i+=1
        data=np.transpose(data)
        return np.savetxt(self.directory + '/' + datetime.datetime.now().strftime("%y%m%d_%H") + 'h' + self.title + '.dat', data, header=self.head,comments=self.notes+'\n',delimiter=',')
