import subprocess


def get_backend(os_name):
    backends = {
        'Linux': LinuxBackend,
        'Darwin': MacBsdBackend,
        'Windows': WindowsBackend,
        'freebsd7': MacBsdBackend
    }
    try:
        return backends[os_name]
    except KeyError:
        raise NotImplemented("No backend for OS")


class GenericBackend:

    cmd = []

    def get_process_list(self):
        if self.cmd:
            return subprocess.check_output(self.cmd)
        else:
            raise NotImplemented


class LinuxBackend(GenericBackend):
    cmd = ['ps', '-e', '--format', 'comm', '--no-heading']


class MacBsdBackend(GenericBackend):
    cmd = ['ps', '-e', '-o', "comm=''", '-c']


class WindowsBackend(GenericBackend):
    cmd = ['tasklist', '/nh', '/fo', 'CSV']
