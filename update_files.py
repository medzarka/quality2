import subprocess
p = subprocess.Popen("bash update.sh", stdout=subprocess.PIPE, shell=True)
print(p.communicate())