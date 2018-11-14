import sys
import os
import subprocess

import file as jsf
import run_all 
import run_qgraf 
import generate_form 
import run_form 
import matchmaker.functions as func
from timeit import default_timer as timer

def match_model(dir):
    print sys.argv
    if len(sys.argv)==2:
        NPmodeldir=jsf.proper_dir_path(dir)
        inputfiledir='../input/'
        modeldir='../models/'
        print modeldir

        inputfilelist=['new_input_L2.dat','new_input_L4.dat','new_input_0F.dat','new_input_2F_0S_3D.dat','new_input_2F_1S_2D.dat','new_input_2F_2S_1D.dat','new_input_2F_3S_0D.dat','new_input_4F_LLLL.dat','new_input_4F_LLRR_LRRL.dat','new_input_4F_LRLR.dat','new_input_4F_RRRR.dat']
        effmodeldir=['L2SM/','L4SM/','L6SM_0F/','L6SM_2F_0S_3D/','L6SM_2F_1S_2D/','L6SM_2F_2S_1D/','L6SM_2F_3S_0D/','L6SM_4F_LLLL/','L6SM_4F_LLRR_LRRL/','L6SM_4F_LRLR/','L6SM_4F_RRRR']
        if os.path.isdir(modeldir+NPmodeldir):
            for ipart,partfile in enumerate(inputfilelist):
                run_all.run_all(inputfiledir+partfile,modeldir+effmodeldir[ipart])
                run_all.run_all(inputfiledir+partfile,modeldir+NPmodeldir)
        else:
            print "Model directory "+modeldir+" does not exist"
    else:
        print "usage: python match_model.py NPmodeldirectory"


if __name__=='__main__':

    start = timer()
    if len(sys.argv)==2:
        print sys.argv  
        dir=sys.argv[1]
        #modeldir=sys.argv[2]
        match_model(dir)
    else:
        print "usage: python match_model.py NPmodeldirectory"
    end = timer()
    print "time taken ",end-start, " seconds "
        
