import requests, time, shutil

def get_captcha_key(ANTIGATE_KEY, captcha_image_url):
	''' Solve captcha using antigate.com  '''
	
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
            captcha_response = requests.post(antigate_in, data={'key': ANTIGATE_KEY}, files={'file': captcha_file})
            captcha_id = captcha_response.text.split('|')[-1]
        except:
            raise Exception('ERROR CAPTCHA responce. Maybe error key or empty money balance')
        while captcha_response.text == 'ERROR_NO_SLOT_AVAILABLE':
            time.sleep(5)
            # send and get solved captcha
            try:
                captcha_response = requests.post(antigate_in, data={'key': ANTIGATE_KEY}, files={'file': captcha_file})
                captcha_id = captcha_response.text.split('|')[-1]
            except:
                raise Exception('ERROR CAPTCHA responce. Maybe error key or empty money balance')
        if captcha_response.text.split('|')[0] != 'OK':
            raise Exception('Error captcha solving: '+captcha_response.text)
        while True:
            response = requests.post(antigate_res, data={'key': ANTIGATE_KEY, 'action': 'get', 'id': captcha_id})
            if response.text.split('|')[0] == 'OK':
                return response.text.split('|')[-1]
            else:
                time.sleep(3)
    except:
        raise

''' Usage '''
if __name__ == '__main__':
	captcha_url = 'http://vk.com/captcha.php?sid=772649661360'
	antigate_key = '17db2aead1a9f369fc98f51281634245'
	captcha = get_captcha_key(antigate_key, captcha_url)
	print('Solved captcha:', captcha)
