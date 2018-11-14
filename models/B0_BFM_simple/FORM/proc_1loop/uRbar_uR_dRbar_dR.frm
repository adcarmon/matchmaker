* -*-Form-*-

#: Parentheses 2000
#-
format Mathematica;
*** This we will have to do automated we are just now testing
*CF Ta;
CF Log, den;
Symbol epsi,FourPi;
Symbol D, Dy, Dmu, Nc, V, I,Dm4;
S SIX, SEVEN, FIVE, g1, gw, gs, lam, muH, MBH0;
CF gBH0qL, yd, yl, yu, ydbar, ylbar, yubar, Ta, FSU2L, T, FSU3C, fsu2, fsu3;
CF Evect;
*** Trick to do gam(y,k+p,y)=gam(y,k,y)+gam(y,p,y)
Index itrick;
Auto I m=3, f=3, a=8, l=2, n=3, y=Dy, mu=D;
*Auto I i=Nc,j,f,l;
Auto S s;
*Auto I y=NF, w=NF; 
*Auto I mu=D:Dm4, nu=D:Dm4, al=D:Dm4, be=D:Dm4, ro=D:Dm4, si=D:Dm4;
*Auto I a=V;
*Auto I ff=3;
Auto V k, p, q;
#do i=1,0;
 S diags'i';
#enddo;
F ALARM;
CF FF; 
CF Fc; 
CF Mom; 
CF TTC; 
CF Tc; 
CF deltaF; 
CF dotp; 
CF g5; 
CF gam; 
CF gi; 
CF prop; 
CF invprop; 
CF ubspin; 
CF uspin; 
CF vbspin; 
CF vspin; 
CF eps;
Dimension D;
Off  Statistics;
.global;

#if 0

#do i=1,0;
G expr'i'= diags'i';
#include uRbar_uR_dRbar_dR.aux;
* max power of external momenta that we'll keep
#define Nmax "0"

** write p1.p2=dot(p1,p2)
id p1?.p2?=dotp(p1,p2);


** Write deltas in a way that FORM understands (so that it can sum over indices)
** The range of the index is understoof from its name (a=1, 8; i=1,3; y=1, D; ...)
id deltaF(?a)=d_(?a); 
id gi(?a)=d_(?a); 
***#include colour.faux 

*** Extract momentum explicitly from gamma string
*** Extract the loop momentum explicitly for later tensor reduction
#do jf=1,200
id,once gam(?a, p1?, ?b) = Mom(p1, mugam'jf')*gam(?a, mugam'jf', ?b);
#enddo;
*** Now all gamma matrices should have only indices

*** Implement linearity of gam, Mom and dotp
*** This works because gam with momenta does not contain gamma5 and has only three arguments
*id gam(y1?,itrick?, y2?)=gam(y1 ,itrick, y2 ); 
id Mom(itrick?, mu1?)=Mom(itrick, mu1 ); 
id dotp(itrick?, k1?)=dotp(itrick, k1 ); 
id dotp(k1?, itrick?)=dotp(k1, itrick ); 
.sort

** We are now going to expand in powers of external momenta
*** Let's count powers of external momenta (p1 to p6) in the numerator
*** they can only appear in Mom or dotp in the numerator
#do jc=1,6; 
id Mom(p'jc',mu1?)=sSS*Mom(p'jc',mu1);
id dotp(p'jc',k1?)=sSS*dotp(p'jc',k1);
id dotp(k1?,p'jc')=sSS*dotp(k1,p'jc');
#enddo;
*** eliminate terms that already have more than Nmax power in the numerator
id sSS^('Nmax'+1)=0;
.sort
** Now we do the denominators
** Trick to separate the loop momentum from the external momenta
id prop(p1?,s?)=prop(p1,p1,s);
argument prop,2;
id k1=0;
endargument;
argument prop,1;
#do jc=1,6; 
id p'jc'=0; 
#enddo
endargument;
* Make sure k1 always appears with a plus sign in propagators
id prop(-k1, q?, s?) = prop(k1, -q, s);
id prop(-k1, 0, s?) = prop(k1, 0, s);
* Eliminate the factors of external momenta in the denominators
* We do it recursively for efficiency
repeat;
id,once prop(k1,q?,s?) = prop(k1,0,s)*(1-(sSS^2*dotp(q,q)+2*sSS*dotp(k1,q))*prop(k1,q,s));
id,once prop(0,q?,s?) = prop(0,0,s)*(1-(sSS^2*dotp(q,q))*prop(0,q,s));
id,once sSS^('Nmax'+1)=0;
endrepeat;
* Once the external momenta are eliminated from the propagators we go
* back to standard notation
id prop(k1?,0,s?)=prop(k1,s);
id prop(0,0,s?)=prop(0,s);
.sort

