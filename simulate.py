#! /bin/python3
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button

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
    d = math.sqrt((x0-x1)**2 + (y0-y1)**2)
    a=(r0**2-r1**2+d**2)/(2*d)
    h=math.sqrt(abs(r0**2-a**2))
    x2=x0+a*(x1-x0)/d
    y2=y0+a*(y1-y0)/d
    x3=x2+h*(y1-y0)/d
    y3=y2-h*(x1-x0)/d

    x4=x2-h*(y1-y0)/d
    y4=y2+h*(x1-x0)/d

    return (x3, y3, x4, y4)

def bliza (tacke01, tackax):
    x0, y0, x1, y1= tacke01
    # x0, y0 = tacka0
    # x1, y1 = tacka1
    x, y = tackax
    d0 = math.sqrt((x0-x)**2 + (y0-y)**2)
    d1 = math.sqrt((x1-x)**2 + (y1-y)**2)
    if d1 > d0:
        return (x0,y0)
    else:
        return (x1,y1)

def greskaDis (tacka1, tacka2, tacka3, tackax):
    x1, y1 = tacka1
    x2, y2 = tacka2
    x3, y3 = tacka3
    x, y = tackax
    d1 = math.sqrt((x1-x)**2 + (y1-y)**2)
    d2 = math.sqrt((x2-x)**2 + (y2-y)**2)
    d3 = math.sqrt((x3-x)**2 + (y3-y)**2)
    maks = d1
    if d2 > maks:
        maks = d2
    if d3 > maks:
        maks = d3
    return maks

Fs = 8000
brzina_zvuka = 340
duzina_snimka_s = 1
f1 = 170
f2 = 250
duzina_signala = 0.5
duzina_signala_odbirci = int(Fs * duzina_signala)

t = np.linspace(0,1,Fs)
sig = signal.chirp(t, f1, duzina_signala, f2)

sig[duzina_signala_odbirci::] = 0 ## prazni ostalu

eps = 0.005 ## eksperimentalna vrednost za gresku real world metrike

## A, B, C
node1 = (.0,.0) ## hardcode, treba da predje u plot
node2 = (.3,.7) 
node3 = (.8,.0)

# kasnjenje = float(input("Udaljenost[m/s]:"))

## lepi plotovi eksterno
figure, axes = plt.subplots()
figure.subplots_adjust(bottom=0.2)
plt.title( 'Trilateracija' )


