from django.db import models
from datetime import timezone

class Log(models.Model):
    time = models.CharField(max_length=255)
    log = models.TextField()

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'model_log'  
        # verbose_name = "model_log"

# -------------------------------------------------------
class Log_crud:
    def __init__(self):
        print("Log_crud")
    
    def create(self, time, log):
        # print("create")
        b = Log(time=time, log=log)
        b.save()

    def read(self):
        # print("read")
        all_entries = Log.objects.all()
        times = all_entries.values_list('time', flat=True)
        logs = all_entries.values_list('log', flat=True)

        all_records = []
        for record in tuple(zip(times, logs)):
            all_records =  [record[0][5:] + ":    " + record[1]] + all_records
        return all_records

    def delete(self):
        # print("delete")
        end = Log.objects.values_list('id', flat=True).last()
        start = end - 50
        Log.objects.filter(id__lte = start) .delete()

