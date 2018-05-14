from urllib.request import urlopen

# Basic GET request and response examination
response = urlopen('http://packtpub.com')
print(response.getheader('Content-Type'))
print(response.getheader('Server'))
print(response.status)
print(response.reason)

html = response.read()
print(html[:15])
print(html.decode('utf-8')[:15])

# Basic POST request with data
response = urlopen('http://duckduckgo.com', data=b'q=tkinter')

from urllib.parse import urlencode
data = {'q': 'tkinter, python', 'ko': '-2', 'kz': '-1'}
print(urlencode(data))

response = urlopen('http://duckduckgo.com', data=urlencode(data).encode())
