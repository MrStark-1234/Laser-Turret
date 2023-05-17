import pigpio
import math
import time


SERVO_PIN_HORIZONTAL = 17  
SERVO_PIN_VERTICAL = 18  


pi = pigpio.pi()


pi.set_mode(SERVO_PIN_HORIZONTAL, pigpio.OUTPUT)
pi.set_mode(SERVO_PIN_VERTICAL, pigpio.OUTPUT)


def move_servo(pin, angle):
    angle = max(0, min(angle, 180))
    duty_cycle = int((angle / 180) * 2000) + 500
    pi.set_servo_pulsewidth(pin, duty_cycle)

# Define a function to calculate servo angles based on Cartesian coordinates
def calculate_angles(x, y):
    radius = math.sqrt(x**2 + y**2)
    horizontal_angle = math.degrees(math.atan2(y, x))
    vertical_angle = math.degrees(math.asin(y / radius))
    # Clamp angles within the valid range
    horizontal_angle = max(-90, min(horizontal_angle, 90))
    vertical_angle = max(0, min(vertical_angle, 180))
    return horizontal_angle, vertical_angle


def point_turret(x, y):
    horizontal_angle, vertical_angle = calculate_angles(x, y)
    move_servo(SERVO_PIN_HORIZONTAL, horizontal_angle)
    move_servo(SERVO_PIN_VERTICAL, vertical_angle)
    time.sleep(1)  # Wait for 1 second


point_turret(100, 50)  # Replace with desired Cartesian coordinates


pi.stop()