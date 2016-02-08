import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def pulse_zero(x, k, fract):
    """
    This function returns True if x is equal
    to k*pi + fract. It provides the boundaries
    inside which the waveform is not equal to 0.
    The parameter k is incremented with each
    period of the waveform.

    """
    cnd1 = x >= k
    cnd2 = x < (fract + k)
    cnd3 = x >= (np.pi + k)
    cnd4 = x < (np.pi + fract + k)
    return ((cnd1 and cnd2) or (cnd3 and cnd4))

def make_pulse(fract):
    """
    Function to create the pulse and the relevant
    chopped sin, according to the slider value.
    TODO: document this mess

    """
    repeats = 2 # more repeats create ugly display
    xf = np.linspace(0, repeats, 250*repeats)
    lf = len(xf)/repeats
    zf = [1 for i in xrange(len(xf))]
    yt = 2*np.pi*xf
    for k in xrange(0, 2*repeats, 2):
        for i in xrange(lf*k/2, lf + lf*k/2):
            if pulse_zero(yt[i], k*np.pi, fract):
                zf[i] = 0
            else:
                zf[i] = 1
    pulse = [0 for i in xrange(len(zf))]
    trig = 0
    for i in range(len(zf)):
        if trig<10 and zf[i]==1 :
            pulse[i] = 1
            trig += 1
        if zf[i] == 0 :
            trig = 0

    y = np.sin(2*np.pi*x)
    for i in xrange(len(y)):
        y[i] *= zf[i]

    return y, pulse

def update(val):
    """
    Triggered when the slider changes value.
    It then regenerates the plot, creating
    the visualization of the value change.

    """
    new_dim = np.pi - sl.val
    new1, new2 = make_pulse(new_dim)
    p1.set_ydata(new1)
    p2.set_ydata(new2)
    fig.canvas.draw_idle()

def automate():
    """
    Placeholder to implement a method that
    creates an automated visualization.

    """
    print 'auto'

fract = np.pi/2
repeats = 2
x = np.linspace(0, repeats, 250*repeats)
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)
y1, y2 = make_pulse(fract)

p1, = plt.plot(x, y1, linewidth=1.5)
#plt.plot(x, z, 'g')
p2, = plt.plot(x, y2, 'r', alpha=0.73)
p3, = plt.plot(x, np.sin(2*np.pi*x), 'b--', alpha=0.37)
plt.axis([0, repeats, -2, 2])
plt.gca().axes.get_xaxis().set_ticklabels([])
plt.gca().axes.get_yaxis().set_ticklabels([])
plt.grid(True)
axdim = plt.axes([0.2, 0.1, 0.65, 0.03], axisbg='lightgoldenrodyellow')
#plt.ylim(-2, 2)
fig.canvas.set_window_title('Dimmer visualization')
sl = Slider(axdim, 'dim value', 0.05, np.pi-0.05, valinit=fract)
sl.on_changed(update)
plt.show()
automate()
