from __future__ import annotations

from datetime import datetime, date, timezone, timedelta

from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    state = models.IntegerField()
    name = models.CharField(max_length=64)
    alliance = models.CharField(max_length=64, blank=True)

    @classmethod
    def default_for_user(cls, user):
        return cls.objects.filter(user=user).first()

    def __str__(self):
        if self.alliance:
            return f"[{self.alliance}] {self.name} (#{self.state:03})"
        else:
            return f"{self.name} (#{self.state:03})"


class Day:
    def __init__(self, the_date: date):
        self.date: date = the_date

    @staticmethod
    def today_date() -> date:
        return datetime.now(timezone.utc).date()

    @classmethod
    def today(cls) -> Day:
        return cls(cls.today_date())

    @classmethod
    def fromisoformat(cls, value) -> Day:
        return cls(date.fromisoformat(value))

    def isoformat(self) -> str:
        return self.date.isoformat()

    def is_today(self) -> bool:
        return self.date == self.today_date()

    def __add__(self, other: int) -> Day:
        return Day(self.date + timedelta(days=other))

    def __sub__(self, other: int) -> Day:
        return self.__add__(-other)

    @property
    def previous(self) -> Day:
        return self - 1

    @property
    def next(self) -> Day:
        return self + 1

    def __str__(self):
        return self.date.strftime('%A, %B %d, %Y')
