import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

def find_type(something):
    """
    This function returns object if it isn't a dictionary or list.
    If it is dictionary or list get inner object until it isn't
    a dictionary or list.
    """
    if (type(something) == str or
        type(something) == bool or
        something == None):
        return something
    elif type(something) == dict:
        while True:
            print('Object is a dictionary.')
            ans = input('Do you want to see keys? [y/n] ')
            if ans == 'y':
                for key in something.keys():
                    print(key)
                while True:
                    key = input('Enter a key: ')
                    if key not in something.keys():
                        continue
                    else:
                        return find_type(something[key])
            elif ans == 'n':
                return 'REFUSE'
            else:
                continue
    elif type(something) == list:
        while True:
            print(f'Object is a list of length {len(something)} elements.')
            if len(something) == 0:
                print('There is nothing inside this object.')
                return 'REFUSE'
            ans = input('Do you want to see all elements? [y/n] ')
            if ans == 'y':
                for el in something:
                    print(el)
                while True:
                    ans2 = input('Do you want to see a particular element? [y/n] ')
                    if ans2 == 'y':
                        while True:
                            try:
                                index = int(input(f'Enter a number of element from 1 to {len(something)}: '))
                                if 1 > index > len(something):
                                    continue
                                else:
                                    return find_type(something[index-1])
                            except ValueError:
                                continue
                            except IndexError:
                                continue
                    elif ans2 == 'n':
                        return 'REFUSE'
                    else:
                        continue
            elif ans == 'n':
                return 'REFUSE'
            else:
                continue


TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

options_str = '''1. name info
2. profile description
3. follow info
4. number of posts
5. location
6. url
7. photos
8. show all keys
9. exit'''

while True:
    print('')
    acct = input('Enter Twitter Account: ')
    if (len(acct) < 1):
        break
    try:
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '100'})
        print('Retrieving', url)
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()
    except urllib.error.HTTPError:
        print('There is no user with such name.')
        while True:
            answer = input('Do you want to try another user? [y/n]: ')
            if answer == 'y':
                break
            elif answer == 'n':
                exit()
            else:
                continue
        continue

    js = json.loads(data)
    with open('twit.json', 'w', encoding='utf-8') as f:
        json.dump(js, f, indent=4, ensure_ascii=False)

    with open('twit.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if len(data['users']) == 0:
        print('This user has no friends.')
        continue
    while True:
        print("Do you want to know general info about user's friends or show all keys?")
        ans = input('[general info/show all keys]')
        if ans == 'general info':
            while True:
                try:
                    us = int(input('Enter number from 1 to 100 to choose user: \n'))
                    if 1 > us > 100:
                        continue
                    else:
                        break
                except ValueError:
                    continue
            #print(data['users'][us-1])
            while True:
                print('What do you want to know about user?')
                print(options_str)
                option = input('Choose category, enter a number: ')
                if option == '1':
                    while True:
                        print('id | name | screen_name')
                        while True:
                            key = input('Choose a key: ')
                            if key not in data['users'][us-1].keys():
                                continue
                            else:
                                break
                        print(f"user {key}: {data['users'][us-1][key]}")
                        ans = input('Do you want to try another [key/category/stop]? ')
                        if ans == 'key':
                            continue
                        elif ans == 'category':
                            break
                        elif ans == 'stop':
                            exit()
                        else:
                            continue
                elif option == '2':
                    while True:
                        print('profile description:', data['users'][us-1]['description'])
                        ans = input('Do you want to try another [category/stop]? ')
                        if ans == 'category':
                            break
                        elif ans == 'stop':
                            exit()
                        else:
                            continue
                elif option == '3':
                    while True:
                        print('followers_count | friends_count | favourites_count')
                        while True:
                            key = input('Choose a key: ')
                            if key not in data['users'][us-1].keys():
                                continue
                            else:
                                break
                        print(f"user {key}: {data['users'][us - 1][key]}")
                        ans = input('Do you want to try another [key/category/stop]? ')
                    if ans == 'key':
                        continue
                    elif ans == 'category':
                        break
                    elif ans == 'stop':
                        exit()
                    else:
                        continue
                elif option == '4':
                    while True:
                        print('number of posts:', data['users'][us - 1]['statuses_count'])
                        ans = input('Do you want to try another [category/stop]? ')
                    if ans == 'category':
                        break
                    elif ans == 'stop':
                        exit()
                    else:
                        continue
                elif option == '5':
                    print('location:', data['users'][us - 1]['location'])
                    while True:
                        ans = input('Do you want to try another [category/stop]? ')
                        if ans == 'category':
                            break
                        elif ans == 'stop':
                            exit()
                        else:
                            continue
                elif option == '6':
                    print('profile URL:', data['users'][us - 1]['url'])
                    while True:
                        ans = input('Do you want to try another [category/stop]? ')
                        if ans == 'category':
                            break
                        elif ans == 'stop':
                            exit()
                        else:
                            continue
                elif option == '7':
                    print('profile_image_url | profile_banner_url')
                    while True:
                        key = input('Choose a key: ')
                        if key not in data['users'][us-1].keys():
                            continue
                        else:
                            break
                    print(f"user {key}: {data['users'][us - 1][key]}")
                    while True:
                        ans = input('Do you want to try another [key/category/stop]? ')
                        if ans == 'key':
                            continue
                        elif ans == 'category':
                            break
                        elif ans == 'stop':
                            exit()
                        else:
                            continue
                elif option == '8':
                    while True:
                        for key in data['users'][us - 1].keys():
                            print(key)
                        while True:
                            key = input('Choose a key: ')
                            if key not in data['users'][us-1].keys():
                                continue
                            else:
                                break
                        result = find_type(data['users'][us-1][key])
                        if result != 'REFUSE':
                            print(f'user {key}: {result}')
                        ans = input('Do you want to try another [key/category/stop]? ')
                        if ans == 'key':
                            continue
                        elif ans == 'category':
                            break
                        elif ans == 'stop':
                            exit()
                        else:
                            continue
                elif option == '9':
                    exit()
                else:
                    continue
        elif ans == 'show all keys':
            while True:
                for key in data.keys():
                    print(key)
                key = input('Enter a key: ')
                if key not in data.keys():
                    continue
                result = find_type(data[key])
                if result != 'REFUSE':
                    print(f'{key}: {result}')
                ans = input('Do you want to try another [key/stop]? ')
                if ans == 'key':
                    continue
                elif ans == 'stop':
                    exit()
                else:
                    continue
        else:
            continue
