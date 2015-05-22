import numpy as np

class NormalShock:
    pass

class ObliqueShock:
  
    def beta(self,m1,d,g=1.4,i=0):
        p=-(m1*m1+2.)/m1/m1-g*np.sin(d)*np.sin(d)
        q=(2.*m1*m1+1.)/ np.pow(m1,4.)+((g+1.)*(g+1.)/4.+
                                          (g-1.)/m1/m1)*np.sin(d)*np.sin(d)
        r=-np.cos(d)*np.cos(d)/np.pow(m1,4.)
        
        a=(3.*q-p*p)/3.
        b=(2.*p*p*p-9.*p*q+27.*r)/27.
        
        test=b*b/4.+a*a*a/27.
        
        if (test>0.0):
            return -1.0
        elif (test==0.0):
          x1=np.sqrt(-a/3.)
          x2=x1
          x3=2.*x1
          if(b>0.0):
            x1*=-1.
            x2*=-1.
            x3*=-1.
            
        if(test<0.0):
          phi=np.acos(np.sqrt(-27.*b*b/4./a/a/a))
          x1=2.*np.sqrt(-a/3.)*np.cos(phi/3.)
          x2=2.*np.sqrt(-a/3.)*np.cos(phi/3.+np.pi*2./3.)
          x3=2.*np.sqrt(-a/3.)*np.cos(phi/3.+np.pi*4./3.)
          if(b>0.0):
            x1*=-1.
            x2*=-1.
            x3*=-1.
         
        s1=x1-p/3.
        s2=x2-p/3.
        s3=x3-p/3.
         
        if(s1<s2 and s1<s3):
          t1=s2
          t2=s3
        elif(s2<s1 and s2<s3):
          t1=s1
          t2=s3
        else:
          t1=s1
          t2=s2
        
        b1=np.asin(np.sqrt(t1))
        b2=np.asin(np.sqrt(t2))
        
        betas=b1
        betaw=b2
        if(b2>b1):
          betas=b2
          betaw=b1
         
        if(i==0):
            return betaw
        if(i==1):
            return betas
        
    def M1nM2n(self, M1, beta ,gamma=1.4):
        M1n = M1 * np.sin(beta)
        M2n = np.sqrt((1. + .5 * (gamma - 1.) * M1n**2) /
                      (gamma * M1n**2 - .5 * (gamma - 1.)))
        return M1n, M2n
        
    def M2(self,M1,theta,gamma=1.4):
        beta = self.beta(M1, theta)
        M1n, M2n = self.M1nM2n(M1, beta, gamma)
        M2 = M2n / np.sin(beta-theta)
        return M2
        
    def p2_p1(self,M1,theta,gamma=1.4):
        beta = self.beta(M1, theta)
        M1n = M1 * np.sin(beta)
        p2_p1 = 1.+2.*gamma/(gamma + 1.)*(M1n**2-1.)
        return p2_p1
        