#coding=utf-8
import numpy as np
import random
import numpy.linalg as linalg

__version__ = "1.0.1"
class computation:
    def __init__(self):
        ######sym2
        self._sym2_h=[-0.1294,0.2241,0.8365,0.4830]
        self._sym2_g=[-0.4830,0.8365,-0.2241,-0.1294]
        ######sym3
        self._sym3_h=[0.0352,-0.0854,-0.1350,0.4599,0.8069,0.3327]
        self._sym3_g=[-0.3327,0.8069,-0.4599,-0.1350,0.0854,0.0352]
        ######sym4
        self._sym4_h=[-0.0758,-0.0296,0.4976,0.8037,0.2979,-0.0992,-0.0126,0.0322]
        self._sym4_g=[-0.0322,-0.0126,0.0992,0.2979,-0.8037,0.4976,0.0296,-0.0758]
        ######sym5
        self._sym5_h=[0.0273,0.0295,-0.0391,0.1994,0.7234,0.6340,0.0166,-0.1753,-0.0211,0.0195]
        self._sym5_g=[-0.0195,-0.0211,0.1753,0.0166,-0.6340,0.7234,-0.1994,-0.0391,-0.0295,0.0273]
        ######sym6
        self._sym6_h=[0.0154041093270274,	0.00349071208421747,	-0.117990111148191,	-0.0483117425856330,\
                      0.491055941926747,	0.787641141030194,	0.337929421727622,	-0.0726375227864625,\
                      -0.0210602925123006,	0.0447249017706658,	0.00176771186424280,	-0.00780070832503415]
        self._sym6_g=[0.00780070832503415,	0.00176771186424280,	-0.0447249017706658,	-0.0210602925123006,\
                      0.0726375227864625,	0.337929421727622,	-0.787641141030194,	0.491055941926747,\
                      0.0483117425856330,	-0.117990111148191,	-0.00349071208421747,	0.0154041093270274]
        ######sym7
        self._sym7_h=[0.00268181456825788,	-0.00104738488868292,	-0.0126363034032519,	0.0305155131659636,\
                      0.0678926935013727,	-0.0495528349371273,	0.0174412550868558,	0.536101917091763,\
                      0.767764317003164,	0.288629631751515,	-0.140047240442962,	-0.107808237703818,\
                      0.00401024487153366,	0.0102681767085113]
        self._sym7_g=[-0.0102681767085113,	0.00401024487153366,	0.107808237703818,	-0.140047240442962,\
                      -0.288629631751515,	0.767764317003164,	-0.536101917091763,	0.0174412550868558,\
                      0.0495528349371273,	0.0678926935013727,	-0.0305155131659636,	-0.0126363034032519,\
                      0.00104738488868292,	0.00268181456825788]
        ######sym8
        self._sym8_h=[-0.00338241595100613,-0.000542132331791148,0.0316950878114930,\
           0.00760748732491761,-0.143294238350810,-0.0612733590676585,\
           0.481359651258372,0.777185751700524,0.364441894835331,\
           -0.0519458381077090,-0.0272190299170560,0.0491371796736075,\
           0.00380875201389062,-0.0149522583370482,-0.000302920514721367,0.00188995033275946]
        self._sym8_g=[-0.00188995033275946,-0.000302920514721367,0.0149522583370482,\
           0.00380875201389062,-0.0491371796736075,-0.0272190299170560,\
           0.0519458381077090,0.364441894835331,-0.777185751700524,\
           0.481359651258372,0.0612733590676585,-0.143294238350810,\
           -0.00760748732491761,0.0316950878114930,0.000542132331791148,-0.00338241595100613]
        ######dw2
        self._db2_h=[-0.1294,0.2241,0.8365,0.4830]
        self._db2_g=[-0.4830,0.8365,-0.2241,-0.1294]
        ######dw3
        self._db3_h=[0.0352,-0.0854,-0.1350,0.4599,0.8069,0.3327]
        self._db3_g=[-0.3327,0.8069,-0.4599,-0.1350,0.0854,0.0352]
        ######dw4
        self._db4_h=[-0.0106,0.0329,0.0308,-0.1870,-0.0280,0.6309,0.7148,0.2304]
        self._db4_g=[-0.2304,0.7148,-0.6309,-0.0280,0.1870,0.0308,-0.0329,-0.0106]
        ######dw5
        self._db5_h=[0.0033,-0.0126,-0.0062,0.0776,-0.0322,-0.2423,0.1384,0.7243,0.6038,0.1601]
        self._db5_g=[-0.1601,0.6038,-0.7243,0.1384,0.2423,-0.0322,-0.0776,-0.0062,0.0126,0.0033]
        ######dw6
        self._db6_h=[-0.00107730108499558,0.00477725751101065,0.000553842200993802,-0.0315820393180312,\
                     0.0275228655300163,0.0975016055870794,-0.129766867567096,-0.226264693965169,\
                     0.315250351709243,0.751133908021578,0.494623890398385,0.111540743350080]
        self._db6_g=[-0.111540743350080,0.494623890398385,-0.751133908021578,0.315250351709243,\
                     0.226264693965169,-0.129766867567096,-0.0975016055870794,0.0275228655300163,\
                     0.0315820393180312,0.000553842200993802,-0.00477725751101065,-0.00107730108499558]
    def dftmtx(self,N):
        return np.matrix(np.fft.fft(np.eye(N)))
    def div(self,N):
        res=[]
        for i in range (2,N):
            if N%i==0:
                res.append(i)
        return res
    def htm(self,dft_len,total_len):
        eye_len=int(total_len/dft_len)
        dft=self.dftmtx(dft_len)
        (row,col)=dft.shape
        cols=[]
        for i in range(0,row):
            tmp_row=dft[i]
            tmp_eye=np.eye(eye_len)
            rows=[]
            for j in range(0,tmp_row.shape[1]):
                rows.append(tmp_eye.dot(tmp_row[0,j]))
            cols.append(np.concatenate(rows,axis=1))
        return np.matrix(np.concatenate(cols,axis=0)).dot(1/np.sqrt(dft_len))
    def ihtm(self,dft_len,total_len):
        eye_len=int(total_len/dft_len)
        dft=dftmtx(dft_len)
        dft=dft.H
        (row,col)=dft.shape
        cols=[]
        for i in range(0,row):
            tmp_row=dft[i]
            tmp_eye=np.eye(eye_len)
            rows=[]
            for j in range(0,tmp_row.shape[1]):
                rows.append(tmp_eye.dot(tmp_row[0,j]))
            cols.append(np.concatenate(rows,axis=1))
        return np.matrix(np.concatenate(cols,axis=0)).dot(1/np.sqrt(dft_len))
    def omp(self,args):
        T=args[1].copy()
        s=args[0]
        N=args[2]
        size=T.shape
        M=size[0]
        hat_y=np.zeros((1,N),dtype=np.complex)
        Aug_t=[]
        r_n=s
        pos_array=[]
        for times in range(0,int(M)):
            pos=np.argmax(np.absolute(T.H.dot(r_n)))       
            if np.array(Aug_t).size==0:
                Aug_t=np.array(T[:,pos])
            else:
                Aug_t=np.concatenate([np.array(Aug_t),np.array(T[:,pos])],axis=1)
            Aug_t=np.matrix(Aug_t)
            T[:,pos]=np.zeros((M,1))       
            aug_y=(np.linalg.pinv( np.matrix(Aug_t.H.dot(Aug_t)))).dot(Aug_t.H).dot(s);
            r_n=s-Aug_t.dot(aug_y);
            pos_array.append(pos)
            if np.power(np.absolute(aug_y[-1,0]),2)/linalg.norm(aug_y)<0.05:
                break       
        hat_y[0,pos_array]=aug_y.T   
        return hat_y  
    def dwt(self,N,wname):
        switch={'db2':{'h':self._db2_h,'g':self._db2_g},\
                'db3':{'h':self._db3_h,'g':self._db3_g},\
                'db4':{'h':self._db4_h,'g':self._db4_g},\
                'db5':{'h':self._db5_h,'g':self._db5_g},\
                'db6':{'h':self._db6_h,'g':self._db6_g},\
                'sym2':{'h':self._sym2_h,'g':self._sym2_g},\
                'sym3':{'h':self._sym3_h,'g':self._sym3_g},\
                'sym4':{'h':self._sym4_h,'g':self._sym4_g},\
                'sym5':{'h':self._sym5_h,'g':self._sym5_g},\
                'sym6':{'h':self._sym6_h,'g':self._sym6_g},\
                'sym7':{'h':self._sym7_h,'g':self._sym7_g},\
                'sym8':{'h':self._sym8_h,'g':self._sym8_g},\
                }
        if not switch.get(wname):
            print('wave name not found')
            return        
        h=switch[wname]['h']
        g=switch[wname]['g']
        L=len(h)
        rank_max=int(np.log2(N))
        rank_min=int(np.log2(L))+1
        ww=1
        for jj in range(rank_min,rank_max+1):
            nn=np.power(2,jj)
            p1_0=np.concatenate([np.array(h),np.zeros((1,nn-L))] ,axis=None)
            p2_0=np.concatenate([np.array(g),np.zeros((1,nn-L))] ,axis=None)
            p1=[]
            p2=[]
            for ii in range(0,int(nn/2)):
                p1.append(np.roll(p1_0,int(2*(ii))))
                p2.append(np.roll(p2_0,int(2*(ii))))
            w1=np.concatenate([p1,p2],axis=0)
            mm=np.power(2,rank_max)-np.max(w1.shape)
            w=np.matrix( np.concatenate([np.concatenate([w1,np.zeros((np.max(w1.shape),mm))],axis=1),np.concatenate([np.zeros((mm,np.max(w1.shape))),np.eye(mm,mm)],axis=1)],axis=0))
            ww=ww*w
        return ww
                
    def randsubmtx(self,A,m):
        (row,col)=A.shape
        numlist=list(range(row))
        randnum=[]
        for x in range(m):
            pos=random.randint(0,len(numlist)-1)
            randnum.append(numlist[ pos])
            numlist.remove(numlist[ pos])
        return A[randnum]
        
    
    

    
