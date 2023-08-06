from django.db import models


class ConsignmentNote(models.Model):
    doc_nomber = models.CharField(max_length=30)
    doc_date = models.DateTimeField()
    clien_name = models.CharField(max_length=124)
    purchase = models.JSONField()
    total_amount = models.FloatField()
    shipping_warehouse = models.CharField(max_length=30)
