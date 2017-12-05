#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*- 
'''
@author:     cs
'''
from Tkconstants import LEFT, END, RIGHT, Y, BOTH, BOTTOM, TOP, EXTENDED
from Tkinter import Label, Entry, Listbox, Button, Frame, Canvas, \
    Scrollbar
import os
import threading
import tkMessageBox
from xml.dom.minidom import Document

import XMLEdit


class Design():  
    def __init__(self, conf, rowindex, Widget, fontSize , devices={}):  
        self.conf = conf
        self.rowindex = rowindex;
        self.Widget = Widget
        self.fontSize = fontSize
        self.devices = devices
        self.doc = None
        self.devicesFName = "devices.xml"
    def get(self):
        return self.devices   
    def layout(self):
        canvas = Canvas(self.Widget, width=400, height=10)
        canvas.create_line(10, 2, 400, 2, fill='black', tags="line")
        self.rowindex = self.rowindex+1
        canvas.grid(row=self.rowindex, column=1, columnspan=4) 
        lblTarget = Label(self.Widget, text=self.conf.get("TargetDeviceName", "title", "目标设备"), font=self.fontSize)  
        lblTarget.grid(row=self.rowindex, column=1, columnspan=4)   
        lblTargetW = Label(self.Widget, text=self.conf.get("TargetDeviceName", "width", "宽度（px）"), font=self.fontSize) 
        self.rowindex = self.rowindex+1 
        lblTargetW.grid(row=self.rowindex, column=1)   
        entryTargetW = Entry(self.Widget, width=10, font=self.fontSize)  
        entryTargetW.grid(row=self.rowindex, column=2)  
        self.entryTargetW = entryTargetW
        lblTargetH = Label(self.Widget, text=self.conf.get("TargetDeviceName", "height", "高度（px）"), font=self.fontSize)  
        lblTargetH.grid(row= self.rowindex, column=3)   
        entryTargetH = Entry(self.Widget, width=10, font=self.fontSize)  
        entryTargetH.grid(row = self.rowindex, column=4)     
        self.entryTargetH = entryTargetH
        fmBox = Frame(self.Widget)
        scrollbar = Scrollbar(fmBox)  
        scrollbar.pack(side=RIGHT, fill=Y)
        lb = Listbox(fmBox, yscrollcommand=scrollbar.set, width = 25, selectmode = EXTENDED)
        lb.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=lb.yview)  
        self.rowindex = self.rowindex + 1
        fmBox.grid(row= self.rowindex, column=1, columnspan=2)   
        self.lb = lb;
        fmOper = Frame(self.Widget)
        fmAdd = Frame(fmOper, pady=10)
        btAdd = Button(fmAdd, text="添加", command=self.processAdd)  
        btAdd.pack()
        fmDel = Frame(fmOper, pady=10)
        btDel = Button(fmDel, text="删除", command=self.processDel)  
        btDel.pack()
        fmAdd.pack(side=TOP)
        fmDel.pack(side=BOTTOM)
        fmOper.grid(row= self.rowindex, column=3)  
        canvas = Canvas(self.Widget, width=400, height=10)
        canvas.create_line(10, 2, 400, 2, fill='black', tags="line")
        self.rowindex =  self.rowindex + 1
        canvas.grid(row= self.rowindex, column=1, columnspan=4)
        self.readDefDevice()
        return self.rowindex
    def readDefDevice(self):
        if os.path.exists(self.devicesFName):
            elementTree = XMLEdit.read_xml(self.devicesFName)
            devicesXml = XMLEdit.find_nodes(elementTree, "device")
            for de in devicesXml:
                self.addDevice(int(de.attrib["width"]), int(de.attrib["height"]))
        #add default
        if len(self.devices) == 0:
            self.addDevice(758, 1024)
            self.addDevice(600, 800)        
    def addDevice(self, width, height):
	item = {"width":width, "height":height}
        item_lb = self.getDictKey(width, height)
        self.devices[item_lb] = item
        self.entryTargetW.delete(0, END)
        self.entryTargetW.insert(0, width)
        self.entryTargetH.delete(0, END)
        self.entryTargetH.insert(0, height)
        self.TargetW = width
        self.TargetH = height
        self.lb.insert(END, item_lb)
        thread = threading.Thread(target= self.addDeviceThread, args=(width, height,))
        thread.start()
        thread.join()
    def addDeviceThread(self, width, height):
        if not self.doc:
            self.doc = Document()
            self.devicesDoc = self.doc.createElement('devices') 
            self.doc.appendChild(self.devicesDoc)  
        deviceDoc = self.doc.createElement('device')
        deviceDoc.setAttribute('width', str(width))
        deviceDoc.setAttribute('height',str(height))
        self.devicesDoc.appendChild(deviceDoc)
        with open('devices.xml','w+') as f:
            self.doc.writexml(f,newl = '\n', addindent = '\t',encoding='utf-8')
        print self.devices
        return item_lb  
    def getDeviceIndex(self, width, height):
        item_lb = self.getDictKey(width, height)
        print self.devices.get(item_lb, -1)
        return self.devices.get(item_lb, -1)   
    def getDictKey(self, width, height):
        return "%sx%s" % (str(height), str(width)) 
    def processAdd(self):  
        width = int(self.entryTargetW.get())
        height = int(self.entryTargetH.get())
        if self.getDeviceIndex(width, height) >= 0:
            tkMessageBox.showwarning("提示", "目标尺寸已经存在！");    
        else:
            self.addDevice(width, height)
            print self.devices
    def processDel(self):  
        if len(self.lb.curselection()) == 0:
            tkMessageBox.showwarning("提示", "未选中需要删除的目标尺寸！");   
        else:    
            for index in self.lb.curselection():
                self.devices.pop( self.lb.get(index))
            self.lb.delete(self.lb.curselection())
            print self.devices
