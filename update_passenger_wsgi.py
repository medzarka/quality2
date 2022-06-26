import os
import sys
import environ

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if 'env_file' in os.environ.keys():
    env_file = os.path.join(BASE_DIR, 'env', os.getenv('env_file'))
    print(f'Configuration Site in file {env_file}.')
else:
    env_file = 'env'
    env_file = os.path.join(BASE_DIR, 'env', 'env')
    print(f'Configuration Site in file {env_file}.')

if env_file is None:
    print(f'The env filename "env_file" is not set !')
    sys.exit(-1)

if not os.path.exists(os.path.join(BASE_DIR, env_file)):
    print(f'The env filename {env_file} does not exist!')
    sys.exit(-1)

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, env_file))

f = open('passenger_wsgi.py', 'w', encoding='UTF8')
f.write('from quality2.wsgi import application\n')
f.write('from whitenoise import WhiteNoise\n')

SITE_DATA_DIR = os.path.join(os.environ['HOME'], env('SITE_DATA_PATH'))
SITE_FILES_DIR = os.path.join(os.environ['HOME'], env('SITE_FILES_PATH'))

f.write(f'application = WhiteNoise(application, root="{os.path.join(os.path.join(SITE_FILES_DIR, "static"))}")\n')
f.write(f'application.add_files("{os.path.join(os.path.join(SITE_FILES_DIR, "media"))}", prefix="media/")\n')
f.close()
