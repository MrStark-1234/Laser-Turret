import pigpio
import math
import time
import smbus
 

SERVO_PIN_HORIZONTAL1 = 17  
SERVO_PIN_HORIZONTAL2 = 19
SERVO_PIN_VERTICAL = 18  



pi = pigpio.pi()

pi.set_mode(SERVO_PIN_HORIZONTAL1, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_HORIZONTAL2, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_VERTICAL, pigpio.OUTPUT)


PWR_M   = 0x6B
DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_EN   = 0x38
GYRO_X  = 0x43
GYRO_Y  = 0x45
GYRO_Z  = 0x47
TEMP = 0x41
bus = smbus.SMBus(1)


Device_Address = 0x68 
GxCal=0
GyCal=0


def InitMPU():
     bus.write_byte_data(Device_Address, DIV, 7)
     bus.write_byte_data(Device_Address, PWR_M, 1)
     bus.write_byte_data(Device_Address, CONFIG, 0)
     bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
     bus.write_byte_data(Device_Address, INT_EN, 1)
     time.sleep(1)

def readMPU(addr):
     high = bus.read_byte_data(Device_Address, addr)
     low = bus.read_byte_data(Device_Address, addr+1)
     value = ((high << 8) | low)
     if(value > 32768):
           value = value - 65536
     return value

def move_servo(pin, angle):
    angle = max(0, min(angle, 180))
    duty_cycle = int((angle / 180) * 2000) + 500
    pi.set_servo_pulsewidth(pin, duty_cycle)



def gyro(x,y):
    global GxCal
    global GyCal
   
    x = readMPU(GYRO_X)
    y = readMPU(GYRO_Y)
    Gx = x/131.0 - GxCal
    Gy = y/131.0 - GyCal
    
      
    time.sleep(.01)  

# Define a function to calculate servo angles based on Cartesian coordinates
def calculate_angles(Gx, Gy):
    radius = math.sqrt(Gx**2 + Gy**2)
    horizontal_angle = math.degrees(math.atan2(Gy, Gx))
    vertical_angle = math.degrees(math.asin(Gy / radius))
    # Clamp angles within the valid range
    horizontal_angle = max(-90, min(horizontal_angle, 90))
    vertical_angle = max(0, min(vertical_angle, 180))
    return horizontal_angle, vertical_angle


def point_turret(Gx, Gy):
    horizontal_angle, vertical_angle = calculate_angles(Gx, Gy)
    if(horizontal_angle>180):
        horizontal_angle2=horizontal_angle-180
        move_servo(SERVO_PIN_HORIZONTAL1, horizontal_angle)
        move_servo(SERVO_PIN_HORIZONTAL2, horizontal_angle2)
    else:
         move_servo(SERVO_PIN_HORIZONTAL1, horizontal_angle)
        
    move_servo(SERVO_PIN_VERTICAL, vertical_angle)
    time.sleep(1)  # Wait for 1 second


   
point_turret(Gx, Gy)  # Replace with desired Cartesian coordinates

pi.stop() 