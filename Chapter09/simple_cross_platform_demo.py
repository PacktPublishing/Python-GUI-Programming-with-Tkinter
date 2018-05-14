import platform
import subprocess

os_name = platform.system()
if os_name in ('Darwin', 'freebsd7'):
    cmd = ['ps', '-e', '-o', "comm=''", '-c']
elif os_name == 'Linux':
    cmd = [
        'ps', '-e', '--format',
        'comm', '--no-heading'
    ]
elif os_name == 'Windows':
    cmd = ['tasklist', '/nh', '/fo', 'CSV']
else:
    raise NotImplemented("Command unknown for OS")

processes = subprocess.check_output(cmd)
print(processes)
