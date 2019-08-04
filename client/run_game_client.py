import requests
import uuid

#put URL of server below (example: url = http://1.2.3.4:8080)
url = 'putserverhere'

user_input = ''
if __name__ == '__main__':
    print('Welcome to a brand new game!')
    uid = uuid.uuid4()
    while user_input.strip().lower() != 'quit':
        print('Please enter your next command, or "quit" to end...')
        user_input = raw_input()
        data = {'uid':uid,'command':str(user_input).strip()}
        r = requests.post(url=url,data=data)
        print(r.text)
