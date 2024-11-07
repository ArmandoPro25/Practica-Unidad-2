from machine import Pin, PWM, time_pulse_us
import time

# Configuración de los pines del sensor ultrasonico
Trig_Pin_Front = 17
Echo_Pin_Front = 34
Trig_Pin_Back = 32
Echo_Pin_Back = 12

trigBack = Pin(Trig_Pin_Back, Pin.OUT)
echoBack = Pin(Echo_Pin_Back, Pin.IN)
trigFront = Pin(Trig_Pin_Front, Pin.OUT)
echoFront = Pin(Echo_Pin_Front, Pin.IN)

# Configuración de los pines del Motor A
in1 = Pin(14, Pin.OUT)
in2 = Pin(27, Pin.OUT)
enA = PWM(Pin(13), freq=1000)

# Configuración de los pines del Motor B
in3 = Pin(33, Pin.OUT)
in4 = Pin(25, Pin.OUT)
enB = PWM(Pin(26), freq=1000)

# Configuración de los pines de los LEDs
ledRed = Pin(4, Pin.OUT)
ledYellow = Pin(16, Pin.OUT)


def medir_distancia():
    # Medición del sensor trasero
    trigBack.value(0)
    time.sleep_us(2)
    trigBack.value(1)
    time.sleep_us(10)
    trigBack.value(0)
    
    # Medición del sensor frontal
    trigFront.value(0)
    time.sleep_us(2)
    trigFront.value(1)
    time.sleep_us(10)
    trigFront.value(0)

    duracionBack = time_pulse_us(echoBack, 1, 30000)
    duracionFront = time_pulse_us(echoFront, 1, 30000)

    if duracionBack == -1:
        distanciaBack = None
    else:
        distanciaBack = (duracionBack * 0.0343) / 2

    if duracionFront == -1:
        distanciaFront = None
    else:
        distanciaFront = (duracionFront * 0.0343) / 2

    return distanciaBack, distanciaFront

def avanzar():
    in1.value(1)
    in2.value(0)
    enA.duty(1023)

    in3.value(1)
    in4.value(0)
    enB.duty(1023)
    
    ledRed.value(0)
    ledYellow.value(1)

def retroceder():
    in1.value(0)
    in2.value(1)
    enA.duty(1023)

    in3.value(0)
    in4.value(1)
    enB.duty(1023)
    
    ledRed.value(1)
    ledYellow.value(0)

while True:
    distanciaBack, distanciaFront = medir_distancia()

    if distanciaFront is not None:
        print("Distancia Frontal:", distanciaFront, "cm")
        print("Distancia Trasera:", distanciaBack, "cm")

        if distanciaFront > 10:
            avanzar()
        else:
            retroceder()
    
    time.sleep(0.5)
