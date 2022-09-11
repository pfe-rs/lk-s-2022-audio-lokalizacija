#! /bin/python3
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import math

def trilateracija (tacka1, tacka2, tacka3, r1, r2, r3):
    x1, y1 = tacka1
    x2, y2 = tacka2
    x3, y3 = tacka3
    a = -2*x1 + 2*x2
    b = -2*y1 + 2*y2
    c = r1*r1 - r2*r2 - x1*x1 + x2*x2 - y1*y1 + y2*y2
    d = -2*x2 + 2*x3
    e = -2*y2 + 2*y3
    f = r2*r2 - r3*r3 - x2*x2 + x3*x3 - y2*y2 + y3*y3
    x = (c*e - f*b)/(e*a - b*d)
    y = (c*d - a*f)/(b*d - a*e)
    return x,y

def pitagora (tacka, x2, y2):
    x1,y1 = tacka
    a = abs (x1-x2)
    b = abs (y1-y2)
    c = math.sqrt (a*a + b*b)
    return c

def presek (tacka0, r0, tacka1, r1):
    x0, y0 = tacka0
    x1, y1 = tacka1
    d = math.sqrt((x0-x1)^2 + (y0-y1)^2)
    a=(r0**2-r1**2+d**2)/(2*d)
    h=math.sqrt(r0**2-a**2)
    x2=x0+a*(x1-x0)/d
    y2=y0+a*(y1-y0)/d
    x3=x2+h*(y1-y0)/d
    y3=y2-h*(x1-x0)/d

    x4=x2-h*(y1-y0)/d
    y4=y2+h*(x1-x0)/d

    return (x3, y3, x4, y4)

def bliza (tacka0, tacka1, tackax):
    x0, y0 = tacka0
    x1, y1 = tacka1
    x, y = tackax
    d0 = math.sqrt((x0-x)^2 + (y0-y)^2)
    d1 = math.sqrt((x1-x)^2 + (y1-y)^2)
    if d1 > d0:
        return d0
    else:
        return d1

def greskaDis (tacka1, tacka2, tacka3, tackax):
    x1, y1 = tacka1
    x2, y2 = tacka2
    x3, y3 = tacka3
    x, y = tackax
    d1 = math.sqrt((x1-x)^2 + (y1-y)^2)
    d2 = math.sqrt((x2-x)^2 + (y2-y)^2)
    d3 = math.sqrt((x3-x)^2 + (y3-y)^2)
    maks = d1
    if d2 > maks:
        maks = d2
    if d3 > maks:
        maks = d3
    return maks

t = np.linspace(0,1,8000)
sig = signal.chirp(t,170,0.5,250)
sig[4000::] = np.zeros(4000)
# plt.plot(t,sig)
# plt.show()
zavisnost = np.zeros((100,2))
eps = 0.005
node1 = (.0,.0)
node2 = (.7,.5)
node3 = (.14,-.2)

# lokacija_real = np.zeros((15,2))
# lokacija = np.zeros((50,2), dtype=(float,2))
# lokacija = np.zeros(50)

# for i in range(1,100):
# i = 0
# for x in range (-3,13):
#     for y in range(3,1,-1):
#         i+=1
        # kasnjenje = float(input("Udaljenost[m/s]:"))
        # kasnjenje = i/10;

        # kasnjenje_t = round(kasnjenje/340 * 8000);
        kasnjenje1 = round(distanca1 / 340 * 8000)
        kasnjenje2 = round(distanca2 / 340 * 8000)
        kasnjenje3 = round(distanca3 / 340 * 8000)

        sig1 = 0 * t
        sig2 = 0 * t
        sig3 = 0 * t

        sig1[kasnjenje1:kasnjenje1 + 4000:] = sig[0:4000:]
        sig2[kasnjenje2:kasnjenje2 + 4000:] = sig[0:4000:]
        sig3[kasnjenje3:kasnjenje3 + 4000:] = sig[0:4000:]



        # sum
        me, sigma = 0, 0.1
        summ = np.random.normal(me, sigma, 8000)
        sig1 += summ
        summ = np.random.normal(me, sigma, 8000)
        sig2 += summ
        summ = np.random.normal(me, sigma, 8000)
        sig3 += summ

        # fade
        sig1 = sig1  / (kasnjenje1*kasnjenje1)
        sig2 = sig2  / (kasnjenje2*kasnjenje2)
        sig3 = sig3  / (kasnjenje3*kasnjenje3)


        # diskretizacija
        sig1 = (sig1*255).astype(np.int8)
        sig2 = (sig2*255).astype(np.int8)
        sig3 = (sig3*255).astype(np.int8)

        # plt.plot(sig22)
        # plt.show()

        # korelacija

        korelacija1 = signal.correlate(sig1, sig)
        korelacija2 = signal.correlate(sig2, sig)
        korelacija3 = signal.correlate(sig3, sig)

        udaljenost1 = (korelacija1.argmax() - 8000) * 1/8000 * 340
        udaljenost2 = (korelacija2.argmax() - 8000) * 1/8000 * 340
        udaljenost3 = (korelacija3.argmax() - 8000) * 1/8000 * 340

        print("Greska1:",distanca1 - udaljenost1)
        print("Greska2:",distanca2 - udaljenost2)
        print("Greska3:",distanca3 - udaljenost3)

        xloc, yloc = trilateracija(node1,node2, node3, udaljenost1, udaljenost2, udaljenost3)
        lokacija[i] = pitagora((x,y),xloc,yloc)
        # lokacija[i,0] = (x,y)
        # lokacija[i,1] = (xloc, yloc)
        # zavisnost[i,1] = kasnjenje
        # zavisnost[i,0] = udaljenost
        tackax = (xloc, yloc)
        tacka1 = bliza(presek(node1, udaljenost1+eps, node2, udaljenost2+eps))
        tacka2 = bliza(presek(node2, udaljenost2+eps, node3, udaljenost3+eps))
        tacka3 = bliza(presek(node3, udaljenost2+eps, node1, udaljenost1+eps))
        greska = greskaDis(tacka1, tacka2, tacka3, tackax)



## lepi plotovi eksterno
figure, axes = plt.subplots()

x,y = 0.7, 0.4
for cvor in node1, node2, node3:
    distanca1 = pitagora(node1, x,y)
    distanca2 = pitagora(node2, x,y)
    distanca3 = pitagora(node3, x,y )

    cc = plt.Circle(cvor , 0.4, fill=False, linestyle='--', edgecolor='r' ) ## prvo je zapakovane kordinate, udaljenost + eps
    ac = plt.Circle(cvor, 0.3, fill = False) ## opet prvo zapakovane koordinate pa onda udaljenost koju dobijemo
    bc = plt.Circle(cvor, 0.001) ## ovo je samo tacka gde se nalazi, postelovati mozda da automatski bude manja

    axes.add_artist( cc ) ## dodajemo krug, epsilon krug i tacku
    axes.add_artist(bc)
    axes.add_artist(ac)

    axes.plot(0.5,0.8, marker='x')
    axes.errorbar(0.5,0.8,xerr = 0.1, yerr = 0.1)

axes.set_aspect( 1 )
plt.xlim([0,1])
plt.ylim([0,1])
plt.title( 'Trilateracija' )
plt.show()





# plt.plot(lokacija)
# plt.show()

    #print("Udaljenost[m]:",udaljenost)


    # plt.plot(korelacija)
    # plt.show()
#print(zavisnost)
#plt.plot(zavisnost[::,0] - zavisnost[::,1])
#plt.show()