# from django_cron import CronJobBase, Schedule
# from .models import *


# class MyCronJob(CronJobBase):
#     schedule = Schedule(run_every_mins=5)  # Specify the time you want to run the task
#     code = 'myapp.my_cron_task'  # Unique identifier for the cron job

#     def do(self):
#         if HoldModel.objects.filter(ledger=None).exists():
#             raise Exception("Some holdings didnot have ledgers")
