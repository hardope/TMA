import requests
import json

url = 'http://localhost:8000/api/books/'
file = {'file': open('test.pdf', 'rb')}

data = {
    'title': 'Test',
    'author': 'Test',
    'description': 'Test',
    'price': 100
}

response = requests.post(url, data=data, files=file)

print(response.json())