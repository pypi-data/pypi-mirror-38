import requests


class Filter(object):
    def __init__(self, list, num, filter, entity, auth):
        self.list = list
        self.range = num
        self.filter = filter
        self.entity = entity
        self.response_list = []
        self.auth = auth

    def filter_by_number(self):
        for pr in self.list:
            if(self.entity == 'commits'):
                length = len(requests.get(
                    pr['commits_url'], auth=self.auth
                ).json())
            else:
                length = len(requests.get(
                    pr["url"]+'/files', auth=self.auth
                ).json())
            self.equality_check(length, pr)
        return self.response_list

    def equality_check(self, length, pr):
        if (self.filter == 'eq'):
            if(length == self.range):
                self.response_list.append({pr['title']: pr['url']})
        elif(self.filter == 'lt'):
            if(length < self.range):
                self.response_list.append({pr['title']: pr['url']})
        elif(self.filter == 'gt'):
            if(length > self.range):
                self.response_list.append({pr['title']: pr['url']})
