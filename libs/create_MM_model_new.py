import file as jsf
#import UFO2MM
import matchmaker.functions as func
import os
import sys
import subprocess
import glob
import shutil
import textwrap

class DontDoIt(Exception): pass

def guess_group(groupname):
    groups=['su'+str(t+2) for t in range(18)]
    groups+=['so'+str(t+2) for t in range(18)]
    migroupname=groupname.lower()
    guess=[x for x in groups if x in migroupname]
    if len(guess)==1:
        return guess[0]
    else:
        return ''


    
def GroupData(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    newlines=[l.split() for l in lines]
    for (i,nl) in enumerate(newlines):
        if len(nl) == 1:
            newlines[i].extend(['u1'])
        elif len(nl) == 2:
            nonabeliangroup=raw_input("which gauge group is "+nl[0]+"? ["+guess_group(nl[0])+"]  :")
            if nonabeliangroup=="":
                nonabeliangroup=guess_group(nl[0])
            newlines[i].extend([nonabeliangroup])
        newlines[i].extend("\n")
    with open(filename+"new",'w') as f:
        for nl in newlines:
            f.write('  '.join(nl))

def create_model(MMmodelname,modelname):

    #modelspre=func.get_path('models')+"/"
    #corepre=func.get_path('core')+"/"
    modelspre='../models/'
    corepre='../core/'

    modeldir=modelspre+modelname+'/'
    if os.path.isdir(modeldir):
        raise DontDoIt("Model directory "+modeldir+" already present")
    if not os.path.isdir(MMmodelname):
        raise DontDoIt("MM Model "+MMmodelname+" not present")
    shutil.copytree(MMmodelname,modeldir+"QGRAF/")
    if not os.path.isdir(modeldir+"QGRAF"):
        os.makedirs(modeldir+"QGRAF")
    os.makedirs(modeldir+"QGRAF/proc_0loop")
    os.makedirs(modeldir+"FORM")
    os.makedirs(modeldir+"FORM/proc_0loop")

    GroupData(modeldir+"QGRAF/model_data/gaugedata")
    if not os.path.isdir(modeldir+"QGRAF/model_data"):
        os.makedirs(modeldir+"QGRAF/model_data")

    #UFO2MM.UFO2MM(UFOmodelname,modeldir+"QGRAF/")
    with open(modeldir+"QGRAF/model_data/listheavy") as f:
        linesheavy = f.read().strip()
    with open(modeldir+"QGRAF/model_data/listlight") as f:
        lineslight = f.read().strip()
    with open(modeldir+"QGRAF/model_data/listbackgroundvectors") as f:
        linesbackground = f.read().strip()
    #os.makedirs(modeldir)
    #for fls in glob.glob("model*"):
        #shutil.move(fls, modeldir+"QGRAF/")
    shutil.copy(corepre + "limpia.sh", modeldir+"FORM/proc_0loop/")
    #shutil.copy(corepre + "colour.faux", modeldir+"FORM/proc_0loop/")
    myrepl= ('MASSLESSPARTICLES',textwrap.fill(lineslight,width=50)),('MASSIVEPARTICLES',textwrap.fill(linesheavy,width=50)),('BACKGROUNDPARTICLES',textwrap.fill(linesbackground,width=50))
    #print linesmassless
    jsf.dress_skeleton(myrepl, corepre + 'qgraf.skeleton.0loop.dat',modeldir+"QGRAF/qgraf.skeleton.0loop.dat")


    if len(linesheavy)>0:        
        os.makedirs(modeldir+"QGRAF/proc_1loop")
        os.makedirs(modeldir+"FORM/proc_1loop")
        jsf.dress_skeleton(myrepl, corepre + 'qgraf.skeleton.1loop.dat',modeldir+"QGRAF/qgraf.skeleton.1loop.dat")
        shutil.copy(corepre + "limpia.sh", modeldir+"FORM/proc_1loop/")
        #shutil.copy(corepre + "colour.faux", modeldir+"FORM/proc_1loop/")

    # Run usesusyno
    usesusyno=raw_input("Do you want to use SusyNo to compute the gauge couplings? [Y/n]")
    #print "usesusyno=",usesusyno
    if len(usesusyno)==0 or usesusyno[0] in ["","y","Y"]:    
        myrepl= ('MODEL_NAME',modelname),('MASSIVEPARTICLES','MASSIVEPARTICLES')
        jsf.dress_skeleton(myrepl, corepre + 'usesusyno.skeleton.m',"./usesusyno.m")
        subprocess.call("math -run -noprompt < usesusyno.m",shell=True)
        if os.path.exists("usesusyno.m"):
            os.remove("usesusyno.m")

def create_MM_model_new():

    if len(sys.argv)==3:
        try:
		    create_model(sys.argv[1],sys.argv[2])
        except DontDoIt as e:
            print(e.args[0])
    else:
        print "usage: python create_model_from_FR9.py NPFRmodelname modelname"
        print "NPFRmodelname is a FR .fr model file to add to the SM, with Lagrangian LNP"
        print "modelname is the name of the directory to create in models"


if __name__=='__main__':

    if len(sys.argv)==3:
        try:
		    create_model(sys.argv[1],sys.argv[2])
        except DontDoIt as e:
            print(e.args[0])
    else:
        print "usage: python create_model_from_FR9.py NPFRmodelname modelname"
        print "NPFRmodelname is a FR .fr model file to add to the SM, with Lagrangian LNP"
        print "modelname is the name of the directory to create in models"


