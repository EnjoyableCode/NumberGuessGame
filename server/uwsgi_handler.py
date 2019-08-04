import datetime
from bs4 import BeautifulSoup
import requests
from random import randint
import n2w
import re

from urllib import unquote
import pickle
import os

#put the current directory in the following variable
#ex: curr_dir = '/home/inga/client'
curr_dir = '/home/putcurrentdirectoryhere'

def get_hint_text(divs):
    hint = ''

    if divs:
	randomdiv = divs[randint(0,len(divs) - 1)]

        uls = divs[0].findAll('ul')
        if uls:
            randomul = uls[randint(0,len(uls) - 1)]
            lis = randomul.findChildren('li', recursive=False)
            lis = [x for x in lis if len(x.text) > 40 and '\n' not in x.text]
            if lis:
                randomli = lis[randint(0,len(lis) - 1)]
                hint = randomli.text

    return hint

def get_hint(num):
    url = 'https://en.wikipedia.org/wiki/' + str(num) + '_(number)'

    html = requests.get(url)

    bs = BeautifulSoup(html.text,'html.parser')

    divs = bs.find('div', attrs={'id':'mw-content-text'}).findAll('div')

    hint = ''

    for i in range(100):
        hint = get_hint_text(divs)
        if len(hint) > 40:
            text_num = n2w.convert(num)
            num_rep_list = [text_num,text_num.title(),text_num.upper()]
            num_rep_list_dash = [x.replace(' ','-') for x in num_rep_list]
            num_rep_list_nospace = [x.replace(' ','') for x in num_rep_list]
            num_rep_list = [num] + num_rep_list + num_rep_list_dash + num_rep_list_nospace
            for num_rep in num_rep_list:
                try:
                    hint = hint.replace(num_rep,'????')
                except:
                    hint = ''
            break

    if not hint.strip():
        hint = 'No hint for you'

    return hint


def compare_int(question, target):
    space_split = question.split(' ')
    operator = space_split[0]
    num = int(space_split[1].replace('?',''))

    if operator == '<':

        return target < num

    if operator == '>':

        return target > num

    return 'Bad request'

def even_or_odd(target, parity):
    if parity == 'even':
        return target % 2 == 0

    if parity == 'odd':
        return target % 2 != 0

    return 'Bad request'



def application(environ, start_response):
    body= ''
    try:
        length= int(environ.get('CONTENT_LENGTH', '0'))
    except ValueError:
        length= 0
    if length!=0:
        body = environ['wsgi.input'].read(length)
        command = unquote(body.split('&')[0].split('=')[1]).replace('+',' ')
        uid = body.split('&')[1].split('=')[1]

    curr_files = os.listdir(curr_dir)
    target = ''
    if 'old_ids.p' in curr_files:
        pickled_ids = pickle.load(open(curr_dir + '/old_ids.p'))
        if uid in pickled_ids:
            target = pickled_ids[uid]
        else:
            target = randint(0,100)
            pickled_ids[uid] = target
    else:
        target = randint(0,100)
        new_dict = {uid:target}
        pickle.dump(new_dict,open(curr_dir + '/old_ids.p','wb'))


    guess_query = re.match("\d+\?",command)
    if guess_query:
        if target == int(command.strip()[:-1]):
            target == randind(0,100)
            response = "Correct!  OK, I have a new number now.  Try to get this one..."
        else:
            response = "Sorry! That is not correct."
        start_response('200 OK', [('Content-Type', 'text/html')])
        return response

    parity_query = re.match("(<|>)\s\d+\?",command)

    if parity_query:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return str(compare_int(command,target))

    elif command.strip().lower() == 'hint':
        hint = get_hint(str(target))
        start_response('200 OK', [('Content-Type', 'text/html')])
        return str(get_hint(str(target)))

    elif command.strip().lower().strip() =='even?' or command.lower().strip() == 'odd?':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return str(even_or_odd(target,command.lower().strip()[:-1]))

    elif command.strip().lower() == 'quit':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return "Thank you for playing!"

    else:
        start_response('200 OK', [('Content-Type', 'text/html')])
        return "Command not understood.  Try: hint, even, odd, < N?, > N?, or N?"


