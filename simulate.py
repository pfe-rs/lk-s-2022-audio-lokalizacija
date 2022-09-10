#! /bin/python3
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def triletaracija (x1, y1, x2, y2, x3, y2, r1, r2, r3):
    a = -2*x1 + 2*x2
    b = -2*y1 + 2*y2
    c = r1*r1 - r2*r2 - x1*x1 + x2*x2 - y1*y1 + y2*y2
    d = -2*x2 + 2*x3
    e = -2*y2 + 2*y3
    f = r2*r2 - r3*r3 - x2*x2 + x3*x3 - y2*y2 + y3*y3
    x = (c*e - f*b)/(e*a - b*d)
    y = (c*d - a*f)/(b*d - a*)

t = np.linspace(0,1,8000)
sig = signal.chirp(t,170,0.5,250)
sig[4000::] = np.zeros(4000)
# plt.plot(t,sig)
# plt.show()
zavisnost = np.zeros((100,2))

node1 = (.0,.0)
node2 = (.7,.5)
node3 = (.11,.2)

for i in range(1,100):
    
    # kasnjenje = float(input("Udaljenost[m/s]:"))
    kasnjenje = i/10;
    kasnjenje_t = round(kasnjenje/340 * 8000);
    # print("Kasnjenje[s]:",kasnjenje/340)
    sig2 = 0 * t
    sig2[kasnjenje_t:kasnjenje_t + 4000:] = sig[0:4000:]
    
    # plt.plot(t,sig2)
    # plt.show()

    # sum
    me, sigma = 0, 0.1 
    summ = np.random.normal(me, sigma, 8000)

    sig2 = sig2 + summ


    # fade

    sig2 = sig2  / (kasnjenje )


    # plt.plot(sig2)
    # plt.show()


    # diskretizacija 
    sig22 = (sig2*255).astype(np.int8)

    # plt.plot(sig22)
    # plt.show()
    # korelacija



    korelacija = signal.correlate(sig2, sig)

    udaljenost = (korelacija.argmax() - 8000) * 1/8000 * 340
    zavisnost[i,1] = kasnjenje
    zavisnost[i,0] = udaljenost
    


    #print("Udaljenost[m]:",udaljenost)


    # plt.plot(korelacija)
    # plt.show()
#print(zavisnost)
plt.plot(zavisnost[::,0] - zavisnost[::,1])
plt.show()