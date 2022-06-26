from django.conf import settings
f = open('passenger_wsgi.py', 'w', encoding='UTF8')
f.write('from quality2.wsgi import application')
f.write('from whitenoise import WhiteNoise')
f.write(f'application = WhiteNoise(application, root="{settings.STATIC_ROOT}")')
f.write(f'application.add_files("{settings.MEDIA_ROOT}", prefix="media/")')
f.close()
