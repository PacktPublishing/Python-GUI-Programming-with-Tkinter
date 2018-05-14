import platform
from backend import get_backend

os_name = platform.system()
os_backend = get_backend(os_name)()

print(os_backend.get_process_list())
