<!----
Source code from
http://www.dept.aoe.vt.edu/~devenpor/aoe3114/calc.html
------->

<SCRIPT>
<!----- ISENTROPIC ------->
function isent(form) {
  i=form.i.selectedIndex
  g=eval(form.g.value)
  v=eval(form.v.value)
  if(g<=1.0) {
    alert("gamma must be greater than 1")
    return}

  if(i==1) {
    if(v>=1.0 || v<=0.0) {
      alert("T/T0 must be between 0 and 1")
      return}
    m=Math.sqrt(2.*((1./v)-1.)/(g-1.))}
  else if(i==2) {
    if(v>=1.0 || v<=0.0) {
      alert("p/p0 must be between 0 and 1")
      return}
    m=Math.sqrt(2.*((1./Math.pow(v,(g-1.)/g))-1.)/(g-1.))}
  else if(i==3) {
    if(v>=1.0 || v<=0.0) {
      alert("rho/rho0 must be between 0 and 1")
      return}
    m=Math.sqrt(2.*((1./Math.pow(v,(g-1.)))-1.)/(g-1.))}
  else if(i==4 || i==5) {
    if(v<=1.0) {
      alert("A/A* must be greater than 1")
      return}
    mnew=0.00001
    m=0.0
    if(i==5) {mnew=2.}
    while( Math.abs(mnew-m) > 0.000001) {
      m=mnew
      phi=aas(g,m)
      s=(3. - g) / (1. + g)
      mnew=m - (phi - v) / (Math.pow(phi * m,s) - phi / m)}}
  else if(i==6) {
    if(v<=0.0 || v>=90.0) {
      alert("Mach angle must be between 0 and 90")
      return}
    m=1./Math.sin(v*3.14159265359/180.)}
  else if(i==7) {
    numax=(Math.sqrt((g+1.)/(g-1.))-1)*90.
    if(v<=0.0 || v>=numax) {
      alert("Prandtl-Meyer angle must be between 0 and "+format(""+numax))
      return}
    mnew=2.0
    m=0.0
    while( Math.abs(mnew-m) > 0.00001) {
      m=mnew
      fm=(nu(g,m)-v)*3.14159265359/180.
      fdm=Math.sqrt(m*m-1.)/(1+0.5*(g-1.)*m*m)/m
      mnew=m-fm/fdm}}
  else {
    if(v<=0.0) {
      alert("M must be greater than 0")
      return}
    m=v}
  form.m.value=format(""+m)
  if(m>1.) {
    form.mu.value=format(""+Math.asin(1./m)*180/3.14159265359)
    form.nu.value=format(""+nu(g,m))}
  else if (m==1) {
    form.mu.value=90.
    form.nu.value=0.}
  else {
    form.mu.value=""
    form.nu.value=""}
  form.tt0.value = format(""+tt0(g,m))
  form.pp0.value = format(""+pp0(g,m))
  form.rr0.value = format(""+rr0(g,m))
  form.tts.value = format(""+tts(g,m))
  form.pps.value = format(""+pps(g,m))
  form.rrs.value = format(""+rrs(g,m))
  form.aas.value = format(""+aas(g,m))
}

