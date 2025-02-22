import maya.cmds as cmds

import os

import sys

from functools import partial

import maya.mel as mel



MAYA_SEP = '/'



def correctSysPath():

    for i, path in enumerate(sys.path):

        if path[-1] in (MAYA_SEP, os.sep, os.altsep):

            sys.path[i] = sys.path[i][:-1]



correctSysPath()



def deleteOldAutoSaves():

    import maya.cmds as cmds

    import time

    import os.path, time

    

    

    save = cmds.autoSave(q = True, enable = True)

    destDir = cmds.autoSave(q = True, destinationFolder = True)

    deleteDays = 3

    

    if save:

        now = time.time()

        fileCap = now - 60*60*24*deleteDays

    

        files = os.listdir(destDir)

        

        for file in files:

            fileCreation = os.path.getctime(os.path.join(destDir, file))

            if fileCreation < fileCap:

                os.remove(os.path.join(destDir, file))

                

                

def mayaToolsInstall_UI():

    

    if cmds.window("mayaToolsInstall_UI", exists = True):

        cmds.deleteUI("mayaToolsInstall_UI")

        

    window = cmds.window("mayaToolsInstall_UI", w = 300, h = 100, title = "Maya Tools Install", mnb = False, mxb = False)

    

    mainLayout = cmds.columnLayout(w = 300, h = 100)

    formLayout = cmds.formLayout(w = 300, h = 100)

    

    text = cmds.text(label = "ERROR: Could not find Maya Tools directory.\n Please locate folder using the \'Browse\' button.", w = 300)

    cancelButton = cmds.button(label = "Cancel", w = 140, h = 50, c = mayaToolsInstall_Cancel)

    browseButton = cmds.button(label = "Browse", w = 140, h = 50, c = mayaToolsInstall_Browse)

    

    cmds.formLayout(formLayout, edit = True, af = [(text, 'left', 10), (text, 'top', 10)])

    cmds.formLayout(formLayout, edit = True, af = [(cancelButton, 'left', 5), (cancelButton, 'top', 50)])

    cmds.formLayout(formLayout, edit = True, af = [(browseButton, 'right', 5), (browseButton, 'top', 50)])

    

    cmds.showWindow(window)

    cmds.window(window, edit = True, w = 300, h = 100)

    

    

    

def mayaToolsInstall_Cancel(*args):

    

    cmds.deleteUI("mayaToolsInstall_UI")

    cmds.warning("Maya Tools will not be setup")

    





def mayaToolsInstall_Browse(*args):

    

    mayaToolsDir = cmds.fileDialog2(dialogStyle = 2, fileMode = 3)[0]



    #confirm that this is actually the maya tools directory

    if mayaToolsDir.rpartition("/")[2] != "MayaTools":

        cmds.warning("Selected directory is not valid. Please locate the MayaTools directory.")

        

        

    else:

        cmds.deleteUI("mayaToolsInstall_UI")

        

        #create file that contains this path

        path = cmds.internalVar(usd = True) + "mayaTools.txt"

        

        f = open(path, 'w')

        f.write(mayaToolsDir)

        f.close()

        

        

        #run setup

        cmds.file(new = True, force = True)

        

        

        

def mayaTools():

    

    #import custom maya setup script

    print cmds.internalVar(usd = True)

    print cmds.internalVar(upd = True)

    path = cmds.internalVar(usd = True)

    path = path + "mayaTools.txt"

    print path

    

    if os.path.exists(path):

        f = open(path, 'r')

        

        mayaToolsDir = f.readline()

        if not os.path.exists(mayaToolsDir):

            mayaToolsInstall_UI()

        

        path = mayaToolsDir + "/General/Scripts"

        pluginPath = mayaToolsDir + "/General/Plugins"

        

        #look in sys.path to see if path is in sys.path. if not, add it

        if not path in sys.path:

            sys.path.append(path)

            

            

        #run setup

        import customMayaMenu as cmm

        cmm.customMayaMenu()

        #cmds.file(new = True, force = True)

    

    

    else:

        mayaToolsInstall_UI()

        

        



def launchCustomFileLister():

    import customFileLister

    reload(customFileLister)

    customFileLister.UI()

    

    



#setup script jobs

scriptJobNum = cmds.scriptJob(event = ["NewSceneOpened", launchCustomFileLister ] )

scriptJobNum2 = cmds.scriptJob(event = ["NewSceneOpened", mayaTools])





