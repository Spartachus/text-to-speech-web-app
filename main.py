import requests
import json
import time


text = """
What do you call a fish that wears a bowtie?

Sofishticated.

ha ha ha ha ha ha ha ha ha
"""
bit = text.split()[0]
url = "https://large-text-to-speech.p.rapidapi.com/tts"
payload = {"text": text}

headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "large-text-to-speech.p.rapidapi.com",
    'x-rapidapi-key': "32b2d164famsh0308ce55d35d211p1094a0jsn3848efb22a9c"
    }


response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
print(response.text)


id = json.loads(response.text)['id']
eta = json.loads(response.text)['eta']

print(f'Waiting {eta} seconds for the job to finish...')
time.sleep(eta)

response = requests.request("GET", url, headers=headers, params={'id': id})

while "url" not in json.loads(response.text):
    response = requests.get(url, headers=headers, params={'id': id})
    time.sleep(5)

if not "error" in json.loads(response.text):
    result_url = json.loads(response.text)['url']

    response = requests.get(result_url)

    with open(f'static/{bit}.wav', 'wb') as f:
        f.write(response.content)
    print(f"File {bit}.wav saved!")
else:
    print(json.loads(response.text)['error'])