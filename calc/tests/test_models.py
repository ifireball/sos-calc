import pytest
from datetime import date
from typing import Tuple, Any

from django.db.models.query import QuerySet
from django.conf import settings
from django.contrib.auth.models import User

from calc.models import Account, Day, Speedups


def test_debug():
    assert settings.DEBUG


@pytest.mark.django_db
class TestSpeedups:
    FIELDS = (
        'day',
        "training_1m",
        "training_5m",
        "training_1h",
        "healing_1m",
        "healing_5m",
        "healing_1h",
        "construction_1m",
        "construction_5m",
        "construction_1h",
        "research_1m",
        "research_5m",
        "research_1h",
        "generic_1m",
        "generic_5m",
        "generic_1h",
        "generic_3h",
        "generic_8h",
    )
    TEST_DATA = [
        (date(2021, 1, 6), 1500, 700, 10, 150, 2000, 12, 100, 500, 5, 30, 1200, 12, 2100, 1200, 30, 2, 1),
        (date(2021, 1, 8), 900, 400, 4, 160, 2200, 14, 80, 250, 3, 40, 1300, 10, 1100, 800, 20, 0, 2),
    ]

    @pytest.fixture
    def user(self) -> User:
        return User.objects.get_by_natural_key('user2')

    @pytest.fixture
    def populated_account(self, user) -> Account:
        return Account.objects.get(user=user, name='Foo')

    def test_test_data(self, populated_account):
        res: QuerySet = Speedups.objects.filter(account=populated_account).order_by('day')
        assert list(res.values_list(*self.FIELDS)) == self.TEST_DATA

    @classmethod
    def vectorize(cls, speedups: Speedups) -> Tuple[Any, ...]:
        return tuple(getattr(speedups, fn) for fn in cls.FIELDS)

    @pytest.mark.parametrize('test_row', TEST_DATA)
    def test_vetorize(self, test_row):
        speedups = Speedups(**dict(zip(self.FIELDS, test_row)))
        assert self.vectorize(speedups) == test_row

    def test_defaults(self):
        day = date(2020, 1, 1)
        speedups = Speedups(day=day)
        assert self.vectorize(speedups) == tuple([day] + [0]*(len(self.FIELDS) - 1))

    @pytest.mark.parametrize('test_row', TEST_DATA)
    def test_get_speedups_for_existing_day(self, test_row, populated_account):
        speedup = Speedups.get_speedups_for_day(populated_account, Day(test_row[0]))
        assert self.vectorize(speedup) == test_row

    def test_get_speedups_for_missing_day_with_previous(self, populated_account):
        day = Day(date(2021, 1, 7))
        speedups = Speedups.get_speedups_for_day(populated_account, day)
        assert self.vectorize(speedups) == (day.date,) + self.TEST_DATA[0][1:]
        speedups.training_1m = 1300
        speedups.training_5m = 750
        speedups.save()
        expected = self.TEST_DATA.copy()
        expected.insert(1, (day.date, 1300, 750, 10, 150, 2000, 12, 100, 500, 5, 30, 1200, 12, 2100, 1200, 30, 2, 1))
        res: QuerySet = Speedups.objects.filter(account=populated_account).order_by('day')
        assert list(res.values_list(*self.FIELDS)) == expected

    def test_get_speedups_for_missing_day_with_no_previous(self, populated_account):
        day = Day(date(2021, 1, 5))
        speedups = Speedups.get_speedups_for_day(populated_account, day)
        assert self.vectorize(speedups) == tuple([day.date] + ([0] * (len(self.FIELDS) - 1)))
        speedups.training_1m = 1300
        speedups.training_5m = 750
        speedups.save()
        expected = self.TEST_DATA.copy()
        expected.insert(0, (day.date, 1300, 750, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        res: QuerySet = Speedups.objects.filter(account=populated_account).order_by('day')
        assert list(res.values_list(*self.FIELDS)) == expected
