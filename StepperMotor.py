from LatchingRelay import LatchingRelay
import digitalio
from time import sleep

class StepperMotor:
    def __init__(self, motor_on, motor_off, stepper, full_rotation = 5):
        # motor setup
        self.motor = LatchingRelay(motor_on, motor_off)

        # stepper setup
        self.stepper = digitalio.DigitalInOut(stepper)
        self.stepper.direction = digitalio.Direction.INPUT
        self.stepper.pull = digitalio.Pull.UP

        self.full_rotation = full_rotation
        
    
    def steps(self, total_steps):
        num_steps = 0
        btn_pressed = False

        self.motor.relay_on()

        while num_steps < total_steps:
            # stepper is depressed
            if not self.stepper.value:
                # we record this in our flag variable
                btn_pressed = True

            # if the stepper *was* depressed
            elif btn_pressed:
                # we count it and reset our flag
                num_steps += 1
                btn_pressed = False

            sleep(0.01)

        self.motor.relay_off()

    
    def rotations(self, total_rotations):
        self.steps(total_rotations * self.full_rotation)
