#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*- 
'''
@author:     cs
'''
from Tkinter import Tk, Frame, Button, Label, Entry, Menu
import os
import platform
import threading
import tkFileDialog
import tkMessageBox

import ConfigUtils
import DimensConvertTool
from widget import DesignDevice, TargetDevice


class Form:  
    def __init__(self):  
        self.window = Tk()                
        self.window.title("Dimens Convert Tool")  
        windowW = 420  
        if(platform.system() =="Windows"):
            windowW = 420  
        else:
            windowW = 480      
        self.window.minsize(windowW, 355)  
        self.center_wind(self.window, windowW, 355)
        frame = Frame(self.window)
        frame.pack()    
        config_path = os.path.split(os.path.realpath(__file__))[0] + "/" + "configs.ini"
        self.rootDir = os.path.split(os.path.realpath(__file__))[0] 
        self.config_path = config_path
        conf = ConfigUtils.Config(config_path);
        self.conf = conf
        fontSize = 35;
        menubar = Menu(self.window)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="使用方法",command=self.help) 
        helpmenu.add_separator()
        helpmenu.add_command(label="关于", command=self.about)
        menubar.add_cascade(label="帮助", menu=helpmenu)
        self.window.config(menu=menubar)
        index = 0
        designDevice = DesignDevice.Design(conf, index, frame, fontSize, self.rootDir);
        index = designDevice.layout();
        self.designDevice = designDevice
        targetDevice = TargetDevice.Design(conf, index, frame, fontSize);
        index = targetDevice.layout();
        self.targetDevice = targetDevice
        btApply = Button(frame, text="生成", command=self.processButtonGeneral)  
        btApply.grid(row=index+1, column=1, columnspan=2)   
        btCancel = Button(frame, text="取消", command=self.processButtonCancel)  
        btCancel.grid(row=index+1, column=2, columnspan=2)   
        # 监测事件直到window被关闭  
        self.window.mainloop()
    def center_wind(self, window, w=300, h=200):
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        # calculate position x, y
        x = (ws / 2) - (w / 2)   
        y = (hs / 2) - (h / 2)
        window.geometry('%dx%d+%d+%d' % (w, h, x, y))
           
    def layout_input(self, frame, keys):
        fontSize = 33
        index = 1
        WIDTH = 60
        button_opt = {'padx': 5}  
        for key in keys:
            lbl = Label(frame, text=key[1], font=fontSize)  
            entry = Entry(frame, textvariable=key[2], width=WIDTH, font=fontSize)  
            if len(key) == 5 and key[4] == 1:
                btn = Button(frame, text="选择", command=lambda key=key: self.processChooseFile(key))
            else:
                btn = Button(frame, text="选择", command=lambda key=key: self.processChooseDir(key))  
            lbl.grid(row=index, column=1, sticky='e')  
            entry.grid(row=index, column=2)  
            btn.grid(row=index, column=3, **button_opt)  
            index = index + 1
            
    def processChooseDir(self, key):  
        sel_dir = tkFileDialog.askdirectory(**key[3])
        if sel_dir != '':
            key[2].set(sel_dir) 
            self.conf.write_config(key[0], "value", sel_dir)       
            
    def processChooseFile(self, key):  
        sel_fil = tkFileDialog.askopenfilename(**key[3])
        if sel_fil != '':
            key[2].set(sel_fil)        
            self.conf.write_config(key[0], "value", sel_fil)      
    def mkdirIfnotexists(self, dir_path):  
        if not os.path.exists(dir_path):
            print "%s is not exists mkdir" % dir_path
            os.mkdir(dir_path)      
    def doConvert(self, tool, width, height):  
        tool.convert(width,height)           
    def processButtonGeneral(self):  
        if not os.path.exists(self.designDevice.getResourcesFile()):
            tkMessageBox.showwarning("提示", "源文件不存在！")
        else:      
            try:
                tool = DimensConvertTool.DimensConvertTool("%s\%s" % (self.designDevice.getOutDir(), "out-xmls"), self.designDevice.getResourcesFile());
                devices = self.targetDevice.get();
                for name in devices:
                    thread = threading.Thread(target= self.doConvert, args=(tool, devices[name]["width"],devices[name]["height"],))
                    thread.start()
                    thread.join()
                tkMessageBox.showinfo("消息", "生成成功,文件路径：\n%s\\" % (tool.getOutDir()));
            except:
                tkMessageBox.showerror("错误", "生成失败，请检查源文件是否存在");     
    def processButtonCancel(self):
        self.window.quit()
    def help(self): 
        tkMessageBox.showinfo("消息", '1.输入修改设计尺寸；\n2.添加删除来增加或者删除设备；\n3.生成的文件默认保存在out-xmls文件夹下面;\n 本程序默认保存上一次的修改，具体可看目录下生成的文件，亦可直接修改配置文件\n示例xml：\n<?xml version="1.0" encoding="utf-8"?>\n<resources>\n  <dimen name="x1">1px</dimen>\n</resources>') 
    def about(self): 
        tkMessageBox.showinfo("欢迎", "Designed By WaveWaveWave")

if __name__ == "__main__":      
    Form()