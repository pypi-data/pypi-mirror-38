import requests


class String_Filter(object):
    def __init__(self, list, text_list, filter, entity, auth):
        self.pr_list = list
        self.text_list = text_list
        self.filter = filter
        self.entity = entity
        self.auth = auth
        self.response_list = []

    def filter_by_string(self):
        for pr in self.pr_list:
            if (self.entity == 'commits'):
                commits = requests.get(
                    pr['commits_url'], auth=self.auth
                ).json()
                for com in commits:
                    self.filter_check(
                        self.text_list, com["commit"]["message"].split(),
                        pr
                    )
            else:
                files = requests.get(
                    pr['url']+'/files', auth=self.auth
                ).json()
                filename_list = [f["filename"] for f in files]
                print(filename_list)
                self.filter_check(self.text_list, filename_list, pr)

        return [i for n, i in enumerate(self.response_list)
                if i not in self.response_list[n+1:]
                ]

    def filter_check(self, string_list, split_string, pr):
        if (self.filter == 'any'):
            if any(x in split_string for x in string_list):
                self.response_list.append({pr['title']: pr['url']})
        elif(self.filter == 'all'):
            if all(x in split_string for x in string_list):
                self.response_list.append({pr['title']: pr['url']})
