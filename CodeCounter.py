#coding=UTF-8

import sys,os,os.path
import re
count=0
filters=['java']


def input():
    global destDir
    destDir = raw_input("input dest dir:")
    destDir = destDir.strip()
    if destDir=="":
        destDir=os.curdir


def listFile(destDir):
    '''
    列出所给目录的文件，如果是文件，计算，如果是文档继续调用listFile
    '''
    global count
    if os.path.isdir(destDir)!=True:
        #过滤
        if filter(destDir) == False:
            return  
        if os.path.isfile(destDir):
            count=count+countRows(destDir)
        return
    files = os.listdir(destDir)
    for i in range(len(files)):
        listFile(os.path.join(destDir,files[i]))

def countRows(filePath):

    '''
    计算行数
    '''
    fscok=open(filePath)

    nullLineP=re.compile(r'^(\t{1,}|\n{1,}|\s{1,})$')
    singleNoteP=re.compile(r'^(\t{0,}|\s{0,})//')
    multiNoteStartP=re.compile(r'^(\t{0,}|\s{0,})(/\*)')
    multiNoteEndP=re.compile(r'(\*/)(\t{0,}|\s{0,}|\n{0,})$')
    c=0
    isMulitNoteStart=False
    for line in fscok:
        #匹配空白行
        if nullLineP.match(line)!=None :
            continue

        #匹配单行注释
        if singleNoteP.match(line)!=None:
            continue

        #匹配多行注释开始
        if multiNoteStartP.match(line)!=None:
            isMulitNoteStart=True

        #匹配多行注释结束
        #如果有开始的注释，但是没有结束的，则continue
        if isMulitNoteStart==True and multiNoteEndP.search(line)==None:
            continue
        if multiNoteEndP.search(line) !=None:
           isMulitNoteStart=False 
           continue

        c+=1

    return c


def filter(filePath):
    '''
    过滤文件
    '''
    global filters
    exName=filePath.split('.')[-1]
    if exName in filters :
        return True
    return False

if __name__=="__main__":
    input()
    listFile(destDir)
    print "%d row" % count
