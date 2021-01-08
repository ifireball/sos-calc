from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0004_speedups'),
    ]

    def generate_data(apps, schema_editor):
        from django.conf import settings

        if not settings.DEBUG:
            return

        from datetime import date
        from django.contrib.auth.models import User
        from calc.models import Account, Speedups

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
        TEST_DATA = (
            (date(2021, 1, 6), 1500, 700, 10, 150, 2000, 12, 100, 500, 5, 30, 1200, 12, 2100, 1200, 30, 2, 1),
            (date(2021, 1, 8),  900, 400,  4, 160, 2200, 14,  80, 250, 3, 40, 1300, 10, 1100,  800, 20, 0, 2),
        )

        user2 = User.objects.get_by_natural_key('user2')
        foo = Account.objects.get(user=user2, name='Foo')

        with transaction.atomic():
            for row in TEST_DATA:
                Speedups(account=foo, **dict(zip(FIELDS, row))).save()


    operations = [
        migrations.RunPython(generate_data),
    ]