*** We have to implement linearity of dotp again (we have introduced
*** with sum of vectors here again)
id dotp(itrick?, k1?)=dotp(itrick, k1 ); 
id dotp(k1?, itrick?)=dotp(k1, itrick ); 
.sort


* set to zero objects that are zero (but form does not know they are)
id prop(0,0)=0;
*** On-shell heavy propagator (at zero momentum)
id prop(0,s1?)=-1/s1^2;
.sort

*** momenta only appear as Mom(p,mu) or as dotp(p1,p2)
*** we write dotp explicitly in terms of Mom
#do jf=1,200
id,once dotp(p1?,p2?)=Mom(p1,mudotp'jf')*Mom(p2,mudotp'jf');
#enddo;


*** Keep only even powers of k1
id Mom(k1,mu1?) = sss*Mom(k1,mu1);
repeat; 
id sss^2=1;
endrepeat; 
id sss=0; 

.sort

id Mom(k1,mu1?)^2=k1.k1;
.sort

* ** Tensor reduction
* id Mom(k1, mu1?)*Mom(k1, mu2?)*
*    Mom(k1, mu3?)*Mom(k1, mu4?)*
*    Mom(k1, mu5?)*Mom(k1, mu6?)* 
*    Mom(k1, mu7?)*Mom(k1, mu8?)= 
*    dd_(mu1, mu2, mu3, mu4, mu5, mu6, mu7, mu8)*
*    k1.k1*k1.k1*k1.k1*k1.k1*105/(5040*D+4620*D^2+1260*D^3+105*D^4);
* id Mom(k1, mu1?)*Mom(k1, mu2?)*
*    Mom(k1, mu3?)*Mom(k1, mu4?)*
*    Mom(k1, mu5?)*Mom(k1, mu6?)= 
*    dd_(mu1, mu2, mu3, mu4, mu5, mu6)*
*    k1.k1*k1.k1*k1.k1*15/(120*D+90*D^2+15*D^3);
* id Mom(k1, mu1?)*Mom(k1, mu2?)*
*    Mom(k1, mu3?)*Mom(k1, mu4?)=
*    dd_(mu1, mu2, mu3, mu4)*
*    k1.k1*k1.k1*3/(6*D+3*D^2);
* id Mom(k1, mu1?)*Mom(k1, mu2?)= dd_(mu1, mu2)*k1.k1/D;

* ** Tensor reduction (valid to leading order in epsi, den(a,b)=1/(a-b*epsi))
id Mom(k1, mu1?)*Mom(k1, mu2?)*
   Mom(k1, mu3?)*Mom(k1, mu4?)*
   Mom(k1, mu5?)*Mom(k1, mu6?)* 
   Mom(k1, mu7?)*Mom(k1, mu8?)= 
   dd_(mu1, mu2, mu3, mu4, mu5, mu6, mu7, mu8)*
   k1.k1*k1.k1*k1.k1*k1.k1*105*den(201600,258720);
id Mom(k1, mu1?)*Mom(k1, mu2?)*
   Mom(k1, mu3?)*Mom(k1, mu4?)*
   Mom(k1, mu5?)*Mom(k1, mu6?)= 
   dd_(mu1, mu2, mu3, mu4, mu5, mu6)*
   k1.k1*k1.k1*k1.k1*15*den(2880,3120);
