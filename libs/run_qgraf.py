import file as jsf
import os
import subprocess
import sys
import glob
import matchmaker.functions as func


def write_two_point_function(partlist,dirname):
    # QGRAF does not do tree-level two point functions so we do them ourselves
    # partlist is a list of length 2 with the names of the two particles involved

    #get the sign
    # we go through the propagators and get the sign
    with open(dirname+'QGRAF/model','r') as the_file:
        lines = the_file.read().strip().splitlines()
    thelines=[li.strip().replace('[','').replace(']','').split(',') for li in lines if '+' in li or '-' in li]
    signo=''
    # for i,pa in enumerate(thelines):
    #     print partlist,list(reversed(partlist)),pa[:2],list(reversed(partlist)) in [pa[:2]]
    #     # Note that we might use the same order as in the propagators or the opposite one
    #     if partlist in [pa[:2]] or list(reversed(partlist)) in [pa[:2]]:
    #         signo='('+pa[2]+'1)*'
    #print thelines#ke, va,zip(ke,va)

    #get the sign
    # we go through the propagators and get the sign
    with open(dirname+'QGRAF/model_data/listlightfermions','r') as the_file:
        fermionlines = the_file.read().strip().replace(' ','').split(',')
    with open(dirname+'QGRAF/model_data/listlight','r') as the_file:
        lines = the_file.read().strip().replace(' ','').split(',')
    if partlist[0] in fermionlines or partlist[1] in fermionlines:
        signo='(-1)*'
    elif partlist[0] in lines or partlist[1] in lines:
        signo='(+1)*'
    #print signo
    
    if len(signo)>1:
        # we only proceed if the sign has been computed properly
        # we now check the order of the 2-point vertex
        print dirname+'QGRAF/model_name/v2list'
        # read two-point vertices
        with open(dirname+'QGRAF/model_data/v2list','r') as the_file:
            lines = the_file.read().strip().splitlines()
        v2parts=[(li.split())[:2] for li in lines]

        if partlist in v2parts:
            #correct order
            return "diags:=[\n\n"+signo+"\n cpol("+partlist[0]+"(-1,p1))*\n cpol("+partlist[1]+"(-3,p2))*\n\n v2("+partlist[0]+"(-1,p1),"+partlist[1]+"(-3,p2)),\nNULL]:"
        elif list(reversed(partlist)) in v2parts:
            #opposite order
            if '-' in signo:
                # sign is -*-=+ if in reverse order 
                signo='(+1)*'
            return "diags:=[\n\n"+signo+"\n cpol("+partlist[0]+"(-1,p1))*\n cpol("+partlist[1]+"(-3,p2))*\n\n v2("+partlist[1]+"(-3,p2),"+partlist[0]+"(-1,p1)),\nNULL]:"
        else:
            return "diags:=[\nNull]:"
    else:
        return signo

def run_qgraf(listofparticles,dirname0):

    if os.path.isdir(dirname0):
        if os.path.isfile(listofparticles):
            dirname=jsf.proper_dir_path(dirname0)
            #print "doing directory",dirname
            with open(listofparticles) as f:
                lines = f.read().strip().splitlines()
            for li in lines:
                outfile=" ".join(li.split()).replace(" ","_").replace("[","").replace("]","")
                partlist=','.join(li.split())
                filelist=glob.glob(dirname+"QGRAF/qgraf.skeleton*.dat")
                for fil in filelist:
                    outputdirname=dirname+"QGRAF/proc_"+fil.split('/')[-1].split('.')[-2]+"/"
                    if not os.path.isdir(outputdirname):
                        subprocess.call("mkdir "+outputdirname,shell=True)
                    outputfilename=dirname+"QGRAF/proc_"+fil.split('/')[-1].split('.')[-2]+"/"+outfile+".qgf"
                    #print '0' in fil.split('.')[-2]
                    #print len(li.split()),partlist,li.split()
                    #if os.path.isfile(outputfilename):
                        #print "file "+outputfilename+" already present, doing next"
                    if not os.path.isfile(outputfilename) and "0" in fil.split('.')[-2] and len(li.split()) == 2:
                        # qgraf does not do tree level two point functions, we do it ourselves
                        #print "eoo",partlist,outputfilename
                        twop=write_two_point_function(li.split(),dirname)
                        #print "oee",twop#write_two_point_function(li.split(),outputfilename)
                        if len(twop)>1:
                            #print "writing file "+outputfilename
                            with open(outputfilename,'w') as the_file:
                                the_file.write(twop)
                    elif not os.path.isfile(outputfilename):
                        themodel=dirname+"QGRAF/model"
                        subprocess.call("cp "+themodel+" ./model",shell=True)
                        myrepl=("LISTOFPARTICLES",partlist),("THEMODEL",'model')
                        jsf.dress_skeleton(myrepl,fil,'qgraf.dat')
                        func.rep_mysty('qgraf.dat')
                        if os.path.isfile('OUTPUTFILE'):
                            subprocess.call("rm OUTPUTFILE",shell=True)
                            # por ahora voy a asumir que qgraf esta en el path 
                        subprocess.call("qgraf", shell=True)
                        subprocess.call("mv OUTPUTFILE "+outputfilename,shell=True)
                        subprocess.call("rm model", shell=True)
                        subprocess.call("rm qgraf.dat", shell=True)
        else:
            print "not a valid list of particles"
    else:
        print "not a valid directory"


if __name__=='__main__':
    run_qgraf(sys.argv[1],sys.argv[2])
