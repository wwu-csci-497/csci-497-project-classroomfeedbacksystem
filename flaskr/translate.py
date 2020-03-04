from flask import Flask, request

# would not run, error said that module 'requests' did not exist
#import requests

app = Flask(__name__)

DETECT_BASE_URL = 'https://google-translate1.p.rapidapi.com/language/translate/v2/detect'
TRANSLATE_BASE_URL = 'https://google-translate1.p.rapidapi.com/language/translate/v2'
HEADERS = {
    'x-rapidapi-host': "google-translate1.p.rapidapi.com",
    'x-rapidapi-key': "911c2daf0cmsh9f9965c6c11a7b3p1f68e2jsn22e8c6586122",
    'content-type': "application/x-www-form-urlencoded"
}

@app.route('/')
def health_check():
   return 'Translation Service is up.'


@app.route('/detect', methods=['POST'])
def detect():
    # parse args
    text = request.form.get('text')

    # url encode text
    long_list_of_words = text.split(' ')
    url_encoded_text = f"q={'%20'.join(long_list_of_words)}"

    payload = url_encoded_text

    # make the request
    r = requests.post(DETECT_BASE_URL, data=payload, headers=HEADERS)

    return r.json()


@app.route('/translate', methods=['POST'])
def translate():
    # parse args
    text = request.form.get('text')
    target = request.form.get('target')

    # url encode text
    long_list_of_words = text.split(' ')
    url_encoded_text = f"q={'%20'.join(long_list_of_words)}&target={target}"

    payload = url_encoded_text

    r = requests.post(TRANSLATE_BASE_URL, data=payload, headers=HEADERS)

    return r.json()

if __name__ == '__main__':
    app.run(debug=True)