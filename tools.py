import sys
import os
import subprocess

from datetime import datetime as date

##### Configurations
python_path = '/home/ubuntu/.virtualenvs/quality2/bin/python3'
django_service = 'gunicorn'
backup_prefix = 'django_quality2'
backup_database_path = '/home/ubuntu/backups/database'
backup_files_path = '/home/ubuntu/backups/files'
backup_include = '/home/ubuntu/quality2  /home/ubuntu/data'


def execCommand(cmd, print_trace=True):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    if print_trace:
        print(p.communicate())


def database():
    os.makedirs(backup_database_path, exist_ok=True)
    current_datetime = date.now()
    str_current_datetime = str(current_datetime)
    file_name = os.path.join(backup_database_path, str_current_datetime + ".json")
    execCommand(f'{python_path} manage.py dumpdata --exclude auth.permission --exclude contenttypes > {file_name}')
    print('to load the data, type following command:')
    print(f'{python_path} manage.py loaddata {file_name}')


def backup():
    os.makedirs(backup_files_path, exist_ok=True)
    archive_file = f'{backup_prefix}__backup__{date.today().strftime("%A")}.tgz'
    print(f'Backing up backup files to {archive_file}')
    execCommand(f'tar czf {os.path.join(backup_files_path, archive_file)} {backup_include}')
    print("Backup finished")


def help():
    print("----------------------------------------------------------------")
    print("Help for the tools python program:")
    print("\t-stop : to stop the django application")
    print("\t-start : to start the application")
    print("\t-restart : to restart the application")
    print("\t-requirements : to install the python package requirements")
    print("\t-pull : to download latest update from github")
    print("\t-backup : to create a file backup")
    print("\t-database : to create a database backup")
    print("")
    print("\t-help : to print this help messages")
    print("")


# ./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        help()
    elif len(args) == 1:
        if args[0] == 'stop':
            execCommand("sudo systemctl stop " + django_service)
        elif args[0] == 'start':
            execCommand("sudo systemctl start " + django_service)
        elif args[0] == 'restart':
            execCommand("sudo systemctl restart " + django_service)
        elif args[0] == 'requirements':
            execCommand("pip install -r requirements.txt")
        elif args[0] == 'pull':
            execCommand("git pull")
        elif args[0] == 'backup':
            backup()
        elif args[0] == 'database':
            database()
        elif args[0] == 'help':
            help()
        else:
            print("Action non recognized")
            help()
    else:
        print("Error in using the tool parameters.")
        help()


if __name__ == "__main__":
    main()
