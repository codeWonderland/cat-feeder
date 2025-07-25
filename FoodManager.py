import board
import time

from StorageProtocol import StorageProtocol
from StepperMotor import StepperMotor


sp = StorageProtocol()
sm = StepperMotor(board.GP0, board.GP1, board.GP2)


def dispenceFood(feeding_time):
    current_time = time.localtime()
    formatted_date = "{}/{}\n".format(current_time[1], current_time[2])

    sp.write(
        "last_feeding.txt",
        formatted_date
    )
    sp.write(
        "last_feeding.txt",
        feeding_time,
        "a"
    )

    sm.steps(2)


def getLastFeedingData():
    return sp.read("last_feeding.txt")


def getSchedule():
    return sp.read("feeding_time.txt")


def getNextFeedingTime(feeding_times, last_feed_time):
    last_feeding_index = 0
    for feeding_time in feeding_times:
        if feeding_time == last_feed_time:
            break

        last_feeding_index += 1

    next_feeding_index = (last_feeding_index + 1) % len(feeding_times)

    return feeding_times[next_feeding_index]


def checkFeedTime():
    schedule = getSchedule()
    last_feed_data = getLastFeedingData()
    last_feed_date = last_feed_data[0].split('/')
    last_feed_month = int(last_feed_date[0])
    last_feed_day = int(last_feed_date[1])
    last_feed_time = last_feed_data[1]

    next_feeding_time = getNextFeedingTime(schedule, last_feed_time)

    split_feeding_time = next_feeding_time.split(':')
    feeding_hour = int(split_feeding_time[0])
    feeding_minute = int(split_feeding_time[1])

    current_time = time.localtime()

    last_feed_yesterday = \
        (last_feed_month == 12 and current_time.tm_mon == 1) \
        or last_feed_month < current_time.tm_mon \
        or last_feed_day < current_time.tm_mday

    if feeding_hour <= current_time.tm_hour \
            and feeding_minute <= current_time.tm_min:
        if last_feed_time == schedule[-1]:
            if last_feed_yesterday:
                dispenceFood(next_feeding_time)
        else:
            dispenceFood(next_feeding_time)
