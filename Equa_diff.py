# name:      Equa_diff
# author:    Lundrih (https://github.com/EyumLundrih)


from math import *
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# variables
dt = 0.01 # differentielle de temps
vo = -12  # la vitesse a un signe moins car elle est donner sur -uO
g = 9.81  # gravite
l = 1.7  # longueur de la corde entre 1 et 2
Oi = pi/2  # angle initial <pi/2 pour les petits angles
# forme a priori: ddO/ddt +KdO/dt + sin(O)*g/l=0
K = 1/4# coefficient de frottements
D = (K ** 2) - 4 * (g / l) # discriminant de l'équation caractéristique associéé a l'equa diff comme on suppose les frottements faible,(dans ce cas: K<(4*(g/l)) d'ou K<19,62 !!!) on a D<0
w = sqrt(-D) / 2 #pseudo-pulsation, Im(racine)
r = -K / (l * 2)#partie réelle des racines , Re(racine)
tf = 10000 # temps maximum

# On définit une liste d'indice du temps
temps = [t for t in range(0, tf)]

#Fonction solution de l'Equa diff: O(t); position en fonction du temps
def P(t,Oi,vo):
    return (Oi * cos(w * t * dt) + (vo / w) * sin(w * t * dt)) * exp(r*t*dt)
#Fonction solution de l'Equa diff: dO(t)/dt; vitesse en fonction du temps
def Vp(t,Oi,vo):
    return (((-Oi*w*sin(w*t*dt)+vo*cos(w*t*dt))*exp(r*t*dt))+(r*(Oi * cos(w * t * dt) + (vo / w) * sin(w * t * dt)) * exp(r*t*dt)))
#on obtient les liste de la postion et de la vitesse en fonction du temps
sol1=[P(t,Oi,vo) for t in temps]
vsol1=[Vp(t,Oi,vo) for t in temps]
# fonction inutile juste pour tester que le modulo marche bien
def max_sol(sol1):
    ref=sol1[0]
    for i in range(1, tf):
        if abs(sol1[i])>abs(ref):
            ref=sol1[i]
    return ref

#on cherche a obenir une réponse de postition valable pour les grands angles
#on cree un modulo pour contenir les valeur de la position sur un intervale [-pi,pi]
#puis si l'angle était supérieur a pi ou inférieur a -pi, l'approximation du sin n'étant plus valable, on change calcule une nouvelle réponse en changeant les conditons initiales
#par la position a laquelle le pendule dépasse l'intervale et la vitesse a cette instant on doit aussi renitialiser le temps
def solution(vo, Oi,):
    liste_angle = []
    vf=vo
    Of=Oi
    tt=0
    for t in temps:
        tt+=1
        p=P(tt,Of,vf)
        if abs(p)>pi:
            n=0
            vf = Vp(tt, Of, vf)*0.5
            while p>pi and p>0:
                n+=1
                p-=2*pi
                tt=0
                if n==20:
                    break
            while p<(-pi) and p<0:
                p+=2*pi
                n += 1
                tt=0
                if n==20:
                    break
            liste_angle.append(p)
            Of = p
        else:
            liste_angle.append(p)
    return liste_angle

l_angle = solution(vo, Oi)
#l_angle = sol1 # a tester pour voir la difference aux petits angles (Oi=pi/2 ; vo=-12

max_sol=max_sol(l_angle)
print(max_sol)# pour voir si le modulo est efficace
print(l_angle)# liste des positions

def postition(l, Oi):
    #on rajoute volontairement 15 point initiaux pour que le pendule ne 'parte pas tout de suite'
    sol = [(l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0),
           (l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0),
           (l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0),
           (l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0),
           (l * sin(Oi), -l * cos(Oi), 0), (l * sin(Oi), -l * cos(Oi), 0)]
    for s in l_angle:
        sol.append((l * sin(s), -l * cos(s), 0))
    return sol


def energie_cinetique():
    ec = []
    for t in temps:
        e = 1 / 60000  * ( Vp(t,Oi,vo)/ dt) ** 2 # comme il y'a a pas de masse (tout est dans K) on met un coef pour que l'ec et l'ep soit du meme ordre de grandeur pour vo=0
        ec.append(e)
    return ec


def energie_potentielle():
    ep = []
    for i in l_angle:
        e = -l * cos(i) + l
        ep.append(e)
    return ep


def energie_meca():
    em = []
    for i in temps:
        e = ec[i] + ep[i]
        em.append(e)
    return em


ec = energie_cinetique()
ep = energie_potentielle()
em = energie_meca()

#quelques test sur le pendule

#plt.plot(temps, l_angle)
#plt.plot(temps, ec)
#plt.plot(temps, ep)
#plt.plot(temps, em)
#plt.plot(sol1, vsol1)
#plt.show()

'''
def F5(Y,t):
    theta,thetap=Y
    return np.array([thetap, -np.sin(theta)-1/5*Y[1]])
temps3=np.linspace(0, 120 ,120000)
sol=odeint(F5,[np.pi/2, 5], temps3)
theta, thetap = sol[:,0],sol[:,1]
plt.plot(temps3, theta)
plt.show()

solob=[theta[t] for t in range(0, 120000)]
print(solob)
'''
#        s=Oi*cos(sqrt(g/l)*0.01*t)
# a = l / (6 * g)
# b = (l * -K) / (2 * (g ** 2))
# c = ((l * (-K ** 2)) / (g ** 3)) - ((l ** 2) / (g ** 2))
# y = ((l * (-K ** 3)) / (g ** 4)) - ((-K * (l ** 2)) / (g ** 3)) - (((l ** 2) * -K) / (g ** 3))


# def f(t):
#   return a * (t ** 3) + b * (t ** 2) + c * t + y
