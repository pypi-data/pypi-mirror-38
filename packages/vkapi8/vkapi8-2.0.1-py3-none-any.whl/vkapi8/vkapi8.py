import time
import random
import re
import itertools
import xml.etree.ElementTree as ET
import datetime

import requests
from requests.exceptions import RequestException

from .accesstoken import *


EXCEPTIONS_MAP = dict(enumerate(['Wrong password/login',
                                 '401 Unauthorized',
                                 'Internet issues',
                                 'Blocked'], 1))


class VKApiException(Exception):
    pass


class NetworkException(Exception):
    def __init__(self, error):
        VKApiException.__init__(self, str(error))


class AuthException(VKApiException):
    def __init__(self, login, passw, client, scope, error_code):
        error = '''AuthException: {},
               Arguments: login "{}", pass "{}",
               client "{}",
               scope"{}"'''.format(EXCEPTIONS_MAP[error_code], login, passw, client, scope)
        VKApiException.__init__(self, error)


class MethodException(VKApiException):
    def __init__(self, error):
        VKApiException.__init__(self, str(error))


class VKApi():

    def __init__(self, login, password, client, scope='',
                 version='5.69', session=requests.Session(),
                 debug=False):
        try:
            self.token = get_token(login, password, client,
                                   'offline' + (',' if scope != '' else '') + scope)[0]
        except RuntimeError:
            raise AuthException(login, password, client, scope, 1)
        except urllib.error.HTTPError:
            raise AuthException(login, password, client, scope, 2)
        except urllib.error.URLError:
            raise AuthException(login, password, client, scope, 3)
        except ValueError:
            raise AuthException(login, password, client, scope, 4)
        self.version = version
        self.session = session
        self.debug = debug

    
    def send_fake_request(self):
        _fake_requests_methods = {
            'database.getCities':'country_id',
            'database.getChairs':'faculty_id',
            'groups.getById':'group_id'
        }
        rand = random.randint(0, len(_fake_requests_methods)-1)
        method = list(_fake_requests_methods.keys())[rand]
        self.api_request(method, {_fake_requests_methods[method]:str(random.randint(1, 100))})

    
    def get_region(self, query, city_id):
        json_response = self.api_request('database.getCities', {'country_id':1, 'q':query})
        if json_response.get('error'):
            raise Exception("Error while getting region, error_code=".format(
                str(json_response['error']['error_code'])))
        if not json_response['response']['items']:
            return None
        for item in json_response["response"]["items"]:
            if 'region' in item:
                if item["id"] == city_id:
                    return item["region"]
        return json_response['response']['items'][0]["title"]


    def _get_group_25k_members(self, group_id, fields="", offset=0):
        code = '''var group = "{}";
        var i = 0;
        var count = 25000;
        var ret = {{}};
        var data = {{}};
        while (i < 25 && i*1000 < count)
        {{
            data = API.groups.getMembers({{"group_id":group, "count":1000,
             "offset":i*1000 + {}, "fields":"{}"}});
            count = data["count"];
            ret.push(data["items"]);
            i=i+1;
        }}
        return {{"count":count, "items":ret}};'''.format(group_id, offset, fields)
        resp = self.execute(code)
        if 'error' in resp:
            raise Exception('Error while getting group_members, error: ' + str(resp['error']))
        membs = []
        for array in resp['response']["items"]:
            membs.extend(array)
        return {"count":resp['response']['count'], "items":membs}


    def get_all_group_members(self, group_id, fields=""):
        group_id = self.group_url_to_id(group_id)
        members = self._get_group_25k_members(group_id, fields)
        if members['count'] > 25000:
            for i in range(members['count']//25000 - int(members['count']%25000 == 0)):
                members['items'].extend(self._get_group_25k_members(
                    group_id, fields, (i+1)*25000)['items'])
        return members


    def _get_25_groups_members(self, group_ids, fields=""):
        code = '''var groups = {};
        var i = 0;
        var ret = {{}};
        while (i < 25 && i < groups.length)
        {{
            ret.push({{"id":groups[i], "response":API.groups.getMembers(
            {{["group_id":groups[i], "count":1000, "fields":"{}"}})}});
            i=i+1;
        }}
        return ret;'''.format(str(group_ids).replace('\'', '"'), fields)
        resp = self.execute(code)
        if 'error' in resp:
            raise Exception('Error while getting groups_members, error: ' + str(resp['error']))
        groups_data = {}
        for element in resp['response']:
            groups_data[element['id']] = element['response']
        for group_id, group_data in groups_data.items():
            if group_data['count'] > 25000:
                groups_data[group_id] = self.get_all_group_members(group_id, fields)
        return groups_data


    def get_groups_members(self, group_ids, fields=""):
        group_ids = [self.group_url_to_id(group) for group in group_ids]
        members = self._get_25_groups_members(group_ids[:25], fields)
        if len(group_ids) > 25:
            for i in range(len(group_ids)//25 - int(len(group_ids)%25 == 0)):
                members.update(self._get_25_groups_members(group_ids[(i+1)*25:(i+2)*25], fields))
        return members


    def validate_users(self, user_ids, days_to_del=0, fields='', filter_func=None):
        fields+=',last_seen'
        ret_ids = []
        excluded_ids = {"banned": list(), "abandoned": list(), "excluded": list()}
        new_users = self.get_users_data(user_ids, fields)
        for user in new_users:
            if 'deactivated' in user:
                excluded_ids['banned'].append(user)
                continue
            if 'last_seen' in user:
                days_since_last_seen = (int(time.time())-user['last_seen']['time'])//86400
                if days_to_del and days_since_last_seen>=days_to_del:
                    excluded_ids['abandoned'].append(user)
                    continue
            if filter_func and not filter_func(user):
                excluded_ids['excluded'].append(user)
            ret_ids.append(user['id'])
        return {'clean': ret_ids, 'filtered': excluded_ids}


    def get_users_data(self, user_ids, fields='', data_format='csv', _opti=250):
        if data_format != "csv" and data_format != "xml":
            raise Exception('Error while getting users data, wrong format given: {}'.format(data_format))
        url_xml = '''https://api.vk.com/method/users.get.xml?
                             user_ids={}&fields={}&access_token={}&v={}'''
        url = 'https://api.vk.com/method/users.get?user_ids={}&fields={}&access_token={}&v={}'
        iterations = (len(user_ids) // _opti) + (1 if(len(user_ids)%_opti) else 0)
        if data_format == 'xml':
            user_data = "<?xml version='1.0' encoding='utf8'?>\n<users>\n"
        else:
            user_data = []
        for i in range(iterations):
            try:
                if (len(user_ids) - _opti*i) < _opti:
                    ids = user_ids[_opti*i:]
                else:
                    ids = user_ids[_opti*i:(_opti*(i+1))]
            except:
                break
            if data_format == "xml":
                response = self.session.get(url_xml.format(str(ids), fields,
                                                           self.token, self.version)).text
                root = ET.fromstring(response)
                if root[0].tag == 'error_code':
                    raise Exception('''Error while getting users data,
                     error_code={}'''.format(str(root[0].text)))
                for child in root:
                    user_data += ET.tostring(child, encoding='utf8', method='xml').decode('utf-8').replace("<?xml version='1.0' encoding='utf8'?>", "")
            else:
                ids_str = str(ids).replace('[', '').replace(']', '').replace('\'', '').replace(' ','')
                response = self.session.get(url.format(str(ids_str), fields,
                                                       self.token, self.version)).json()
                if 'error' in response:
                    raise Exception('''Error while getting users data,
                     error_code=''' + str(response['error']['error_code']))
                user_data.extend(response['response'])
            time.sleep(0.34)
        return user_data


    def get_users_sequence_generator(self, from_id, to_id, fields="", opti=300):
        iterations = (to_id-from_id) // opti + 1
        for i in range(iterations):
            if i%15 + 1 == 0:
                self.send_fake_request()
                time.sleep(1)
            ids = list(range(i*opti+from_id, (i+1)*opti+from_id))
            if to_id - (i*opti+from_id) < opti:
                ids = ids[:to_id - (i*opti + from_id)]
            response = self.api_request('users.get', {
                'user_ids': str(ids).replace("[", "").replace("]", ""),
                'fields': fields})
            if 'error' in response:
                raise MethodException('''Error while getting users information,
                 error: {}''' + str(response['error']['error_code']))
            yield response['response']


    def get_users_data_generator(self, ids, fields=""):
        _opti = 300
        iterations = len(ids) // _opti + 1
        for i in range(iterations):
            if i%15 == 14:
                self.send_fake_request()
                time.sleep(1)
            ids_to_load = ids[i*_opti:(i+1)*_opti]
            response = self.api_request('users.get', {
                'user_ids':str(ids_to_load).replace("[", "")\
                                           .replace("]", "")\
                                           .replace("'", "")\
                                           .replace(" ", ""),
                'fields':fields})
            if 'error' in response:
                raise MethodException('''Error while getting users information,
                 error: {}''' + str(response['error']['error_code']))
            yield response['response']


    def _get_user_groups_by_offset(self, user_id, offset=0):
        json_response = self.api_request('groups.get',
                                         {'user_id':user_id, 'offset':offset, 'count':1000})
        if 'error' in json_response:
            raise Exception('''Error while getting group members,
             error=''' + str(json_response['error']))
        return json_response['response']


    def get_user_groups(self, user_id):
        user_id = self.user_url_to_id(user_id)
        groups = self._get_user_groups_by_offset(user_id)
        if groups['count'] > 1000:
            iterations = int(groups['count']/1000) - int(groups['count']%1000 == 0)
            for i in range(iterations):
                groups['items'].extend(self._get_user_groups_by_offset(user_id, 1000*i)['items'])
        return groups


    def execute(self, code):
        return self.api_request('execute', {'code':code})


    def api_request(self, method, data):
        data['access_token'] = self.token
        data['v'] = self.version
        try:
            resp = self.session.post('https://api.vk.com/method/{}'.format(method), data=data)
        except RequestException as e:
            if self.debug: print(e)
            raise NetworkException(str(e))
        time.sleep(0.34)
        if resp.status_code != 200:
            raise NetworkException('''Network error while executing {} method,
             error code: {}'''.format(method, str(resp.status_code)))
        return resp.json()


    def _get_25_users_subscriptions(self, ids):
        code = '''var ids = ''' + str(ids).replace('\'', '"') +  ''';
        var i = 0;
        var ret = {};
        while (i < 25 && i < ids.length)
        {
            ret.push({"id":ids[i], "response":API.users.getSubscriptions({"user_id":ids[i], 
            "extended":0, "count":200})});
            i=i+1;
        }
        return ret;'''
        resp = self.execute(code)
        if 'error' in resp:
            raise MethodException('''Error while getting 25_users_groups,
             error: ''' + str(resp['error']))
        users_data = {}
        for element in resp['response']:
            if not element['response'] or not element['response']:
                users_data[element['id']] = None
                continue
            users_data[element['id']] = element['response']
        return users_data


    def _get_25_users_groups(self, ids):
        code = '''var ids = ''' + str(ids).replace('\'', '"') +  ''';
        var i = 0;
        var ret = {};
        while (i < 25 && i < ids.length)
        {
            ret.push({"id":ids[i], "response":API.groups.get({"user_id":ids[i], 
            "extended":1, "count":500})});
            i=i+1;
        }
        return ret;'''
        resp = self.execute(code)
        if 'error' in resp:
            raise MethodException('''Error while getting 25_users_groups,
             error: ''' + str(resp['error']))
        users_data = {}
        for element in resp['response']:
            if not element['response'] or not element['response']:
                users_data[element['id']] = None
                continue
            user_groups = []
            for group in element['response']['items']:
                if group['type'] == 'group':
                    user_groups.append(group['id'])
            users_data[element['id']] = {'count':len(user_groups), 'items':user_groups}
        return users_data


    def _get_25_users_friends(self, ids):
        code = '''var ids = ''' + str(ids).replace('\'', '"') +  ''';
        var i = 0;
        var ret = {};
        while (i < 25 && i < ids.length)
        {
            ret.push({"id":ids[i], "response":API.friends.get({"user_id":ids[i], 
            "count":1000})});
            i=i+1;
        }
        return ret;'''
        resp = self.execute(code)
        if 'error' in resp:
            raise MethodException('''Error while getting 25_users_friends,
             error: ''' + str(resp['error']))
        users_data = {}
        for element in resp['response']:
            if not element['response'] or not element['response']:
                users_data[element['id']] = None
                continue
            if element['response']['count'] > 1000:
                users_data[element['id']] = self.get_friends_ids(element['id'])
            else:
                users_data[element['id']] = element['response']
        return users_data


    def _get_25_users_subs(self, ids):
        code = '''var ids = ''' + str(ids).replace('\'', '"') +  ''';
        var i = 0;
        var ret = {};
        while (i < 25 && i < ids.length)
        {
            ret.push({"id":ids[i], 
            "response":API.users.getFollowers({"user_id":ids[i], "count":1000})});
            i=i+1;
        }
        return ret;'''
        resp = self.execute(code)
        if 'error' in resp:
            raise MethodException('''Error while getting 25_users_subs,
             error: ''' + str(resp['error']))
        users_data = {}
        for element in resp['response']:
            if not element['response']:
                users_data[element['id']] = None
                continue
            if element['response']['count'] > 1000:
                users_data[element['id']] = self.load_all_subs(element['id'])
            else:
                users_data[element['id']] = element['response']
        return users_data


    def _get_25_users_videos(self, ids):
        code = '''var ids = ''' + str(ids).replace('\'', '"') +  ''';
        var i = 0;
        var ret = {};
        while (i < 25 && i < ids.length)
        {
            ret.push({"id":ids[i], 
            "response":API.video.get({"owner_id":ids[i], "count":200})});
            i=i+1;
        }
        return ret;'''
        resp = self.execute(code)
        if 'error' in resp:
            raise MethodException('''Error while getting 25_users_videos,
             error: ''' + str(resp['error']))
        users_data = {}
        for element in resp['response']:
            if not element['response']:
                users_data[element['id']] = None
                continue
            if element['response']['count'] > 200:
                users_data[element['id']] = self.load_5k_videos(element['id'])
            else:
                users_data[element['id']] = element['response']
        return users_data


    def get_users_extended_info(self, ids, infos, retries=8):
        methods = {
            "friends": self._get_25_users_friends,
            "subs": self._get_25_users_subs,
            "publics": self._get_25_users_subscriptions,
            "groups": self._get_25_users_groups,
            "videos": self._get_25_users_videos
        }
        methods_to_apply = [(method_name, method)\
                            for method_name, method in methods.items()\
                            if method_name in infos]
        i = iter(ids)
        ids_to_aggregate = list(itertools.islice(i, 0, 25))
        while ids_to_aggregate:
            yield_data = {}
            for method_name, method in methods_to_apply:
                new_data = None
                tries_count = 0
                while not new_data:
                    try:
                        new_data = method(ids_to_aggregate)
                    except MethodException as method_exc:
                        if self.debug: print(method_exc)
                        if tries_count > retries:
                            if self.debug: print('exiting')
                            raise method_exc
                        tries_count += 1
                        time.sleep(10)
                    except NetworkException as net_exc:
                        if self.debug: print(net_exc)
                        if tries_count > retries:
                            if self.debug: print('exiting')
                            raise net_exc
                        tries_count += 1
                        time.sleep(10)
                for user, data in new_data.items():
                    yield_data[user] = {method_data[0]: None for method_data in methods_to_apply}
                    yield_data[user][method_name] = data
            ids_to_aggregate = list(itertools.islice(i, 0, 25))
            yield yield_data


    def _get_posts_by_offset(self, wall_id, offset, count, domain):
        request_data = {'offset':offset, 'count':count}
        if domain:
            request_data['domain'] = wall_id
        else:
            request_data['owner_id'] = wall_id
        resp = self.api_request('wall.get', request_data)
        if 'error' in resp:
            raise MethodException('''Error while getting wall posts,
             error=''' + str(resp['error']))
        return resp['response']


    def get_posts(self, wall_id, domain=False, number_of_posts=100):
        text = {"author_text": list(),
                "copy_text": list(),
                "posts_count": 0,
                "reposts_count": 0}
        posts_count = 0
        offset = 0
        posts = {'count': 100}
        while posts_count < number_of_posts and posts_count < posts['count']:
            posts = self._get_posts_by_offset(wall_id, offset, 100, domain)
            offset += 100
            for item in posts['items']:
                if item["text"]:
                    text["author_text"].append(item["text"])
                    text['posts_count'] += 1
                if "copy_history" in item:
                    text["reposts_count"] += 1
                    if item["copy_history"][0]["text"]:
                        text["copy_text"].append(item["copy_history"][0]["text"])
                posts_count += 1
        return text


    def get_groups_by_id_generator(self, ids, fields=''):
        iter_size = 500
        for i, groups_chunk in enumerate(ids[pos:pos + iter_size]\
                                         for pos in range(0, len(ids), iter_size)):
            if not i % 5:
                self.send_fake_request()
            retries = 5
            resp = None
            while not resp or 'error' in resp:
                retries -= 1
                if not retries:
                    raise MethodException('Error while getting groups by id')
                resp = self.api_request('groups.getById',
                                        {'group_ids': ','.join(str(grp) for grp in groups_chunk),
                                         'fields': fields})
                if 'error' in resp:
                    time.sleep(3)
            yield resp['response']


    def group_url_to_id(self, group_url):
        group_url = str(group_url)
        parts = group_url.split("/")
        if len(parts) != 1:
            group_url = parts[-1:][0]
        group_id = group_url.strip()
        if re.match(r'(club|public)\d', group_id) != None:
            group_id = re.search(r'\d.*', group_id).group(0)
        return group_id


    def user_url_to_id(self, user_url):
        user_url = str(user_url)
        parts = user_url.split('/')
        if len(parts) != 1:
            user_url = parts[-1:]
        user_id = user_url.strip()
        if re.match(r'id\d*', user_id) != None:
            user_id = re.search(r'\d.*', user_id).group(0)
        return user_id

    
    def get_user_id(self, link):
        domain = link.split("/")[-1]
        resp = self.api_request('users.get', {'user_ids':domain})
        if resp.get('error'):
            raise Exception('''Error while getting user_id,
             error: {}'''.format(str(resp['error'])))
        return resp['response'][0]['id']

    
    def _load_25k_subs(self, user_id, offset=0):
        code = '''var user = ''' + str(user_id) + ''';
        var i = 0;
        var ret = [];
        var count = 25000;
        var data = {};
        while (i*1000 < count &&  i<25)
        {
            data = API.users.getFollowers({"user_id":user,
            "count":1000, "offset":i*1000 + ''' + str(offset) + '''});
            count = data["count"];
            ret.push(data["items"]);
            i=i+1;
        }
        return {"count":count, "items":ret};'''
        resp = self.execute(code)
        if resp['response']['count'] is None:
            return {'count':None, 'items':None}
        if 'error' in resp:
            raise Exception('''Error while getting 25k subs,
             error: ''' + str(resp['error']))
        subs = []
        for array in resp['response']['items']:
            subs.extend(array)
        if 'execute_errors' in resp:
            pass
        return {'count':resp['response']['count'], 'items':subs}

    
    def load_all_subs(self, user_id):
        user_id = self.user_url_to_id(user_id)
        subs = self._load_25k_subs(user_id)
        count = subs['count']
        if count is None:
            return None
        for i in range(count//25000 - int(count%25000 == 0)):
            subs['items'].extend(self._load_25k_subs(user_id, i*25000))
        return subs


    def load_5k_videos(self, user_id):
        code = '''var user = ''' + str(user_id) + ''';
        var i = 0;
        var ret = [];
        var count = 5000;
        var data = {};
        while (i*200 < count &&  i<25)
        {
            data = API.videos.get({"user_id":user, 
            "count":200, "offset":i*200});
            count = data["count"];
            ret.push(data["items"]);
            i=i+1;
        }
        return {"count":count, "items":ret};'''
        resp = self.execute(code)
        if resp['response']['count'] is None:
            return {'count':None, 'items':None}
        if 'error' in resp:
            raise Exception('''Error while getting 5k subs,
             error: ''' + str(resp['error']))
        subs = []
        for array in resp['response']['items']:
            subs.extend(array)
        if 'execute_errors' in resp:
            pass
        return {'count':resp['response']['count'], 'items':subs}


    def get_friends_ids(self, user_id, count=25000):
        user_id = self.user_url_to_id(user_id)
        code = '''var user = ''' + str(user_id) + ''';
        var i = 0;
        var ret = [];
        var count = ''' + str(count) + ''';
        var data = {};
        while (i*1000 < count)
        {
            data = API.friends.get({"user_id":user, "count":1000, "offset":i*1000});
            count = data["count"];
            ret.push(data["items"]);
            i=i+1;
        }
        return {"count":count, "items":ret};'''
        resp = self.execute(code)
        if 'error' in resp:
            raise Exception('''Error while getting all friends,
             error: ''' + str(resp['error']))
        if resp['response']['count'] is None:
            return None
        friends = []
        for array in resp['response']['items']:
            friends.extend(array)
        if 'execute_errors' in resp:
            pass
        return {"count": resp['response']['count'], "items":friends}


    def _get_10k_messages(self, peer_id, date=time.strftime("%d%m%Y"), _offset=0):
        messages = {}
        filtered = 0
        for i in range(4):
            code = '''var peer_id = ''' + str(peer_id) + ''';
            var i = 0;
            var ret = [];
            var count = 10000;
            var data = [];
            var date = ''' + date + ''';
            while (i*100 + {offset} < count && i<25)
            {{
                data = API.messages.search({{"peer_id":peer_id, 
                "date":date, "count":100, "offset":i*100 + {offset}}});
                count = data["count"];
                ret.push(data["items"]);
                if(data["items"].length == 0){{
                    return {{"count":count, "items":ret}};
                }}
                i=i+1;
            }}
            return {{"count":count, "items":ret}};'''.format(offset=i*2500+_offset)
            resp = self.execute(code)
            if 'error' in resp:
                raise Exception('''Error while getting all friends,
                 error: ''' + str(resp['error']))
            for arrray in resp['response']['items']:
                for message in arrray:
                    if 'body' in message and message['body'] != '':
                        messages[message['id']] = {'body':message['body'],
                                                   'date':message['date'],
                                                   'user_id':message['user_id']}
                    else:
                        filtered += 1
            if not resp['response']['items'] or not resp['response']['items'][0]:
                break
            self.send_fake_request()
        return {"count": resp['response']['count'], "filtered":filtered, "items":messages}


    def get_dialog_messages(self, peer_id, count=100, date=time.strftime("%d%m%Y")):
        resp = self.api_request('messages.search', {'peer_id':peer_id, 'date':date, 'count':count})
        if 'error' in resp:
            raise Exception('''Error while getting dialog messages,
             error: {}'''.format(str(resp['error'])))
        return resp['response']


    def get_all_messages_generator(self, peer_id, opti=7500, limit=7500):
        count = 10000
        j = 0
        date = time.strftime("%d%m%Y")
        while j < count and j*opti < limit:
            i = 0
            messages = {}
            while len(messages) < opti and i < count and i < opti:
                new_messages = self._get_10k_messages(peer_id, date, i)
                if not new_messages['items']:
                    j = count
                    break
                count = new_messages['count']
                i += len(new_messages['items']) + new_messages['filtered']
                messages.update(new_messages['items'])
            if not messages:
                yield {}
                break
            time.sleep(1)
            self.send_fake_request()
            date = datetime.datetime.fromtimestamp(messages[min(list(messages.keys()))]['date']).strftime('%d%m%Y')
            j += i
            yield messages


    def search_dialogs(self, unread=False, offset=0):
        resp = self.api_request('messages.getDialogs',
                                {'offset':offset,
                                 'unread':int(unread),
                                 'count':200})
        if 'error' in resp:
            raise Exception('''Error while getting dialogs,
             error: {}'''.format(str(resp['error'])))
        return resp['response']


    def accept_friend_request(self, id):
        resp = self.api_request('friends.add', {'user_id':id}).json()
        if 'error' in resp:
            raise Exception('''Error while checking for new requests,
             error: {}'''.format(str(resp['error'])))
        return resp


    def check_for_new_friend_requests(self):
        resp = self.api_request('friends.getRequests', {'count':1000}).json()
        if 'error' in resp:
            raise Exception('''Error while checking for new requests,
             error: {}'''.format(str(resp['error'])))
        return resp['response']['items']


    def accept_all_friend_requests(self):
        for request in self.check_for_new_friend_requests():
            self.accept_friend_request('id')


    def get_unread_messages(self):
        unread_dialogs = self.search_dialogs(unread=True)['items']
        unread_messages = {}
        for dialog in unread_dialogs:
            msg = dialog['message']
            peer_id = (msg['chat_id']+2000000000) if('chat_id' in msg) else msg['user_id']
            unread = self.get_dialog_messages(peer_id, dialog['unread'])
            unread_messages[peer_id] = unread['items']
        return unread_messages


    def send_message(self, peer_id, message):
        resp = self.api_request('messages.send', {'peer_id':peer_id, 'message':message})
        if 'error' in resp:
            raise Exception('''Error while checking for new requests,
             error: {}'''.format(str(resp['error'])))
        return resp


    def join_public(self, group_id):
        resp = self.api_request('groups.join', {'group_id':group_id})
        if 'error' in resp:
            raise Exception('''Error while joining group,
             error: {}'''.format(str(resp['error'])))
        return resp


    #post_id = string 'wall134643_101' or 'wall-1_123453456'
    def repost_post(self, post_id, message=''):
        resp = self.api_request('wall.repost', {'object':post_id, 'message':message})
        if 'error' in resp:
            raise Exception('''Error while reposting,
             error: {}'''.format(str(resp['error'])))
        return resp
