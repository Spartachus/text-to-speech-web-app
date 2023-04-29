from flask import Flask,render_template,request,url_for
import requests
from dotenv import load_dotenv
import os
import requests
import json
import time

def configure():
  load_dotenv()

app = Flask(__name__)
 
@app.route('/', methods=['POST','GET'])  
def lecto():   
    configure()
    if request.method == 'POST':  
      api = os.getenv("API_KEY")
      try:
        text =  request.form.get('transcript')
        ap_name = text.split()[0]
        url = "https://large-text-to-speech.p.rapidapi.com/tts"
        payload = {"text": text}
        headers = {
            'content-type': "application/json",
            'x-rapidapi-host': "large-text-to-speech.p.rapidapi.com",
            'x-rapidapi-key': api
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

            with open(f'static/{ap_name}.wav', 'wb') as f:
                f.write(response.content)
            print(f"File {ap_name}.wav saved!")
            audio_name =  url_for('static', filename=f'{ap_name}.wav')
            return render_template("succes.html", audio_name = audio_name)


        else:
            print(json.loads(response.text)['error'])
            return render_template("fail.html") 
      except:
          return render_template("fail.html")

    return render_template('home.html')  

if __name__ == '__main__':
    app.run(debug=True)
