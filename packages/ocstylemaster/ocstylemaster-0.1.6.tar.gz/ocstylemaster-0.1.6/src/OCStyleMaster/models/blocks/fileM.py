# -*- coding:utf-8 -*-

import os
from OCStyleMaster.models.blocks.base import *

class FileM(File):

    def __init__(self, filePath):
        super(FileM, self).__init__(filePath)
        self.funCount = 0
        self.totalFuncLineCount = 0


    def analyze(self):
        for child in self.children:
            child.analyze()

        self.__analyze_all_func_line_count()

    def __analyze_all_func_line_count(self):
        fCount,lCount = self.__get_child_func_line_count(self)
        self.funCount = fCount
        self.totalFuncLineCount = lCount


    def __get_child_func_line_count(self,obj):
        import OCStyleMaster.models.blocks.funcM as funcM
        fCount = 0
        lCount = 0
        for child in obj.children:
            if isinstance(child,funcM.FuncM):
                fCount += 1
                lCount += child.line_count()
            cfCount,clCount = self.__get_child_func_line_count(child)
            fCount+=cfCount
            lCount+=clCount
        return fCount,lCount


    def output_all_errors(self):
        """
        输出 错误
        :return:
        """
        errors = sorted(self.errors,key = lambda obj:obj.start)
        if GlobalData().fileHandler is None:
            averageLineCount = 0
            if self.funCount > 0:
                averageLineCount = self.totalFuncLineCount/self.funCount
                averageLineCount = round(averageLineCount,2)
            print("[{}] Function Count : {}; Average Function Line Count {}".format(self.filename,self.funCount,averageLineCount))
            for e in errors:
                print(e)
        else:
            h = GlobalData().fileHandler
            file = "[{}]\n".format(self.filename)
            h.write(file)
            for e in errors:
                string = str(e) + "\n"
                h.write(string)
            h.flush()