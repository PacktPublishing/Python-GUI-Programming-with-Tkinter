import requests

# Make a simple GET request

response = requests.request('GET', 'http://www.alandmoore.com/')
print(response)

response = requests.get('http://www.alandmoore.com')
print(response)

# Make a POST with data
response = requests.post(
    'http://duckduckgo.com',
    data={'q': 'tkinter', 'ko': '-2', 'kz': '-1'})

print(response)


# Sessions

s = requests.session()

# Assume this is a valid authentication service that returns an auth token
s.post('http://example.com/login', data={'u': 'test', 'p': 'test'})
# Now we would have an auth token
response = s.get(
    'http://example.com/protected_content'
)
# Our token cookie would be listed here
print(s.cookies.items())


# Response objects

r = requests.get('http://www.alandmoore.com')
print(r.headers)

r = requests.get('http://www.example.com/does-not-exist')
r.status_code

r.raise_for_status()