id Mom(k1, mu1?)*Mom(k1, mu2?)*
   Mom(k1, mu3?)*Mom(k1, mu4?)=
   dd_(mu1, mu2, mu3, mu4)*
   k1.k1*k1.k1*3*den(72,60);
id Mom(k1, mu1?)*Mom(k1, mu2?)= dd_(mu1, mu2)*k1.k1*den(4,2);


*****************************************************************
****        
****     Here comes the gamma matrices
****
*****************************************************************

*********************
* Join gamma lines in right order
repeat; 
id,once gam(?a, y?)*gam(y?, ?b)=gam(?a, ?b); 
endrepeat;
.sort
*********************
** Now we should only have gam(y1?, ?a , y1?) for closed fermion loops
**                    and  gam(y1?, ?a, y2?) with y1 and y2 different for open fermion loops
**     recall that for FORM gam(y1?,?a,y2?) includes the case in which y1=y2


** Anticommute gamma5 and use gamma5^2=1 to take it to the left
repeat; 
id,once gam(y? , ?a, SIX, SEVEN, ?b) =0;
id,once gam(y? , ?a, SEVEN, SIX, ?b) =0;
id,once gam(y? , ?a, SIX, SIX, ?b) = 2*gam(y , ?a, SIX, ?b);
id,once gam(y? , ?a, SEVEN, SEVEN, ?b) = 2*gam(y , ?a, SEVEN, ?b);
id,once gam(y?, ?a, mu1?, SIX, ?b) =gam(y,?a,SEVEN, mu1, ?b); 
id,once gam(y?, ?a, mu1?, SEVEN, ?b) =gam(y,?a,SIX, mu1, ?b); 
endrepeat;
.sort 

** Now that we have all gamma5 to the left, let's write it explicitely
id gam(?a, SIX, ?b)= gam(?a, ?b)+gam(?a, FIVE, ?b);
id gam(?a, SEVEN, ?b)= gam(?a, ?b)-gam(?a, FIVE, ?b);


* * Let us now eliminate repeated indices, we do it only in terms with gamma5
* * Terms without gamma5 are treated ok by form
* repeat; 
* id gam(y1?, FIVE, ?a, mua?, mua?, ?b, y1?)= D*gam(y1,FIVE, ?a, ?b, y1); 
* id,once gam(y1?, FIVE, ?a, mua?, mu1?, ?b, mua?, ?c, y1?) =  - gam(y1, FIVE, ?a, mu1, mua, ?b, mua, ?c, y1)+2*gam(y1, FIVE, ?a, ?b, mu1, ?c, y1);
* endrepeat; 

* Let us now eliminate repeated indices, we do it in all terms (open, closed, with or without gamma5)
* Terms without gamma5 are treated ok by form
repeat; 
id gam(y1?, ?a, mua?, mua?, ?b, y2?)= D*gam(y1, ?a, ?b, y2); 
id,once gam(y1?, ?a, mua?, mu1?, ?b, mua?, ?c, y2?) =  - gam(y1, ?a, mu1, mua, ?b, mua, ?c, y2)+2*gam(y1, ?a, ?b, mu1, ?c, y2);
endrepeat; 


* -----------------------------------> Work on gamma5 <----------------------------
*** This has been taken from Elisabetta
* -----------------------------> Rules For gamma5:  <------------------------------

* -------------> > anticommutes with any gamma_mu and squares to one <-------------
* already done
*repeat;
* id, once, gam(?a1, five, mu?,?a2, y?) = -gamma(?a1, mu, five, ?a2, y);
* id, once, gamma(?a1,five,five,?a2) = gamma(?a1,?a2);
*endrepeat;

* -------------------> >      Tr(g5) = Tr (g5 gmu gnu) = 0     <-------------------
* -------------------> >      Tr(g5 x odd) = 0                 <-------------------

id gam(y1?,FIVE,y1?) = 0;
id gam(y1?,FIVE,mu1?,mu2?,y1?) = 0;
id gam(y1?,FIVE, mu1?,y1?) = 0;
id gam(y1?,FIVE,mu1?,mu2?,mu3?,y1?) = 0;
id gam(y1?,FIVE,mu1?,mu2?,mu3?,mu4?,mu5?,y1?) = 0;

