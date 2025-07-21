import board
import time

from StorageProtocol import StorageProtocol
from StepperMotor import StepperMotor



sp = StorageProtocol()
sm = StepperMotor(board.GP0, board.GP1, board.GP2)


def dispenceFood():
    current_time = time.localtime()
    formatted_time = "{}/{}".format(current_time[1], current_time[2])

    sp.write(
        "last_feed_date.txt", 
        formatted_time
    )

    sm.steps(2)


def checkFeedTime():
    current_time = time.localtime()

    last_feed_date = sp.read("last_feed_date.txt")[0].split('/')
    last_feed_month = int(last_feed_date[0])
    last_feed_day = int(last_feed_date[1])
    
    feeding_time = sp.read("feeding_time.txt")[0].split(':')
    feeding_hour = int(feeding_time[0])
    feeding_minute = int(feeding_time[1])

    # ((a and b) or c or (d and e)) and f and g
    if ((last_feed_month == 12 and current_time[1]) == 1 \
        or last_feed_month < current_time[1] \
        or last_feed_day < current_time[2]) \
        and feeding_hour <= current_time[3] \
        and feeding_minute <= current_time[4]:
        
        dispenceFood()
