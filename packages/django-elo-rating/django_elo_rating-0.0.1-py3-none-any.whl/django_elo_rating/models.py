import math

from django.db import models
from django.conf import settings


class EloRated(models.Model):
    elo_rating = models.FloatField(default=settings.ELO_START_VALUE)

    class Meta:
        abstract = True

    def probability(self, opponent):
        return 1 / (1 + math.pow(10, (opponent.elo_rating - self.elo_rating) / 400))

    def updated_elo(self, opponent, result):
        return self.elo_rating + settings.ELO_FACTOR_K * (result - self.probability(opponent))