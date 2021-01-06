from django.db import migrations, transaction


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from django.conf import settings

        if not settings.DEBUG:
            return

        from django.contrib.auth.models import User
        from calc.models import Account

        with transaction.atomic():
            User.objects.create_user('user1')
            user2 = User.objects.create_user('user2')

            Account(user=user2, name='Foo', state=123, alliance='ALL').save()
            Account(user=user2, name='Bar', state=123, alliance='ALL').save()

    operations = [
        migrations.RunPython(generate_data),
    ]