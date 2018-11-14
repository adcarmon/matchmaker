import file as jsf
import subprocess
import glob
import os
import sys
import matchmaker.functions as func



# This takes a QGRAF model file and extract the list of bosonic particles
def get_bosons(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    bolist=[]
    for x in lines:
        if ("+]" in x):
            bolist.append(x.split(',')[0].strip().replace("[",""))
            if (x.split(',')[0].strip().replace("[","")!=x.split(',')[1].strip().replace("[","")):
                bolist.append(x.split(',')[1].strip().replace("[",""))
    return bolist


# This will be used to replace the correct spatial indices
def JSP_replace(st,ilist,plist,dummyindex,indexlist):
    repl=[('[','('),(']',')')]
    #print "teo=",indexlist.replace(" ","").replace("\n","").split(",")
    for x in indexlist.replace(" ","").replace("\n","").split(","):
        #print "tio=",[(x+x+str(i+1),x+str(t)) for (i,t) in enumerate(ilist)]
        repl.extend([(x+x+str(i+1),x+str(t)) for (i,t) in enumerate(ilist)])
        repl.extend([(x+x+"minus",x+"minus"+str(dummyindex)+"0")])
    repl.extend([('pp'+str(i+1),t) for (i,t) in enumerate(plist)])
    return  reduce(lambda a, kv: a.replace(*kv), repl, st)


def allpos(i):
    res=int(i)
    if res<0:
        res += 100
    return str(res)

def feynman_rules(dirname):
    # This is a dictionary of dictionaries encoding all the Feynman rules
    alldicts={}
    templist=glob.glob(dirname+"QGRAF/model_data/*list")
    allkeys=[x.split('/')[-1][:-4] for x in templist]
    #print "allkesy=",allkeys
    for key in allkeys:
        filename=dirname+"QGRAF/model_data/"+key+"list"
        tempdict={}
        for line in open(filename):
            #print "TIO",line.split()
            tempdict[" ".join(line.split()[:-1])]=line.split()[-1]
        alldicts[key]=tempdict
        #print key
        #if key == "v4":
            #print "OEOEOE",key,tempdict.keys()
    return alldicts


def read_new_params(dirname):
    # define new parameters
    with open(dirname+'QGRAF/model_data/listparam','r') as f:
        all_lines = f.readlines()
    return ', '.join([x.replace('\n','') for x in all_lines])

def read_new_functions(dirname):
    # define new parameters
    with open(dirname+'QGRAF/model_data/newfunctions','r') as f:
        all_lines = f.readlines()
    return ', '.join([x.replace('\n','') for x in all_lines])

def read_new_symbols(dirname):
    # define new parameters
    with open(dirname+'QGRAF/model_data/newsymbols','r') as f:
        all_lines = f.readlines()
    return ', '.join([x.replace('\n','') for x in all_lines])

def read_new_indices(dirname):
    # define new parameters
    with open(dirname+'QGRAF/model_data/newindices','r') as f:
        all_lines = f.readlines()
    #print "all_lines=",', '.join([x.replace("\n","").split("=")[0] for x in all_lines])
    return ', '.join([x.replace("\n","").split("=")[0] for x in all_lines])
    #return ', '.join([x.replace('\n','') for x in all_lines])

def read_new_indices_with_dims(dirname):
    # define new parameters
    with open(dirname+'QGRAF/model_data/newindices','r') as f:
        all_lines = f.readlines()
    #return ', '.join([x.split("=")[0] for x in all_lines])
    return ', '.join([x.replace('\n','') for x in all_lines])

def read_partial_fractions(dirname):
    # define new partial fractions
    with open(dirname+'QGRAF/model_data/listmass') as f:
        lines = f.read().splitlines()
    partialfrac=''
    if len(lines)>0:
        masslist=(lines[0].split())
        for x in [(masslist[i],masslist[j]) for i in range(len(masslist)) for j in range(i+1, len(masslist))]:
            partialfrac += "repeat;\n" 
            partialfrac += "id,once prop(k1, "+x[0]+")*prop(k1, "+x[1]+")= 1/("+x[0]+"^2-"+x[1]+"^2)*(prop(k1, "+x[0]+")- prop(k1, "+x[1]+"));\n" 
            partialfrac += "endrepeat;\n\n" 
    return partialfrac


def write_aux_files(dirname,filename,alldicts):
    process=filename.split('/')[-1][:-4]
    particles=process.split('_')
    bosons=get_bosons(dirname+'QGRAF/model')
    #print bosons
    bparticles=[x for x in particles if x in bosons]
    dim=(3*len(particles)-len(bparticles))/2
    thenmax=6-dim
    #print "parts=",particles
    #print "numparts=",len(particles)," dim=",dim,"  thenmax=",thenmax
    looporder=filename.split('/')[-2]
    formdir=dirname+'FORM/'+looporder+'/'
    #print "Doing file",filename,"that corresponds to process",process,"at",looporder
    #print
    if not os.path.isdir(formdir):
        subprocess.call("mkdir "+formdir,shell=True)

    newindices=read_new_indices(dirname)
    diagnum=1
    lastline=0
    outputline=''

    outputfilename=formdir+process+'.aux' # one diagram at a time

    if not os.path.isfile(outputfilename):
        #print "diagram file",outputfilename,"os present"
        #print "delete it if you want to regenerate the diagrams"
        #diagnum=int(subprocess.check_output(" tail -n 2 "+outputfilename,shell=True).split()[1].replace("diags",""))+1
        #print "number of diagrams generated=", diagnum-1
    #else:
        of = open(outputfilename,"w")
        dummyi=0
        for line in open(filename):
            dummyi+=1
            datalinetemp=line.rstrip().replace('(',',').replace(')','').replace('*','').split(',')
            if datalinetemp[-1]=='' and len(datalinetemp)>1: 
                # last line of the current diagram
                lastline=1
                dataline=datalinetemp[:-1]
            else:
                dataline=datalinetemp

            # Now we start with the proper replacements
            if dataline[0]=='' and len(dataline)>1:
                # numerical factor
                outputline += "("+dataline[1].replace("+","")+")"        
            elif len(dataline)>1: 
                [op,fields,indices0,ppi]=dataline[0].strip(),dataline[1::3],dataline[2::3],dataline[3::3]
                indices = [allpos(ii) for ii in indices0]
                #print "op=",op," fields=",fields," indices=",indices," ppi=",ppi," dummyi=",dummyi," newindices=",newindices
                #print alldicts[op]
                #print "eoo=",JSP_replace(alldicts[op][" ".join(fields)],indices,ppi,dummyi,newindices)
                outputline += "*("+JSP_replace(alldicts[op][" ".join(fields)],indices,ppi,dummyi,newindices)+")"
                #print outputline
                # if 'cpol' in op and "B" in fields:
                #     print "YAYAYA*("+JSP_replace(alldicts[op][" ".join(fields)],indices,ppi,dummyi,newindices)+")"
                #     print indices,ppi,dummyi,newindices

            if lastline==1:
                #print "id diags"+str(diagnum)+" = "+outputline+";\n"
                of.write("id diags"+str(diagnum)+" = "+outputline+";\n\n")
                diagnum += 1
                outputline=''
                lastline = 0
                dummyi=0

        of.close()
    return diagnum,process,thenmax,formdir


def generate_form(dirname0):
    #corepre=func.get_path('core')+"/"
    corepre="../core/"
    if os.path.isdir(dirname0):
        dirname=jsf.proper_dir_path(dirname0)
        #print "doing directory",dirname


        alldicts=feynman_rules(dirname)
        #newparams=read_new_params(dirname)
        newfunctions=read_new_functions(dirname)
        #print "newfunctions",newfunctions
        newsymbols=read_new_symbols(dirname)
        newindices=read_new_indices_with_dims(dirname)
        partialfrac=read_partial_fractions(dirname)
        # Go through all the QGRAF files
        filelist=glob.glob(dirname+"QGRAF/proc*/*qgf")
        #print filelist

        for filename in filelist:
            diagnum,process,thenmax,formdir=write_aux_files(dirname,filename,alldicts)
            # check if form file is there, if it is do not do anything
            if not os.path.isfile(formdir+process+'.frm'):
                ## Let's now write the form skeleton program

                myrepl= ('NUMBER_OF_DIAGRAMS',str(diagnum-1)),('NEW_SYMBOLS',newsymbols),('NEW_FUNCTIONS',newfunctions),('NEW_INDICES',newindices),("FILE_WITH_DIAGRAMS",process+".aux"),("PROCESS",process.replace("_","").replace("[","").replace("]","")),("PARTIALFRACTIONS",partialfrac),("THENMAX",str(thenmax))
                jsf.dress_skeleton(myrepl, corepre+'skeleton.frm',formdir+process+'.frm')
    else:
        print "not a valid directory"

if __name__=='__main__':

    generate_form(sys.argv[1])


