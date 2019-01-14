# -*- coding: utf-8 -*-
 
global xytovalue,xytodist
xytovalue,xytodist={},{}

import PIL
#im=PIL.Image.open("512789ImageFormesT0.jpg")
#im=PIL.Image.open("cadrillage.jpg")
#im=PIL.Image.open("2carre.bmp")
#im=PIL.Image.open("chat.jpg")
im=PIL.Image.open("paysage.jpg")
im=im.convert('RGB')
im2=PIL.Image.new("RGB", (im.size[0],im.size[1]), 'white')

dic={}

#CORRECTION DE L'IMAGE
if False:
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if im.getpixel((i,j))[0]<50:
                im.putpixel((i,j),(0,0,0))
            elif im.getpixel((i,j))[0]>200:
                im.putpixel((i,j),(255,255,255))
            else:
                print 'ERREUR !!'
                print i,j,im.getpixel((i,j))[0]

class arraynumber(list):
    """Liste de flottants compatibles aux opérations élémentaires"""
    def add(self,liste):
        for i in range(len(self)):
            self[i]+=liste[i]
    def scalar(self,scal):
        for i in range(len(self)):
            self[i]=self[i]*scal

#Création d'une image décalée de 1 pixel vers la droite
for a in range(im.size[0]-1):
    for b in range(im.size[1]):
        dic[(a,b)]=im.getpixel((a,b))
for a in range(im2.size[0]-1):
    for b in range(im2.size[1]):
        im2.putpixel((a+1,b),(dic[a,b]))


#Parties isolées de tracker
def eigenvalues(im,x,y,lenwindow):
    """Renvoie les valeurs propres associés à une fenêtre centrée sur un pixel"""
    G=arraynumber([0,0,0]) #g11, g12=g21, g22
    for i in range(x-lenwindow,x+lenwindow+1):
        for j in range(y-lenwindow,y+lenwindow+1):
            gradx=( im.getpixel((i+1,j))[0]-im.getpixel((i-1,j))[0] )/2.
            grady=( im.getpixel((i,j+1))[0]-im.getpixel((i,j-1))[0] )/2.
            G.add(arraynumber([gradx**2, gradx*grady, grady**2]))
    Tr=G[0]+G[2] #a+d
    det=G[0]*G[2]-G[1]**2 #ad-bc
    if Tr**2-4*det < 0: print "WTF !!"
    sqrtdelta=(Tr**2-4*det)**0.5 #sqrt(b^2-4ac)
    if sqrtdelta!=sqrtdelta:
        print "Un NaN sauvage apparait !"
    ev1=(Tr+sqrtdelta)/2. #-b+sqrt(delta)
    ev2=(Tr-sqrtdelta)/2. #faire gaffe, b = -Tr !
    return ev1,ev2

def remplirxytovalue(im,lenwindow):
    """Crée et remplit xytovalue (dictionnaire pixel -> valeurs propres)"""
    global xytovalue    
    xytovalue={}
    for i in range(lenwindow+1,im.size[0]-lenwindow-1):
        print i
        for j in range(lenwindow+1,im.size[1]-lenwindow-1):
            result=eigenvalues(im,i,j,lenwindow)
            xytovalue[i,j]=min(result)


##Début partie réellement utile
def colorier(im,value):
    """Colorie une image à partir d'xytovalue et d'un seuil"""
    pointsdinteret=[i for i in xytovalue if xytovalue[i]>=value]
    for i in pointsdinteret:
        im.putpixel(i,(255,0,0))
    im.show()

def imagespectrale(im):
    """Crée l'image en intensité de valeurs propres"""
    #nécessaire de reprogrammer le max
    global xytovalue
    EVmax=0
    for i in xytovalue:
        if xytovalue[i]>EVmax:
            EVmax=xytovalue[i]
    alpha=255./EVmax
    xyto0255={i:int(xytovalue[i]*alpha) for i in xytovalue}
    imghost=PIL.Image.new("RGB", (im.size[0],im.size[1]), 'white')
    for i in xyto0255:
        value=xyto0255[i]
        imghost.putpixel(i,(255-value,255-value,255-value) )
    imghost.show()

def tracker(im,im2,lenwindow):
    global xytovalue,xytodist
    xytovalue,xytodist={},{}
    for x in range(lenwindow+1,im.size[0]-lenwindow-1):
        print x
        for y in range(lenwindow+1,im.size[1]-lenwindow-1):
            G=arraynumber([0,0,0]) #g11, g12=g21, g22
            e=arraynumber([0,0])
            for i in range(x-lenwindow,x+lenwindow+1):
                for j in range(y-lenwindow,y+lenwindow+1):
                    gradx=( im.getpixel((i+1,j))[0]-im.getpixel((i-1,j))[0] )/(2.*255)
                    grady=( im.getpixel((i,j+1))[0]-im.getpixel((i,j-1))[0] )/(2.*255)
                    G.add(arraynumber([gradx**2, gradx*grady, grady**2]))
                    temparray=arraynumber([gradx,grady])
                    temparray.scalar((im.getpixel((i,j))[0] - im2.getpixel((i,j))[0])/255.)
                    e.add(temparray)
#            print G
#            print e
            Tr=G[0]+G[2]
            det=G[0]*G[2]-G[1]**2
            sqrtdelta2=Tr**2-4*det
            sqrtdelta=(sqrtdelta2)**0.5  if sqrtdelta2>0 else 0
            ev1=(Tr+sqrtdelta)/2.
            ev2=(Tr-sqrtdelta)/2.
            if (i,j)==(78,10):
                print e
                print Tr,type(Tr)
                print det,type(det)
                print sqrtdelta,type(sqrtdelta)
                print ev1
                print ev2
            xytovalue[x,y]=min(ev1,ev2)
            if det!=0:
                Ginv=arraynumber([ G[0],-G[1],G[2] ])
                Ginv.scalar( 1/float(det) )
                xytodist[x,y]=arraynumber([ Ginv[0]*e[0] + Ginv[1]*e[1] , Ginv[1]*e[0] + Ginv[2]*e[1] ])


def moyenneinteressante(seuil):
    global xytodist,xytovalue
    termes=0.
    somme=arraynumber([0.,0.])
    for i in xytodist:
        if xytovalue[i]>=seuil:
            termes+=1.
            somme.add( xytodist[i] )
    somme.scalar(1/termes)
    return somme