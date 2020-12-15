import time
import machine, neopixel
from colors import *

def cycle():
    # cycle
    for i in range(
            N):
        for j in range(N):
            np[j] = (0, 0, 0)
        np[i % N] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)


def bounce(color,bg_color):
    for i in range(4 * N):
        for j in range(N):
            np[j] = bg_color
        if (i // N) % 2 == 0:
            np[i % N] = color
        else:
            np[N - 1 - (i % N)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)


def blink(delay):
    for i in range(0, 4 * 256, 8):
        for j in range(N/2):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[2*j] = (0,0,val)
            np[2*j+1] = (0,val,0)

        np.write()
        time.sleep_ms(delay)
        for j in range(N/2):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[2*j]   = (0,val,0)
            np[2*j+1] = (0,0,val)

        np.write()
        time.sleep_ms(delay)

def setSolid(color):
    for i in range(N):
        np[i] = color
    np.write()

def blink_rgb(index,delay):
    old_color = np[index]
    np[index] = red
    np.write()
    time.sleep_ms(delay)
    np[index] = green
    np.write()
    time.sleep_ms(delay)
    np[index] = blue
    np.write()
    time.sleep_ms(delay)
    np[index] = old_color
    np.write()

def run(color,delay,back=False):

    direction = [1,-1]
    color_old=[(),(),()]
    for i in range(1,N-1):
        first_led  = (i-1)*direction[back]
        second_led = i*direction[back]
        third_led  = (i+1)*direction[back]

        color_old[0] = np[first_led]
        color_old[1] = np[second_led]
        color_old[2] = np[third_led]
        np[first_led] = color
        np[second_led] = color
        np[third_led] = ledOff
        np.write()
        time.sleep_ms(delay)

        np[first_led] = color_old[0]
        np[second_led]   = color_old[1]
        np[third_led] = color_old[2]
        np.write()
        time.sleep_ms(delay)


def setLogisticMap(x,r):
    for j in range(N):
        x = r*x*(1-x)
        np[j] = hsv_to_grb(x, 1, 0.2)
    np.write()
    return x

def ping_pong():
    x = 0.7
    for i in range(N):
        r = 3.6 + 0.4*i/N
        x = setLogisticMap(x,r)
        run(red,5,i%2)

def tohex(x):
    return int(x*255)

def hsv_to_grb(h, s, v):
    if s == 0.0: return (tohex(v), tohex(v), tohex(v))
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (tohex(t), tohex(v), tohex(p))
    if i == 1: return (tohex(v), tohex(q), tohex(p))
    if i == 2: return (tohex(v), tohex(p), tohex(t))
    if i == 3: return (tohex(q), tohex(p), tohex(v))
    if i == 4: return (tohex(p), tohex(t), tohex(v))
    if i == 5: return (tohex(p), tohex(v), tohex(q))

def shift_down(index=[],runningColor=ledOff):
    np[N-1] = np[0]
    for i in range(N-1):
        np[i] = np[i+1]

    if index != []:
        for i in range(N):
            np2[i] = np[i]

        np2[index % N]     = runningColor
        np2[(index+1) % N] = runningColor
        np2.write()
    else:
        np.write()

def loop_down(delay,count):
    for i in range(N*count):
        shift_down()
        time.sleep_ms(delay)


def shift_up():
    np[0] = np[N-1]
    for i in range(1,N):
        np[N-i] = np[N-i-1]
    np.write()

def loop_up(delay,count):

     for i in range(N*count):
         shift_up()
         time.sleep_ms(delay)

def swapfade():
    for j in range(N*2):
        for i in range(N):
            np[i] =hsv_to_grb(j/100,j/100,j/100)
        np.write()
        time.sleep_ms(10)

def rainbow(saturation):
    for i in range(N):
        np[i] =hsv_to_grb(i/N,1,saturation)
    np.write()

def sweep_rainbow(delay, count,saturation, runningColor=ledOff):
    for j in range(count*N):
        for i in range(N):
            np[i] =hsv_to_grb(j/N,1,saturation)
        np[j % N] = runningColor
        np[(j+1)%N] = runningColor
        np.write()
        time.sleep_ms(delay)

def loop_around(delay,count,runningColor):
    for i in range(N*count):
        shift_down(i%N,runningColor)
        time.sleep_ms(delay)

def dark_snake():
    np[2] = (1,1,1)
    np[3] = (1,0,0)
    np[4] = (0,1,0)
    np[5] = (0,0,1)
    
    np[6]  = (1,0,1)
    np[7]  = (0,1,1)
    np[8]  = (1,1,0)
    
    np[42] = (10,10,10)
    np[43] = (10,0,0)
    np[44] = (0,10,0)
    np[45] = (0,0,10)
    
    np[49] = (0,144,0)
    np[48] = (0,0,134)
    
    np.write()
    
    loop_around(10,100,green)
    


##############################
# main code
N = 100
np = neopixel.NeoPixel(machine.Pin(4), N)
np2 = neopixel.NeoPixel(machine.Pin(4), N)

# NC = len(color)

# setSolid(ledOff)
# np[74] = pink
# np.write()


# dark_snake()


########################################
# wish your color
# np[42] = red
# np[33] = green
# np[2] = yellow
# np[8] = blue

# for i in range(15,20):
#     np[i] = blue

# np[17] = pink

# np[44] = white

# np[27] =  (71,141,23)

# for i in range(100):
#     if i % 2:
#         time.sleep_ms(3000)
#         np[26] = ledOff
#     else:
#         time.sleep_ms(2000)
#         np[26] = blue

#     np.write()

# for i in range(10):
#     setSolid(blue)
#     setSolid(ledOff)
#     setSolid(red)
#     setSolid(ledOff)
#     setSolid(green)
#     setSolid(ledOff)




# for i in range(50):
#     run(ledOff, 10, i % 2)
# loop_around(1,100,pink)

# bounce(blue, ledOff)

# blink(10)

# setSolid(blue)

# swapfade()

# rainbow(0.5)
# loop_up(5,1)
# loop_down(5,1)
# setSolid(ledOff)

# sweep_rainbow(1,10,0.5,blue)

# sweep_rainbow_run(20,10,0.5)

# setLogisticMap(0.7234, 3.995232)
rainbow(0.2)

# setLogisticMap(0.7234, 3.995232)

np[10] = blue
np[11] = blue
np.write()
while 1:
    loop_around(500,250,pink)
    ping_pong()


