'''Usefull Python tricks and code'''

'http://toly.github.io/blog/2014/02/13/parallelism-in-one-line/' - 'Многопоточность в одно строчку (map)'


'http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml'  - прекомпільовані пакети (pip install module_name.whl)


'''Overriding module Classes (vk-requests)'''
class MyAuthAPI(AuthAPI):
    def do_login(self, ...):
        # implement whatever you want

    # other methods overridings


class MyVKSession(VKSession):
    DEFAULT_AUTH_API_CLS = MyAuthAPI

api = vk_requests.create_api(..., session_cls=MyVKSession)


'''My AntiGate Captcha Solver'''
    def get_captcha_key(self, captcha_image_url):
        '''my_fix - for row#175. There didn`t exist that self.get_captcha_key, so i made it.

        my_fix - solve captcha with antigate.com'
        '''
        # test
        # logger.error('=============NEED ENTER CAPTCHA')
        # print('Open CAPTCHA image url: ', captcha_image_url)
        # captcha_key = raw_input('Enter CAPTCHA key: ')
        # return captcha_key
        logger.info('===== CAPTCHA SOLVING WITH ANTIGATE.COM')

        import requests, time, shutil

        antigate_key = '17db2aead1a9f369fc98f51281634245'
        antigate_in = 'http://antigate.com/in.php'
        antigate_res = 'http://antigate.com/res.php'

        try:
            # download captcha to memory
            r = requests.get(captcha_image_url, stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True
                captcha_file = r.raw
            # send and get solved captcha
            try:
                captcha_response = requests.post(antigate_in, data={'key': antigate_key}, files={'file': captcha_file})
                captcha_id = captcha_response.text.split('|')[-1]
            except:
                raise Exception('ERROR CAPTCHA responce. Maybe error key or empty money balance')
            if captcha_response.text.split('|')[0] != 'OK':
                raise Exception('ERROR CAPTCHA response. Maybe bad captcha file')
            while True:
                response = requests.post(antigate_res, data={'key': antigate_key, 'action': 'get', 'id': captcha_id})
                if response.text.split('|')[0] == 'OK':
                    logger.error('===== CAPTCHA SOLVED')
                    return response.text.split('|')[-1]
                else:
                    time.sleep(3)
        except:
            raise
        logger.error('===== CAPTCHA NOT SOLVED')



''' py2exe requests error '''
http://stackoverflow.com/questions/32289972/py2exe-no-such-file-or-directory-error

add 
requets.get(...verify=False)

or (not work last time)

copy cacert.pem (from requetst) to work_dir
add this after imports
from os.path import join, abspath
requests.utils.DEFAULT_CA_BUNDLE_PATH = join(abspath('.'), 'cacert.pem')


''' кеширование дорогой функции '''
http://pythonworld.ru/osnovy/faq.html

В первый раз, когда вы вызываете функцию, mydict содержит одно значение. 
Второй раз, mydict содержит 2 элемента, поскольку, когда foo() начинает
выполняться, mydict уже содержит элемент.

Часто ожидается, что вызов функции создаёт новые объекты для значений по
умолчанию. Но это не так. Значения по умолчанию создаются лишь однажды, 
когда функция определяется. Если этот объект изменяется, как словарь в нашем примере, 
последующие вызовы функции будут использовать изменённый объект.

def expensive(arg1, arg2, _cache={}):
    if (arg1, arg2) in _cache:
        return _cache[(arg1, arg2)]

    # Расчёт значения
    result = ... expensive computation ...
    _cache[(arg1, arg2)] = result     # Кладём результат в кэш
    return result


''' Комент на ютубі, якщо є токен '''
import requests

access_token = 'ya29.pAKjBEf4RyKrUD846zQn5IrQFiovtMC9AdDySWdiDspnvoCFUpoM2I4SqpWCpggS_A'
video_id = 'noLr_BM4toE'
text = 'test'

upload_url = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&access_token='+access_token
data = {
    "snippet": {
  "videoId": video_id,
  "topLevelComment": {
        "snippet":{"textOriginal": text}}
 }
}

r = requests.post(upload_url, json=data, headers={"Content-Type": "application/json"})

print(r, r.text)

''' Отримання access_token and refresh_token '''

1. Get
'''
https://accounts.google.com/o/oauth2/auth?
client_id=711510932378-h8r3uufcgcbp9seinqr57lfnl4mi72cj.apps.googleusercontent.com&
redirect_uri=http%3A%2F%2Flocalhost%2Foauth2callback&
scope=https://www.googleapis.com/auth/youtube.force-ssl&
response_type=token&
access_type=offline
'''
responce:
code like 'LU4oyung7uLb6gS0lbUJcNrcGDyCtPZjf03pOdv08FI'

2. Post
upload_url = "https://accounts.google.com/o/oauth2/token"
data = {
"client_id": "711510932378-h8r3uufcgcbp9seinqr57lfnl4mi72cj.apps.googleusercontent.com",
"client_secret": "-eCcqSxUbOGYwjjPIaZihYD2",
"grant_type": "authorization_code",
"redirect_uri": "http://localhost/oauth2callback",
"code": "4/LU4oyung7uLb6gS0lbUJcNrcGDyCtPZjf03pOdv08FI"
}


r = requests.post(upload_url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}, verify=False)
print(r, r.text)

responce:
<Response [200]> {
  "access_token" : "ya29.pwL6IrZFwLkLrxi1KYXElHPu-h5RtCwozTJWq1q_w0kqrgOmDEKjC7x6fu1hUrsAJg",
  "token_type" : "Bearer",
  "expires_in" : 3600,
  "refresh_token" : "1/CYu8IxLhXTmJ981g6mEmvT3mFgB41_gohVvfL-50bCU"
}


'''Flask server'''
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

app.run()


'''Парсінг сайта по ссилці'''


# pip install requests
# pip install lxml
from lxml import html
import requests

page = requests.get("http://fs.to/video/films/iLb43q3wqMRzJVsHijQAGQ-razborka-v-manile.html")

tree = html.fromstring(page.content)

genre = tree.xpath('//span[@itemprop="genre"]/a[@class="tag"]/span/text()')
actors = tree.xpath('//span[@itemprop="actor"]//span/text()')
print(genre)
print(actors)


''' Pyinstaller '''
pyinstaller.exe --onefile --windowed app.py


''' password hash and salt '''
from werkzeug.security import generate_password_hash, \
     check_password_hash

class User(object):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password, 'sha256', 30)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

me = User('John Doe', 'default')
valid = check_password_hash(me.pw_hash, 'default')
print(valid)

# 1000$TwOCz0RF$156ef82e1a59346e430613dcb96330e73ebe4867