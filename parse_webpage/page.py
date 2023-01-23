import requests

url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_' \
      '%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8 '

# response = requests.get(url, headers={'one': 'true'})
# print(response.request.headers)

headers = {
    'Accept': '*/*',
    'User-Agent': 'python-requests/2.27.1'
}

req = requests.get(url, headers=headers)
src = req.text

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(src)
