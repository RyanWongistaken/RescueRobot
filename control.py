import pigpio
import time
import xbox

class Controlthread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        joy = xbox.Joystick()
        # Motor Configuration
        # A----C
        # B----D
        # pins for motor control
        PIN_A = 17
        PIN_B = 27
        PIN_EN = 22

        BIT_0 = 23
        BIT_1 = 24
        BIT_2 = 25
        servo = {'bottom': 16, 'top': 26}
        pi = pigpio.pi()
        if (joy.connected()):
            print("Xbox controller connected")
        #print("To exit, press BACK button")
        pan = 1800
        tilt = 1600
        sens = 1
        pi.write(PIN_EN, 0)

    def FORWARD(MOTOR):
        pi.write(MOTOR['a'], 1)
        pi.write(MOTOR['b'], 0)

    def REVERSE(MOTOR):
        pi.write(MOTOR['a'], 0)
        pi.write(MOTOR['b'], 1)

    def run(self):
        while 1:
            (left_x, left_y) = joy.leftStick()
            (right_x, right_y) = joy.rightStick()

            if (abs(left_y) > abs(left_x)):
                speed_l = abs(left_y) * (255)
            else:
                speed_l = abs(left_x) * (255)

            speed_b = ('{:08b}'.format(int(speed_l / 32)))

            bit0 = int(speed_b[7])
            bit1 = int(speed_b[6])
            bit2 = int(speed_b[5])

            pi.write(BIT_0, bit0)
            pi.write(BIT_1, bit1)
            pi.write(BIT_2, bit2)

            if (left_y > 0.3):
                pi.write(PIN_A, 0)
                pi.write(PIN_B, 0)
                pi.write(PIN_EN, 1)

            elif (left_y < -0.3):
                pi.write(PIN_A, 1)
                pi.write(PIN_B, 1)
                pi.write(PIN_EN, 1)

            else:
                if (left_x > 0.3):
                    pi.write(PIN_A, 0)
                    pi.write(PIN_B, 1)
                    pi.write(PIN_EN, 1)
                elif (left_x < -0.3):
                    pi.write(PIN_A, 1)
                    pi.write(PIN_B, 0)
                    pi.write(PIN_EN, 1)
                else:
                    pi.write(PIN_EN, 0)

            if (right_x > 0.8):
                pan += sens
            elif (right_x < -0.8):
                pan -= sens

            if (right_y > 0.8):
                tilt -= sens
            elif (right_y < -0.8):
                tilt += sens

            if (pan >= 2300):
                pan = 2300
            elif (pan <= 1300):
                pan = 1300

            if (tilt >= 1900):
                tilt = 1900
            elif (tilt <= 900):
                tilt = 900

            pi.set_servo_pulsewidth(servo['bottom'], pan)
            pi.set_servo_pulsewidth(servo['top'], tilt)
            # print("PUlse: ", servoPulse)

            print("Pan:", pan, "Tilt", tilt, "BIN:", speed_b, "0: ", bit0, "1: ", bit1, "2: ",
                  bit2)  # "L: ", left_x, " | Y:", left_y, " | S:", speed_l)



