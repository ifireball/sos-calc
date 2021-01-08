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


class Speedups(models.Model):
    account = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    day = models.DateField()
    training_1m = models.IntegerField(default=0)
    training_5m = models.IntegerField(default=0)
    training_1h = models.IntegerField(default=0)
    healing_1m = models.IntegerField(default=0)
    healing_5m = models.IntegerField(default=0)
    healing_1h = models.IntegerField(default=0)
    construction_1m = models.IntegerField(default=0)
    construction_5m = models.IntegerField(default=0)
    construction_1h = models.IntegerField(default=0)
    research_1m = models.IntegerField(default=0)
    research_5m = models.IntegerField(default=0)
    research_1h = models.IntegerField(default=0)
    generic_1m = models.IntegerField(default=0)
    generic_5m = models.IntegerField(default=0)
    generic_1h = models.IntegerField(default=0)
    generic_3h = models.IntegerField(default=0)
    generic_8h = models.IntegerField(default=0)

    class Meta:
        unique_together = ['account', 'day']

    @staticmethod
    def minutes_sum(v1m=0, v5m=0, v1h=0, v3h=0, v8h=0) -> int:
        return v1m + 5 * v5m + 60 * (v1h + 3 * v3h + 8 * v8h)

    @property
    def training_minutes(self) -> int:
        return self.minutes_sum(self.training_1m, self.training_5m, self.training_1h)

    @property
    def healing_minutes(self) -> int:
        return self.minutes_sum(self.healing_1m, self.healing_5m, self.healing_1h)

    @property
    def construction_minutes(self) -> int:
        return self.minutes_sum(self.construction_1m, self.construction_5m, self.construction_1h)

    @property
    def research_minutes(self) -> int:
        return self.minutes_sum(self.research_1m, self.research_5m, self.research_1h)

    @property
    def generic_minutes(self) -> int:
        return self.minutes_sum(
            self.generic_1m,
            self.generic_5m,
            self.generic_1h,
            self.generic_3h,
            self.generic_8h
        )

    @property
    def training_available(self) -> int:
        return self.training_minutes + self.generic_minutes

    @property
    def healing_available(self) -> int:
        return self.healing_minutes + self.generic_minutes

    @property
    def construction_available(self) -> int:
        return self.construction_minutes + self.generic_minutes

    @property
    def research_available(self) -> int:
        return self.research_minutes + self.generic_minutes

    @classmethod
    def get_speedups_for_day(cls, account: Account, day: Day) -> Speedups:
        speedups: Speedups
        try:
            speedups = cls.objects.get(account=account, day=day.date)
            return speedups
        except cls.DoesNotExist:
            speedups = cls.objects.filter(account=account, day__lte=day.date).order_by('-day').first()
            if speedups:
                if speedups.day != day.date:
                    speedups.day = day.date
                    speedups.id = None
                    speedups._state.adding = True
                    speedups._state.db = None
                return speedups
            else:
                speedups = Speedups()
                speedups.account = account
                speedups.day = day.date
                return speedups

    def __str__(self):
        return f"Speedups for '{self.account}' @ {self.day.isoformat()}"