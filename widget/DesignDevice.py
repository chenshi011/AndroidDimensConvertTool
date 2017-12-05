#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*- 
'''
@author:     cs
'''
from Tkinter import Label, IntVar, Entry, StringVar, Button
import os
import tkFileDialog


class Design():  
    def __init__(self, conf, rowindex, Widget, fontSize, rootDir= None):  
        self.Widget = Widget;
        self.fontSize = fontSize;
        self.conf = conf;
        self.rowindex = rowindex;
        self.file_opt = options = {}  
        self.rootDir = rootDir
        if not rootDir:
            self.rootDir = os.path.split(os.path.realpath(__file__))[0] 
        options['defaultextension'] = '.xml'  
        options['filetypes'] = [('xml files', '.xml')]  
    def getRowindex(self):  
        return self.rowindex 
    def processChooseFile(self, options):  
        sel_fil = tkFileDialog.askopenfilename(**options)
        if sel_fil != '':
            self.DesinRes.set(sel_fil)
            self.conf.set("DesignResources", "value", sel_fil)   
    def getOutDir(self): 
        return os.path.dirname(self.getResourcesFile())         
    def getResourcesFile(self): 
        return self.DesinRes.get()        
    def layout(self):
        self.rowindex = self.rowindex + 1
        fileName = self.conf.get("DesignResources", "title", "xml源文件")
        lblDesinRes = Label(self.Widget, text=fileName, font=self.fontSize)  
        lblDesinRes.grid(row=self.rowindex, column=1)   
        self.DesinRes = StringVar(value = self.conf.get("DesignResources", "path",  "%s\%s" % (self.rootDir ,"dimensions.xml")))
        entryDesinRes = Entry(self.Widget, textvariable=self.DesinRes, font=self.fontSize, width=25)  
        entryDesinRes.grid(row=self.rowindex, column=2, columnspan= 2)  
        self.file_opt['initialfile'] = self.DesinRes.get()
        self.file_opt['title'] = "选择%s" % fileName  
        entryDesinRes = Button(self.Widget, text="选择", command=lambda options= self.file_opt: self.processChooseFile(options))
        entryDesinRes.grid(row=self.rowindex, column=4, columnspan= 1)  
        lblDesinW = Label(self.Widget, text=self.conf.get("DesignWidth", "title", "设计宽度（px）"), font=self.fontSize)  
        self.rowindex = self.rowindex + 1
        lblDesinW.grid(row=self.rowindex, column=1)   
        self.DesinW = IntVar(value = self.conf.get("DesignWidth", "value", 1072))
        entryDesinW = Entry(self.Widget, textvariable=self.DesinW, font=self.fontSize, width = 35)  
        entryDesinW.grid(row=self.rowindex, column=2, columnspan= 3)  
        
        self.rowindex = self.rowindex + 1
        lblDesinH = Label(self.Widget, text=self.conf.get("DesignHeight", "title", "设计高度（px）"), font=self.fontSize)  
        lblDesinH.grid(row=self.rowindex, column=1)   
        self.DesinH = IntVar(value=self.conf.get("DesignHeight", "value", 1448))
        entryDesinH = Entry(self.Widget, textvariable=self.DesinH, font=self.fontSize, width = 35)  
        entryDesinH.grid(row=self.rowindex, column=2, columnspan= 3)    
        return self.rowindex
