import subprocess
import glob
import sys
import os
import re
import file as jsf

def better_log(file,indexlist):
    #print file
    if not os.path.isfile(file+".mat"):
        with open(file) as f:
            lines = f.read().splitlines()
            for i,li in enumerate(lines):
                if "ampl" in li:
                    i0=i;
                if ";" in li:
                    i1=i;
        lin=''.join([x.strip() for x in  lines[i0:i1+1]])
        lin=lin.replace("e_","ee")
        lin=re.sub(r'd_\(([0-9a-zA-Z]*),([0-9a-zA-Z]*)\)', r'dd[\1,\2]', lin)
        # for i in range(200):
        #     for j in range(200):
        #         for ind in indexlist.replace(" ","").split(","):
        #             print 'ind=',ind
        #             inds=str(ind)
        #             lin=lin.replace("d_("+ind+ind+str(i+1)+","+ind+ind+str(j+1)+")","dd["+ind+ind+str(i+1)+","+ind+ind+str(j+1)+"]")
        #             lin=lin.replace("d_("+ind+str(i+1)+","+ind+str(j+1)+")","dd["+ind+str(i+1)+","+ind+str(j+1)+"]")
        #print lin
        with open(file+".mat","w") as ff:
            ff.write(lin)

def read_new_indices(dirname):
    # define new parameters
    with open(dirname+'QGRAF/model_data/newindices','r') as f:
        all_lines = f.readlines()
    #print "YEYEYE",', '.join([x.replace('\n','') for x in all_lines])
    return ', '.join([x.split("=")[0] for x in all_lines])
    #return ', '.join([x.replace('\n','') for x in all_lines])


def run_form(dirname0):
    if os.path.isdir(dirname0):
        filesdonealready=[]
        dirname=jsf.proper_dir_path(dirname0)
        newindices=read_new_indices(dirname)
        #print "YIYIYI",newindices

        #print "Running form on directory",dirname
        currentdir=os.getcwd()

        if os.path.isdir(dirname+"FORM/proc_0loop/"):
            os.chdir(dirname+"FORM/proc_0loop/")
            filelist=glob.glob("*frm")
            for fil in filelist:
                if os.path.isfile(fil[:-4]+".log"):
                    #print "file",fil[:-4]+".log","present, next please!"
                    filesdonealready.append(fil[:-4]+".log")
                else:
                    #print "form -l "+fil
                    subprocess.call("form -l "+fil,shell= True)
                    #We didn't gain anything on one test we did by using tform
                    # we would gain quite a bit by sending different processes to a cluster
                    #subprocess.call("tform -w4 -l "+fil,shell= True)
                better_log(fil[:-4]+".log",newindices)
            os.chdir(currentdir)
        if os.path.isdir(dirname+"FORM/proc_1loop/"):
            os.chdir(dirname+"FORM/proc_1loop/")
            filelist=glob.glob("*frm")
            for fil in filelist:
                if os.path.isfile(fil[:-4]+".log"):
                    #print "file",fil[:-4]+".log","present, next please!"
                    filesdonealready.append(fil[:-4]+".log")
                else:
                    #print "form -l "+fil
                    subprocess.call("form -l "+fil,shell= True)
                better_log(fil[:-4]+".log",newindices)
            os.chdir(currentdir)

        #if len(filesdonealready)>0:
            #print "The following files were done already"
            #print "If you want to do them, remove them and run again"
            #for x in filesdonealready:
                #print x
    else:
        print "not a valid directory"

if __name__=='__main__':

    run_form(sys.argv[1])

