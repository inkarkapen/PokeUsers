from __future__ import unicode_literals
from ..logReg_app.models import User
from django.db import models

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="pokerpokes")
    poked = models.ForeignKey(User, related_name="pokedpokes")
    created_at = models.DateField(auto_now_add=True)
    counter = models.IntegerField(blank=False, default=0, null=True)
    total = models.IntegerField(blank=False, default=0, null=True)