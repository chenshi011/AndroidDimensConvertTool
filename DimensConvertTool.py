#!/usr/local/bin/python2.7
# -*- coding:utf-8 -*- 
'''
@author:     cs
'''
import os

import XMLEdit


class DimensConvertTool():  
    def __init__(self, outDir, resources="dimensions.xml"):  
        print outDir
        self.DEBUG = False;
        self.outDir = outDir
        self.resources = resources
    def getOutDir(self):
        return str(self.outDir)  
    def convert(self, targetW, targetH, designW=1072, designH=1448):
        if not os.path.exists(self.resources):
            return False
        try:
            if not os.path.exists(self.outDir):
                os.makedirs(self.outDir)
            basename = os.path.basename(self.resources).split(".")[0]
            file_out = "%s/%s-%sx%s.xml" % (self.outDir, basename, targetH, targetW)
            XREG = r'x(.+)'
            YREG = r'y(.+)'
            xScale = float(targetW * 1.0 / designW);
            yScale = float(targetH * 1.0 / designH);
            tree = XMLEdit.read_xml(self.resources)
            dimens = XMLEdit.find_nodes(tree, "dimen")
            findW = 0
            findH = 0
            total = 0
            findBoth = 0
            nomatchs = []
            for dimen in dimens:
                px = float(dimen.text.split("px")[0])   
                if self.DEBUG:
                    print px 
                if XMLEdit.contains(str(dimen.attrib["name"]), XREG):
                    findW = findW + 1
                    if self.DEBUG:
                        print "findW:%s" % findW
                    dimen.text = "%.2fpx" % float(px * xScale)
                elif XMLEdit.contains(dimen.attrib["name"], YREG):
                    findH = findH + 1
                    if self.DEBUG:
                        print "findH:%s" % findH
                    dimen.text = "%.2fpx" % float(px * yScale)
                else:
                    dimen.text = "%.2fpx" % float(px * xScale)
                    nomatchs.append(dimen.attrib["name"])   
                    total = total + 1
            if self.DEBUG:    
                print "total:%d,findW:%d,findH:%d,findBoth:%d,nomatch:%d" % (total, findW, findH, findBoth, (total - findW - findH))
            if len(nomatchs) > 0:
                print "-----------nomatchs-----------"
            for nomatch in nomatchs:
                print nomatch
            XMLEdit.write_xml(tree, file_out)    
            return True        
        except:
            print "error"
            return False
        finally:
            return True        