<!----- NORMAL SHOCK ------->
function nsr(form) {
  i=form.i.selectedIndex
  g=eval(form.g.value)
  v=eval(form.v.value)
  if(g<=1.0) {
    alert("gamma must be greater than 1")
    return}

  if(i==1) {
    if(v>=1.0 || v<=Math.sqrt((g-1.)/2./g)) {
      alert("M2 must be between "+ format(""+Math.sqrt((g-1.)/2./g))+" and 1")
      return}
    m1=m2(g,v)}
  else if(i==2) {
    if(v<=1.0) {
      alert("p2/p1 must be greater than 1")
      return}
    m1=Math.sqrt((v-1.)*(g+1.)/2./g +1.)}
  else if(i==3) {
    if(v<=1.0 || v>=(g+1.)/(g-1.)) {
      alert("rho2/rho1 must be between 1 and "+format(""+((g+1.)/(g-1.))))
      return}
    m1=Math.sqrt(2.*v/(g+1.-v*(g-1.)))}
  else if(i==4) {
    if(v<=1.0) {
      alert("T2/T1 must be greater than 1")
      return}
    aa=2.*g*(g-1.)
    bb=4.*g-(g-1.)*(g-1.)-v*(g+1.)*(g+1.)
    cc=-2.*(g-1.)
    m1=Math.sqrt((-bb+Math.sqrt(bb*bb-4.*aa*cc))/2./aa)}
  else if(i==5) {
    if(v>=1.0 || v<=0.0) {
      alert("p02/p01 must be between 0 and 1")
      return}
    mnew=2.0
    m1=0.0
    while( Math.abs(mnew-m1) > 0.00001) {
      m1=mnew
      al=(g+1.)*m1*m1/((g-1.)*m1*m1+2.)
      be=(g+1.)/(2.*g*m1*m1-(g-1.))
      daldm1=(2./m1-2.*m1*(g-1.)/((g-1.)*m1*m1+2.))*al
      dbedm1=-4.*g*m1*be/(2.*g*m1*m1-(g-1.))
      fm=Math.pow(al,g/(g-1.))*Math.pow(be,1./(g-1.))-v
      fdm=g/(g-1.)*Math.pow(al,1/(g-1.))*daldm1*Math.pow(be,1./(g-1.))+Math.pow(al,g/(g-1.))/(g-1.)*Math.pow(be,(2.-g)/(g-1.))*dbedm1
      mnew=m1-fm/fdm}}
  else if(i==6) {
    vmax=Math.pow((g+1.)/2.,-g/(g-1.))
    if(v>=vmax || v<=0.0) {
      alert("p1/p02 must be between 0 and "+format(""+vmax))
      return}
    mnew=2.0
    m1=0.0
    while( Math.abs(mnew-m1) > 0.00001) {
      m1=mnew
      al=(g+1.)*m1*m1/2.
      be=(g+1.)/(2.*g*m1*m1-(g-1.))
      daldm1=m1*(g+1.)
      dbedm1=-4.*g*m1*be/(2.*g*m1*m1-(g-1.))
      fm=Math.pow(al,g/(g-1.))*Math.pow(be,1./(g-1.))-1./v
      fdm=g/(g-1.)*Math.pow(al,1/(g-1.))*daldm1*Math.pow(be,1./(g-1.))+Math.pow(al,g/(g-1.))/(g-1.)*Math.pow(be,(2.-g)/(g-1.))*dbedm1
      mnew=m1-fm/fdm}}

  else {
    if(v<=1.0) {
      alert("M1 must be greater than 1")
      return}
    m1=v}
  form.m1.value=format(""+m1)
  form.m2.value=format(""+m2(g,m1))
  p2p1=1.+2.*g/(g+1.)*(m1*m1-1.)
  form.p2p1.value = format(""+p2p1)
  p02p01=pp0(g,m1)/pp0(g,m2(g,m1))*p2p1
  form.p02p01.value=format(""+p02p01)
  form.r2r1.value=format(""+rr0(g,m2(g,m1))/rr0(g,m1)*p02p01)
  form.t2t1.value=format(""+tt0(g,m2(g,m1))/tt0(g,m1))
  form.p1p02.value=format(""+pp0(g,m1)/p02p01)

}

<!----- OBLIQUE SHOCK ------->
function osr(form) {
  i=form.i.selectedIndex
  g=eval(form.g.value)
  m1=eval(form.m.value)
  if(g<=1.0) {
    alert("gamma must be greater than 1")
    return}

  if(m1<=1.0) {
    alert("m1 must be greater than 1")
    return}
  if(i==0 || i==1) {
    delta=eval(form.a.value)*3.14159265359/180.
    if(delta>=3.14159265359/2.) {
      alert("Turning angle too large")
      return}
    if(delta<=0.0) {
      alert("Turning angle must be greater than zero")
      return}
    beta=mdb(g,m1,delta,i)
    if(beta<0.0) {
      form.beta.value=""
      form.delta.value=""
      form.m1n.value=""
      form.m2n.value=""
      form.m2.value="Shock"
      form.p2p1.value ="Detached"
      form.p02p01.value=""
      form.r2r1.value=""
      form.t2t1.value=""
      return}}
  else if(i==2) {
    beta=eval(form.a.value)*3.14159265359/180.
    if(beta>=3.14159265359/2.) {
      alert("Wave angle must be less than 90 deg.")
      return}
    if(beta-Math.asin(1./m1)<=0.0) {
      alert("Wave angle must be greater than Mach angle")
      return}
    delta=mbd(g,m1,beta)}
  else if(i==3) {
    m1n=eval(form.a.value)
    if(m1n<=1.0 || m1n>=m1) {
      alert("M1n must be between 1 and M1")
      return}
    beta=Math.asin(m1n/m1)
    delta=mbd(g,m1,beta)}

  m1n=m1*Math.sin(beta)
  form.beta.value=format(""+beta*180./3.14159265359)
  form.delta.value=format(""+delta*180/3.14159265359)
  form.m1n.value=format(""+m1n)
  form.m2n.value=format(""+m2(g,m1n))
  form.m2.value=format(""+form.m2n.value/Math.sin(beta-delta))
  p2p1 = 1.+2.*g/(g+1.)*(m1n*m1n-1.)
  form.p2p1.value = format(""+p2p1)
  p02p01=pp0(g,m1n)/pp0(g,m2(g,m1n))*p2p1
  form.p02p01.value= format(""+p02p01)
  form.r2r1.value=format(""+rr0(g,m2(g,m1n))/rr0(g,m1n)*p02p01)
  form.t2t1.value=format(""+tt0(g,m2(g,m1n))/tt0(g,m1n))

}
function tt0(g,m) {
   return Math.pow((1.+(g-1.)/2.*m*m),-1.)}

