#! /bin/python3
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
t = np.linspace(0,1,8000)
sig = signal.chirp(t,170,0.5,250)
sig[4000::] = np.zeros(4000)
plt.plot(t,sig)
plt.show()
kasnjenje = float(input("Udaljenost[m/s]:"))
kasnjenje_t = round(kasnjenje/340 * 8000);
print("Kasnjenje[s]:",kasnjenje/340)
sig2 = 0 * t
sig2[kasnjenje_t:kasnjenje_t + 4000:] = sig[0:4000:]
plt.plot(t,sig2)
plt.show()


# sum
me, sigma = 0, 0.1 
summ = np.random.normal(me, sigma, 8000)

sig2 = sig2 + summ


# fade

sig2 = sig2  / (kasnjenje )


plt.plot(sig2)
plt.show()


# diskretizacija 
sig22 = (sig2*255).astype(np.int8)

plt.plot(sig22)
plt.show()

# korelacija



korelacija = signal.correlate(sig2, sig)

udaljenost = (korelacija.argmax() - 8000) * 1/8000 * 340
print("Udaljenost[m]:",udaljenost)


plt.plot(korelacija)
plt.show()
