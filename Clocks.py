import NIFTYLivePrices
import NIFTYAverageUpdater
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
    print("Live")
    NIFTYLivePrices.StartUpdating()

@sched.scheduled_job('cron', hour=13, minute=00, timezone='UTC')
def scheduled_job():
    print("Average Prices Updated")
    NIFTYAverageUpdater.UpdateAveragePrices()

sched.start()