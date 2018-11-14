def proper_dir_path(dirname0):
    if "/" not in dirname0[-1]:
        dirname = dirname0+"/"
    else:
        dirname = dirname0
    return dirname

def dress_skeleton(repl,skel,dressed):

    """
    dress_skeleton(repl,skel,dressed) dresses file skel into file dressed
    with the replacements in repl
    
    skel and dressed are strings (the names of the skeleton and output files)
    repl is a sequence of tuples of two strings, the first being the string 
    to be replaced and the second the one to replace it with
    
    sample ussage:
    
    myrepl= ('change_A','with_A'),('change_B','with_B')
    dress_skeleton(myrepl,'file1.dat','file2.dat')
    
    this will make a copy of file1.dat into file2.dat with every occurence
    of 'change_A' being replaced with 'with_A' and every occurence of
    'change_B' being replaced with 'with_B'
    """
    dressed_file = open(dressed, 'w')
    skel_file = open(skel, 'r')
    for line in skel_file:        
        dressed_file.write(reduce(lambda a, kv:a.replace(*kv),repl,line))
    skel_file.close()
    dressed_file.close()




if __name__ == '__main__':

    # this would be run if we call the script directly

    eps=10**-10
    # let's test diagonaliza
    print "testing the function diagonaliza"
    check=[]
    bads=[]
    for n in range(10000):
    	Md=np.diag(np.random.rand(3))
        mati=200*np.random.rand(3,3)-100+1j*(200*np.random.rand(3,3)-100)
    	umatiL=np.matrix(gram_schmidt(mati))
    	mati=200*np.random.rand(3,3)-100+1j*(200*np.random.rand(3,3)-100)
    	umatiR=np.matrix(gram_schmidt(mati))
        Mmat=umatiL.T*Md*umatiR.H
    	sol=diagonaliza(Mmat,eps)
        res=is_zero(np.sort(np.diag(Md))-np.sort(np.diag(sol[1])),eps)
        if not res:
            	bads.append(Mmat)                
    	check.append(res)
    print "We tested ",len(check)," points"
    if all(check):
    	print "It works ALWAYS!"
    else:
    	print "It didn't work"
        print bads

    print "testing the function diagonalizaS"
    # let's test diagonalizaS
    check=[]
    bads=[]
    for n in range(10000):
    	diagonal=200*np.random.rand(3)-100+1j*(200*np.random.rand(3)-100)
    	Md=np.diag([x/np.abs(x) for x in diagonal])
    	mati=200*np.random.rand(3,3)-100
    	Omati=np.matrix(gram_schmidt(mati))
    	Mmat=Omati.T*Md*Omati
    	if is_unitary(Mmat) and is_symmetric(Mmat):
            sol=diagonalizaS(Mmat,eps)
            res=is_zero(np.sort(np.diag(Md))-np.sort(np.diag(sol[1])),eps)
            if not res:
            	bads.append(Mmat)                
            check.append(res)
    print "We tested ",len(check)," points"
    if all(check):
    	print "It works ALWAYS!"
    else:
    	print "It didn't work"
        print bads


    print "testing the function diagonalizaH"
    # let's test diagonalizaH
    check=[]
    bads=[]
    for n in range(10000):
    	Md=np.diag(np.random.rand(3))
    	mati=200*np.random.rand(3,3)-100+1j*(200*np.random.rand(3,3)-100)
    	Umati=np.matrix(gram_schmidt(mati))
    	Mmat=Umati*Md*Umati.T
    	if is_symmetric(Mmat,eps):
            sol=diagonalizaH(Mmat,eps)
            res=is_zero(np.sort(np.diag(Md))-np.sort(np.diag(sol[1])),eps)
            if not res:
            	bads.append(Mmat)
            check.append(res)
    print "We tested ",len(check)," points"
    if all(check):
    	print "It works ALWAYS!"
    else:
    	print "It didn't work"
        print bads
