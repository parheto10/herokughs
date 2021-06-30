# Generated by Django 3.1.3 on 2020-11-19 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parametres', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=250, unique=True, verbose_name='MATRICULE')),
                ('genre', models.CharField(choices=[('H', 'HOMMME'), ('F', 'FEMME')], default='H', max_length=10, verbose_name='GENRE')),
                ('grade', models.CharField(choices=[('DR.', 'DOCTEUR'), ('MED.', 'MEDECIN'), ('INF.', 'INFIRMIER(E)'), ('AIDE', 'AIDE SOIGNANT(E)'), ('SECRETAIRE', 'SECRETAIRE')], max_length=50)),
                ('telephone1', models.CharField(max_length=50, verbose_name='TELEPHONE 1')),
                ('telephone2', models.CharField(blank=True, max_length=50, verbose_name='TELEPHONE 2')),
                ('adresse', models.CharField(blank=True, max_length=255, verbose_name='ADRESSE')),
                ('bio', models.TextField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='upload_image_avatar')),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('hopital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.hopital')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.service')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'personnel',
                'verbose_name_plural': 'PERSONNELS',
                'ordering': ('-add_le', '-update_le'),
            },
        ),
    ]
