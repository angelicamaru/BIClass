import numpy as np
import pandas as pd
import itertools
def read_database(file):
 db=[]
 with open(file)as f:
  N=f.readlines()
  for b in N:
   li=b.split(" ")
   l=[]
   for v in li:
    if v!="\n":
     l.append(int(v))
   db.append(l)
 return db
def diff(li1,li2):
 return[x for x in li1 if not x in li2]
def powerset(li):
 ps=itertools.chain.from_iterable(itertools.combinations(li,r)for r in range(0,len(li)+1))
 pl=[]
 for e in reversed(list(ps)):
  pl.append(list(e))
 return pl
def eclat(db,minsup):
 h={}
 for E,t in enumerate(db):
  for i in t:
   if not i in h:
    h[i]=[]
   h[i].append(E)
 F=[]
 P=[([i],set(h[i]))for i in sorted(h.keys())if len(h[i])>=minsup]
 def eclatRec(P,minsup,F):
  for V,(Xa,tXa)in enumerate(P):
   F.append((Xa,len(tXa)))
   Pa=[]
   for Xb,tXb in P[V+1:]:
    I=tXa&tXb
    if len(I)>=minsup:
     Pa.append((sorted(list(set(Xa+Xb))),I))
   if Pa:
    eclatRec(Pa,minsup,F)
 eclatRec(P,minsup,F)
 return F
def createAssociationRules(F,minconf):
 B=[]
 for Z,supZ in[fEntry for fEntry in F if len(fEntry[0])>1]:
  A=sorted(powerset(Z),key=lambda l:len(l),reverse=True)
  A.remove([])
  A.remove(Z)
  while A:
   X=A.pop(0)
   O=[xEntry for xEntry in F if xEntry[0]==X][0][1]
   c=supZ/O
   if c>=minconf:
    B.append((X,diff(Z,X),supZ,c))
   else:
    m=powerset(X)
    for z in m:
     if z in A:
      A.remove(z)
 return B
def getStrongRules(db,minsup,minconf):
 return createAssociationRules(eclat(db,minsup),minconf)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
