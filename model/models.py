from django.db import models


class Station(models.Model):
    number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True)
    def __unicode__(self):
        return self.name


class EngineType(models.Model):
    number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name


class Engine(models.Model):
    station = models.ForeignKey(Station)
    engine_type = models.ForeignKey(EngineType)
    seq_number = models.CharField(max_length=200)

    def __unicode__(self):
        return self.station.number + '/' + self.engine_type.number + '-' + self.seq_number


class Mission(models.Model):
    statement = models.CharField(max_length=200)
    issue = models.CharField(max_length=200)
    horn = models.BooleanField()
    date = models.DateTimeField()
    number = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    info = models.CharField(max_length=200)
    engines = models.ManyToManyField(Engine)
    def __unicode__(self):
        return self.number + ': ' + self.statement