function pp0(g,m) {
   return Math.pow((1.+(g-1.)/2.*m*m),-g/(g-1.))}

function rr0(g,m) {
   return Math.pow((1.+(g-1.)/2.*m*m),-1./(g-1.))}

function tts(g,m) {
   return tt0(g,m)*(g/2. + .5)}

function pps(g,m) {
   return pp0(g,m)*Math.pow((g/2. + .5),g/(g-1.))}

function rrs(g,m) {
   return rr0(g,m)*Math.pow((g/2. + .5),1./(g-1.))}

function aas(g,m) {
   return 1./rrs(g,m)*Math.sqrt(1./tts(g,m))/m}

function nu(g,m) {
   n=Math.sqrt((g + 1.) / (g - 1.)) * Math.atan(Math.sqrt((g - 1.) / (g + 1.) * (m * m - 1.)))
   n=n - Math.atan(Math.sqrt(m * m - 1.))
   n=n*180./3.14159265359
   return n}

function m2(g,m1) {
   return Math.sqrt((1. + .5 * (g - 1.) * m1 * m1) / (g * m1 * m1 - .5 * (g - 1.)))}

function mdb(g,m1,d,i) {
  p=-(m1*m1+2.)/m1/m1-g*Math.sin(d)*Math.sin(d)
  q=(2.*m1*m1+1.)/Math.pow(m1,4.)+((g+1.)*(g+1.)/4.+(g-1.)/m1/m1)*Math.sin(d)*Math.sin(d)
  r=-Math.cos(d)*Math.cos(d)/Math.pow(m1,4.)

  a=(3.*q-p*p)/3.
  b=(2.*p*p*p-9.*p*q+27.*r)/27.

  test=b*b/4.+a*a*a/27.

  if(test>0.0) {return -1.0}
  else {
    if(test==0.0) {
      x1=Math.sqrt(-a/3.)
      x2=x1
      x3=2.*x1
      if(b>0.0) {
        x1*=-1.
        x2*=-1.
        x3*=-1.}}
    if(test<0.0) {
      phi=Math.acos(Math.sqrt(-27.*b*b/4./a/a/a))
      x1=2.*Math.sqrt(-a/3.)*Math.cos(phi/3.)
      x2=2.*Math.sqrt(-a/3.)*Math.cos(phi/3.+3.14159265359*2./3.)
      x3=2.*Math.sqrt(-a/3.)*Math.cos(phi/3.+3.14159265359*4./3.)
      if(b>0.0) {
        x1*=-1.
        x2*=-1.
        x3*=-1.}}

    s1=x1-p/3.
    s2=x2-p/3.
    s3=x3-p/3.

    if(s1<s2 && s1<s3) {
      t1=s2
      t2=s3}
    else if(s2<s1 && s2<s3) {
      t1=s1
      t2=s3}
    else {
      t1=s1
      t2=s2}

    b1=Math.asin(Math.sqrt(t1))
    b2=Math.asin(Math.sqrt(t2))

    betas=b1
    betaw=b2
    if(b2>b1) {
      betas=b2
      betaw=b1}

    if(i==0) {return betaw}
    if(i==1) {return betas}}
}

function mbd(g,m1,b) {
   return Math.atan((m1*m1*Math.sin(2.*b)-2./Math.tan(b))/(2.+m1*m1*(g+Math.cos(2.*b))))}

function format(s) {

  val=eval(s)

  if(Math.abs(val)<1.0e+6 && Math.abs(val)>1.0e-5) {
     if(val>0.0) return " "+s.substring(0,10)     //Medium size numbers w/o exponents
     else return s.substring(0,11)}

  ie=s.indexOf("e")     //Numbers with exponents

  if(ie>0) {
    mant=s.substring(0,ie)
    if(val>=0.0) mant=" "+mant
    if(mant.length>8) mant=mant.substring(0,8)
    if(Math.abs(val)>1.0) mant=mant+"e+"
    else if(Math.abs(val)<1.0) mant=mant+"e-"}

  else if(Math.abs(val)>=1.0e+6) {     //Large numbers without exponents
    if(val>0) mant=" "+s.substring(0,1)+"."+s.substring(1,6)+"e+"
    else mant=s.substring(0,2)+"."+s.substring(1,6)+"e+"}

  else if(Math.abs(val)<=1.0e-5) {      //Small numbers without exponents
    ip=s.indexOf(".")
    t=s.substring(ip+1,s.length)
    ix=1
    while(t.substring(0,1)=="0") {
      t=t.substring(1,t.length)
      ix++}
    if(val>0) mant=" "+t.substring(0,1)+"."+t.substring(1,6)+"e-"
    else mant=s.substring(0,2)+"."+t.substring(1,6)+"e-"}

  xpo=Math.abs(Math.floor(Math.log(Math.abs(val))/Math.log(10.0)))
  xpos=""+xpo
  if(xpo<10) return mant+"00"+xpos
  if(xpo<100) return mant+"0"+xpos
  return mant+xpos

}

</SCRIPT>
