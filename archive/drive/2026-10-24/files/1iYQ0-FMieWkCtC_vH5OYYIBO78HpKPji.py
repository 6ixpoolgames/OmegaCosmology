# Omega Cosmology v3.1: arithmetic checks for Part 11 (Examples 10-18) and Part 12 Prop. I2.
# A consistency check run while writing the primer; not a repository result.
import itertools, math
from fractions import Fraction as F
import numpy as np

def H(ps): return -sum(p*math.log2(p) for p in ps if p>0)
def MI(joint):  # joint dict {(a,b):p}
    pa={};pb={}
    for (a,b),p in joint.items(): pa[a]=pa.get(a,0)+p; pb[b]=pb.get(b,0)+p
    return sum(p*math.log2(p/(pa[a]*pb[b])) for (a,b),p in joint.items() if p>0)

# Ex 11 fair bit vs copy
p={(r,o):0.25 for r in (0,1) for o in (0,1)}
q={(0,0):0.5,(1,1):0.5,(0,1):0,(1,0):0}
tv=0.5*sum(abs(p[k]-q[k]) for k in p)
print("Ex11 TV",tv,"success",0.5+0.5*tv, "P(O=R)",p[(0,0)]+p[(1,1)],q[(0,0)]+q[(1,1)])

# Ex 12 readiness with retries
for m in range(1,17):
    A=0.9*(1-0.9**m); B=0.5*(1-0.2**m)
    print("Ex12 m",m,round(A,6),round(B,6), "A>B" if A>B else "")

# Ex 13 shared supplier
print("Ex13 one unit: marginal 0.9 each, joint 0, product",0.81)

# Ex 14 retention vs channel
# A uniform {1,2}; X1 = catalyst present (1) regardless -> I(A;X1)=0; I(A;X0)=1 (X0 = A)
jA0={(1,1):0.5,(2,2):0.5}; jA1={(1,1):0.5,(2,1):0.5}
print("Ex14 I(A;X0)",MI(jA0),"I(A;X1)",MI(jA1))
# channel V->Y: with catalyst Y=V, without Y=0
with_c={(0,0):0.5,(1,1):0.5}; without={(0,0):0.5,(1,0):0.5}
print("Ex14 I(V;Y) with",MI(with_c),"without",MI(without))
print("Ex14 P(Y=V) with",1.0,"without",0.5,"Delta",0.5)

# Ex 15 XOR
j={}
for c in (0,1):
  for m in (0,1):
    j[(c,m,c^m)]=0.25
def cmi(j):  # I(Theta;M|C) with keys (c,m,th)
    tot=0
    for c in (0,1):
        pc=sum(v for k,v in j.items() if k[0]==c)
        sub={(k[2],k[1]):v/pc for k,v in j.items() if k[0]==c}
        tot+=pc*MI(sub)
    return tot
print("Ex15 I(Th;C)",MI({(k[0],k[2]):0.25 for k in j}) , "I(Th;M)",MI({(k[1],k[2]):0.25 for k in j}), "I(Th;M|C)",cmi(j))
# perfect knowledge: C=Theta
j2={}
for th in (0,1):
  for m in (0,1):
    j2[(th,m,th)]=0.25
print("Ex15b I(Th;M|C)",cmi(j2))

# Ex 16
for a,b in itertools.product((1,0),repeat=2):
    print("Ex16 a,b",a,b,"OR",int(a or b),"always",1)

# Ex 17
print("Ex17 1D G=1",math.log(2),"G=2",math.log(3),"Gram [[1,1],[1,1]]",math.log(np.linalg.det(np.eye(2)+np.ones((2,2)))),"orth",math.log(np.linalg.det(np.eye(2)*2)),"k copies",[round(math.log(1+k),4) for k in range(1,5)])

# Ex 18 depth
print("Ex18 depth chain A->B->C =2; subdivided A->A'->B->C =3")

# three-bit checks (Ex10)
for t in (0,0.5,1):
    P={(x,y,z):(1+t*x*y*z)/8 for x in (-1,1) for y in (-1,1) for z in (-1,1)}
    X=np.array([[x,y,z] for (x,y,z) in P]); w=np.array(list(P.values()))
    mu=w@X; C=(X-mu).T@np.diag(w)@(X-mu)
    Xo=np.array([[x,y,x*y*z] for (x,y,z) in P]); muo=w@Xo; Co=(Xo-muo).T@np.diag(w)@(Xo-muo)
    print("Ex10 t",t,"mean",mu.round(6),"cov diag",np.diag(C).round(6),"out mean",muo.round(6),"out cov diag",np.diag(Co).round(6),"D2",1/(1-abs(t)/2))
# balanced functions count
cnt={}
pts=[(x,y,z) for x in (-1,1) for y in (-1,1) for z in (-1,1)]
for S in itertools.combinations(range(8),4):
    f=[1 if i in S else -1 for i in range(8)]
    c=F(sum(pts[i][0]*pts[i][1]*pts[i][2]*f[i] for i in range(8)),8)
    cnt[c]=cnt.get(c,0)+1
print("Ex10 balanced",sorted(cnt.items()))
# calibration boundary
beta,q=2,1
print("calib q(1+b)=3 at q=1,b=2:",(1+4*beta),(1+beta)*(1+q*beta))
