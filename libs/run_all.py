import sys
import os
import subprocess

import file as jsf
import run_qgraf
import generate_form
import run_form
import matchmaker.functions as func
from timeit import default_timer as timer



def run_all(inputfile,modeldir0):

    modeldir=jsf.proper_dir_path(modeldir0)
    if os.path.isfile(inputfile):
        if os.path.isdir(modeldir):
            # Run QGRAF
            run_qgraf.run_qgraf(inputfile,modeldir)
            # Generate Form
            generate_form.generate_form(modeldir)
            # Run Form
            run_form.run_form(modeldir)
        else:
            print "Model directory "+modeldir+" does not exist"
    else:
        print "Input file "+inputfile+" does not exist"


if __name__=='__main__':

    start = timer()
    if len(sys.argv)==3:
        print sys.argv  
        inputfile=sys.argv[1]
        modeldir=sys.argv[2]
        run_all(inputfile,modeldir)
    else:
        print "usage: python run_all.py inputfile modeldirectory"
    end = timer()
    print "time taken ",end-start, " seconds "