* -------> >   Tr((gmu gnu grho gsigma) x g5) = -4i \eps(mu,nu,rho,sigma)   <-------
id gam(y1?,FIVE,mu1?,mu2?,mu3?,mu4?,y1?) = -(4+samb'i'*(4-D))*I*e_(mu1,mu2,mu3,mu4);

* -------> >   Tr((gmu gnu grho gsigma) x g5) = -4i \eps(mu,nu,rho,sigma)   <-------
*id gam(y1?,FIVE,mu?,mu?,mu1?,mu2?,mu3?,mu4?,y1?) = -4*I*e_(mu1,mu2,mu3,mu4)*(D+2*samb'i'*(4-D));
*id gam(y1?,FIVE,mu1?,mu?,mu?,mu2?,mu3?,mu4?,y1?) = -4*I*e_(mu1,mu2,mu3,mu4)*(D+2*samb'i'*(4-D));
*id gam(y1?,FIVE,mu1?,mu2?,mu?,mu?,mu3?,mu4?,y1?) = -4*I*e_(mu1,mu2,mu3,mu4)*(D+2*samb'i'*(4-D));
*id gam(y1?,FIVE,mu1?,mu2?,mu3?,mu?,mu?,mu4?,y1?) = -4*I*e_(mu1,mu2,mu3,mu4)*(D+2*samb'i'*(4-D));
*id gam(y1?,FIVE,mu1?,mu2?,mu3?,mu4?,mu?,mu?,y1?) = -4*I*e_(mu1,mu2,mu3,mu4)*(D+2*samb'i'*(4-D));


.sort

* ------------> Error message If there is still any g5 in a closed loop<------------
id gam(y1?,?a1,FIVE,?a2,y1?)=ALARM(y1,?a1,FIVE,?a2,y1);

*B g,gamma; print;
.sort

*** End of Elisabetta's

*B gam;
*print[];
*.sort


* Now we let form do the traces without gamma5
repeat;
*id gam(y?,SIX,?a,y?)=g_(1,6_,?a);
*id gam(y?,SEVEN,?a,y?)=g_(1,7_,?a);
id gam(y?,?a,y?)=g_(1,?a);
endrepeat;



tracen,1;




************************************

id k1.k1 = invprop(k1, 0);
id prop(k1, 0)*invprop(k1, 0)=1;


repeat;
id,once prop(k1, 0)*prop(k1, MBH0)= 1/(0^2-MBH0^2)*(prop(k1, 0)- prop(k1, MBH0));
endrepeat;



* Deal with left over powers of k1.k1 in the numerator
repeat;
id invprop(k1,0)*prop(k1,s?)=1+s^2*prop(k1,s);
endrepeat;

*-----  zero of dimreg.
id prop(k1, 0)=0; 

*---- IBP identity 
#do jc=0,8 
id,once prop(k1,s?)^(10-'jc') = 
prop(k1, s)^(9-'jc')/s^2*(D/2-(9-'jc'))/(9-'jc'); 
#enddo; 


* We now let form know about momenta explicitly
* So that it will write the result in a compact universal form
id Mom(k1?,mu1?)=k1(mu1);
#do iii=1,6
id Evect(p'iii',mu1?)=pol'iii'(mu1);
#enddo
id dotp(k1?,k2?)=k1.k2;

id eps(?a) = e_(?a);

id D =4-2*epsi;
repeat;
id epsi^2=0;
id den(sa?, sb?)=1/sa+sb/sa*epsi*den(sa, sb);
endrepeat;

id prop(k1,sa?)=I*sa^2/FourPi^2*(1+1/epsi-Log(sa^2));
id epsi=0;
id 1/epsi=0;

.store 
#enddo

G  ampluRbaruRdRbardR= 
   #do ja=1,0
   +expr'ja'
   #enddo
   ;

#else
G ampluRbaruRdRbardR=0;

#endif

.sort
B prop,pol1,pol2,q,sSS;
print;


.end 