x,y = 0.4, 0.3
def update_plot():
    global sig
    udaljenosti=[]
    distance = []
    for cvor in node1, node2, node3:
        distanca = pitagora(cvor, x,y) ## prava distanca bez ikakvih gresaka, idealno
        kasnjenje = round(distanca / brzina_zvuka * Fs)
        distance.append(distanca)
        # kasnjenje1 = round(distanca1 / brzina_zvuka * Fs)
        # kasnjenje2 = round(distanca2 / brzina_zvuka * Fs)
        # kasnjenje3 = round(distanca3 / brzina_zvuka * Fs)
        sig_mod = 0 * t
        # sig1 = 0 * t
        # sig2 = 0 * t
        # sig3 = 0 * t

        sig_mod[kasnjenje:kasnjenje + duzina_signala_odbirci] = sig[0:duzina_signala_odbirci]
        # sig1[kasnjenje1:kasnjenje1 + 4000:] = sig[0:4000:]
        # sig2[kasnjenje2:kasnjenje2 + 4000:] = sig[0:4000:]
        # sig3[kasnjenje3:kasnjenje3 + 4000:] = sig[0:4000:]

        # sum
        me, sigma = 0, 0.1
        summ = np.random.normal(me, sigma, Fs * duzina_snimka_s)
        sig_mod += summ
        # summ = np.random.normal(me, sigma, Fs)
        # sig2 += summ
        # summ = np.random.normal(me, sigma, Fs)
        # sig3 += summ

        # fade
        sig_mod = sig_mod  / pow(kasnjenje,2)
        # sig2 = sig2  / (kasnjenje2*kasnjenje2)
        # sig3 = sig3  / (kasnjenje3*kasnjenje3)
        #### !!! diskretizacija trenutno pod pauzom, izgleda pravilo probleme
        # diskretizacija
        ### !! korelise se sa original signalom koji je float, mora i on da se diskretizuje
        sig_mod = (sig_mod * np.iinfo(np.int8).max).astype(np.int8) ## ovde je bila greska, signed 8 bit ide do 127
        sig_diskret = (sig * np.iinfo(np.int8).max).astype(np.int8) 
        sig = (sig_diskret / np.iinfo(np.int8).max).astype(np.float16)
        sig_mod = (sig_mod / np.iinfo(np.int8).max).astype(np.float16) ## ovde je bila greska, signed 8 bit ide do 127
        
        # sig_mod = (sig_mod * 127).astype(np.int8)
        # sig1 = (sig1*255).astype(np.int8)
        # sig2 = (sig2*255).astype(np.int8)
        # sig3 = (sig3*255).astype(np.int8)

        # korelacija
        korelacija = signal.correlate(sig_mod, sig)
        # plt.plot(korelacija)
        # plt.show()
        # korelacija = signal.correlate(sig_mod, sig)
        # korelacija1 = signal.correlate(sig1, sig)
        # korelacija2 = signal.correlate(sig2, sig)
        # korelacija3 = signal.correlate(sig3, sig)

        ## udaljenost 
        udaljenost = (korelacija.argmax() - 8000) * 1/Fs * brzina_zvuka ## da ne bude 8000 vec da izracuna
        udaljenosti.append(udaljenost) ## append na listu
        # print(udaljenost)
        # udaljenost1 = (korelacija1.argmax() - Fs) * 1/Fs * brzina_zvuka
        # udaljenost2 = (korelacija2.argmax() - Fs) * 1/Fs * brzina_zvuka
        # udaljenost3 = (korelacija3.argmax() - Fs) * 1/Fs * brzina_zvuka


        # print("Greska1:",distanca1 - udaljenost1)
        # print("Greska2:",distanca2 - udaljenost2)
        # print("Greska3:",distanca3 - udaljenost3)

        prava_kruznica = plt.Circle(cvor, distanca, fill = False, edgecolor = 'g') ## real

        cc = plt.Circle(cvor , distanca + eps, fill=False, linestyle='--', edgecolor='y' ) ## prvo je zapakovane kordinate, udaljenost + eps
        ac = plt.Circle(cvor, udaljenost, fill = False, edgecolor = 'r') ## opet prvo zapakovane koordinate pa onda udaljenost koju dobijemo
        bc = plt.Circle(cvor, eps) ## ovo je samo tacka gde se nalazi, postelovati mozda da automatski bude manja

        axes.add_artist( cc ) ## dodajemo krug, epsilon krug i tacku
        axes.add_artist(bc)
        axes.add_artist(ac)
        axes.add_artist(prava_kruznica)
        

    axes.plot(x,y, marker='x') ## pravi x sa errorbar-om
    axes.errorbar(x,y,xerr = eps, yerr = eps)

    xloc, yloc = trilateracija(node1,node2, node3, udaljenosti[0], udaljenosti[1], udaljenosti[2])
    # tackax = (xloc, yloc)
    tackax = (x, y)
    tacka1 = bliza(presek(node1, distance[0]+eps, node2, distance[1]+eps), (x,y))
    tacka2 = bliza(presek(node2, distance[1]+eps, node3, distance[2]+eps), (x,y))
    tacka3 = bliza(presek(node3, distance[2]+eps, node1, distance[0]+eps), (x,y))
    
    # tacka1 = bliza(presek(node1, udaljenosti[0]+eps, node2, udaljenosti[1]+eps), (x,y))
    # tacka2 = bliza(presek(node2, udaljenosti[1]+eps, node3, udaljenosti[2]+eps), (x,y))
    # tacka3 = bliza(presek(node3, udaljenosti[2]+eps, node1, udaljenosti[0]+eps), (x,y))
    greska = greskaDis(tacka1, tacka2, tacka3, tackax)
    print(greska)

    x_plt = plt.Circle(tackax, greska,alpha = 0.5, facecolor = 'r') ## gde je x nadjen

    axes.plot(xloc,yloc, marker='*', color='g') ## nadjeni x 
    axes.add_artist(x_plt)
        
    axes.set_aspect( 1 )
    axes.set_xlim([-1.5,1.5])
    axes.set_ylim([-1.5,1.5])
    plt.draw()
    # plt.title( 'Trilateracija' )
    # plt.show()
    # udaljenost = []


def submitx(xnew):
    global x
    x = eval(xnew)
    update_plot()

def submity(ynew):
    global y
    y = eval(ynew)
    update_plot()

def submita(anew):
    global node1
    node1 = eval(anew)
    update_plot()

def submitb(bnew):
    global node2
    y = eval(bnew)
    update_plot()

def submitc(cnew):
    global node3
    node3 = eval(cnew)
    update_plot()

def obrisi(aaaa):
        axes.clear()
        update_plot()

#promena vrednosti za X(x,y)
boxx = figure.add_axes([0.1, 0.05, 0.1, 0.075])
boxy = figure.add_axes([0.23, 0.05, 0.1, 0.075])
boxa = figure.add_axes([0.36, 0.05, 0.1, 0.075])
boxb = figure.add_axes([0.49, 0.05, 0.1, 0.075])
boxc = figure.add_axes([0.62, 0.05, 0.1, 0.075])
clear = figure.add_axes([0.75, 0.05, 0.1, 0.075])

text_x = TextBox(boxx, "x:") 
text_x.on_submit(submitx)
text_x.set_val(str(x))
text_y = TextBox(boxy, "y:") 
text_y.on_submit(submity)
text_y.set_val(str(y))  
#
text_a = TextBox(boxa, "A:") 
text_a.on_submit(submita)
# text_a.set_val(str(node1[0]) + ',' + str(node1[1]))
text_a.set_val(node1)

text_b = TextBox(boxb, "B:") 
text_b.on_submit(submitb)
# text_b.set_val(str(node1[0]) + ',' + str(node1[1]))
text_b.set_val(node2)

text_c = TextBox(boxc, "C:") 
text_c.on_submit(submitc)
# text_c.set_val(str(node1[0]) + ',' + str(node1[1])) 
text_c.set_val(node3) 

bnext = Button(clear, "obrisi:")
bnext.on_clicked(obrisi)

# plt.xlim([-2.5,2.5])
# plt.ylim([-2.5,2.5])
plt.show()


# update_plot()

# plt.plot(lokacija)
# plt.show()

    #print("Udaljenost[m]:",udaljenost)


    # plt.plot(korelacija)
    # plt.show()
#print(zavisnost)
#plt.plot(zavisnost[::,0] - zavisnost[::,1])
#plt.show()