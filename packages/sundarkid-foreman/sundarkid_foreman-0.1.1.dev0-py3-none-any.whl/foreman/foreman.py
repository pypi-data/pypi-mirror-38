import requests
import sys
import json
from pprint import pprint
from copy import deepcopy, copy
import syslog

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)


class Foreman:

    def __init__(self, user, passwrod, fman_server):
        self.user = user
        self.password = passwrod
        self.url_base = fman_server
        pass

    # HTTP functional wrappers
    def https_get(self, url, user, password):
        '''
        Function to wrap around the HTTP GET request

        :param url: str
        :param user: str
        :param password: str
        :return: dict
        '''
        status = 0
        print(url)
        try:
            r = requests.get(url, auth=(user, password), verify=False)
            status = r.status_code
            return {
                'status_code': r.status_code,
                'headers': r.headers,
                'text': r.text,
                'data': r.json()
            }
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0], str(e))
            return {
                'status_code': status,
                'headers': {},
                'text': '',
                'data': {}
            }

    def https_post(self, url, user, password, payload, header={}):
        '''
        Function to wrap around the HTTP POST request

        :param url: str
        :param user: str
        :param password: str
        :param payload: dict
        :param header: dict
        :return: dict
        '''
        status = 0
        try:
            r = requests.post(url, auth=(user, password), verify=False,
                              data=json.dumps(payload), headers=header)
            status = r.status_code
            return {
                'status_code': r.status_code,
                'headers': r.headers,
                'text': r.text,
                'data': r.json()
            }
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0], str(e))
            return {
                'status_code': status,
                'headers': {},
                'text': '',
                'data': {}
            }

    def https_put(self, url, user, password, payload, header={}):
        '''
        Function to wrap around the HTTP PUT request

        :param url: str
        :param user: str
        :param password: str
        :param payload: dict
        :param header: dict
        :return: dict
        '''
        status = 0
        try:
            r = requests.put(url, auth=(user, password), verify=False,
                             data=json.dumps(payload), headers=header)
            status = r.status_code
            return {
                'status_code': r.status_code,
                'headers': r.headers,
                'text': r.text,
                'data': r.json()
            }
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0], str(e))
            return {
                'status_code': status,
                'headers': {},
                'text': '',
                'data': {}
            }

    def https_delete(self, url, user, password, payload, header={}):
        '''
        Function to wrap around the HTTP POST request

        :param url: str
        :param user: str
        :param password: str
        :param payload: dict
        :param header: dict
        :return: dict
        '''
        status = 0
        try:
            r = requests.delete(url, auth=(
                user, password), verify=False, data=json.dumps(payload), headers=header)
            status = r.status_code
            return {
                'status_code': r.status_code,
                'headers': r.headers,
                'text': r.text,
                'data': r.json()
            }
        except Exception as e:
            print("Unexpected error:", sys.exc_info()[0], str(e))
            return {
                'status_code': status,
                'headers': {},
                'text': '',
            }

   # HostGroup level functionality
    def get_all_hostgroup(self):
        '''
        Function to get all hostgroups accessible by this user

        :return: list
        '''
        self.url_get_hostgroup = self.url_base + "/api/hostgroups"
        page = 1
        hostgroups = []
        total = 0
        while True:
            url = self.url_get_hostgroup + "?per_page=100&page=" + str(page)
            result = self.https_get(
                url=url, user=self.user, password=self.password)
            if result['status_code'] == 200:
                if 'subtotal' in result['data']:
                    total = result['data']['subtotal']
                    if 'results' in result['data']:
                        for i in result['data']['results']:
                            hostgroups.append(i)
                    if len(hostgroups) >= total:
                        break
                page += 1
            else:
                raise Exception(result)
        return hostgroups

    def get_hostgroup(self, id):
        '''
        Function to get a hostgroup accessible by this user by ID
        :param id: str/int
        :return: dict
        '''
        self.url_get_hostgroup = self.url_base + "/api/hostgroups/"
        url = self.url_get_hostgroup + str(id)
        result = self.https_get(url=url, user=self.user,
                                password=self.password)
        if result['status_code'] == 200:
            return result
        else:
            raise Exception(result)

    def add_new_hostgroup(self, host_group):
        '''
        Function to add a new hostgroup to an Environment

        :param host_group: dict  (Example = {
                 "hostgroup": {
                     "name": "TestHostgroupGrandParent",
                     "environment_id": 79,
                 }
             })
        :return: dict
        '''
        self.url_create_hostgroup = self.url_base + "/api/hostgroups"
        header = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        result = self.https_post(url=self.url_create_hostgroup, user=self.user, password=self.password,
                                 payload=host_group,
                                 header=header)
        if result['status_code'] == 201:
            return result
        else:
            raise Exception(result)

    def remove_hostgroup(self, id):
        '''
        Function to remove a hostgroup accessible by this user by ID

        :param id: int/str (Host Group ID)
        :return: dict
        '''
        self.url_delete_hostgroup = self.url_base + \
            "/api/hostgroups/" + str(id) if type(id) == int else id
        header = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        result = self.https_delete(url=self.url_delete_hostgroup, user=self.user, password=self.password, payload={},
                                   header=header)
        if result['status_code'] == 200:
            return result
        else:
            raise Exception(result)

    def modify_hostgroup(self, id, details):
        '''
        Function to modify the HostGroup details

        :param id: int/str (Host Group ID)
        :param details: Dict (Host Group Specs)
        :return: dict
        '''
        self.url_modify_host_group = self.url_base + \
            "/api/hostgroups/" + str(id) if type(id) == int else id
        header = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        result = self.https_put(url=self.url_modify_host_group, user=self.user, password=self.password,
                                payload=details,
                                header=header)
        if result['status_code'] == 200:
            return result
        else:
            raise Exception(result)

    # Organization Level functionality

    def add_new_organization(self, organization):
        '''
        Function to add a new hostgroup to an Environment

        :param organization: dict  (Example = {
                 "organization": {
                     "name": "TestOrg",
                     "parent_id": 3,
                 }
             })
        :return: dict
        '''
        self.url_create_organization = self.url_base + "/api/organization"
        header = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        result = self.https_post(url=self.url_create_organization, user=self.user, password=self.password,
                                 payload=organization,
                                 header=header)
        if result['status_code'] == 201:
            return result
        else:
            raise Exception(result)

    def modify_organization(self, id, details):
        '''
        Function to modify the HostGroup details

        :param id: int/str (Host Group ID)
        :param details: Dict (Host Group Specs)
        :return: dict
        '''
        self.url_modify_organization = self.url_base + \
            "/api/organization/" + str(id) if type(id) == int else id
        header = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        result = self.https_put(url=self.url_modify_organization, user=self.user, password=self.password,
                                payload=details,
                                header=header)
        if result['status_code'] == 200:
            return result
        else:
            raise Exception(result)

    def get_all_environments(self):
        '''
        Function to get all environments accessible by this user

        :return: list
        '''
        self.url_get_environments = self.url_base + "/api/environments"
        page = 1
        envs = []
        total = 0
        while True:
            url = self.url_get_environments + "?per_page=100&page=" + str(page)
            result = self.https_get(
                url=url, user=self.user, password=self.password)
            if result['status_code'] == 200:
                if 'subtotal' in result['data']:
                    total = result['data']['subtotal']
                    if 'results' in result['data']:
                        for i in result['data']['results']:
                            envs.append(i)
                    if len(envs) >= total:
                        break
                page += 1
            else:
                raise Exception(result)
        return envs

    def get_all_organizations(self):
        '''
        Function to get all organizations accessible by the user

        :return: list
        '''
        self.url_get_all_organizations = self.url_base + "/api/organizations"
        page = 1
        orgs = []
        total = 0
        while True:
            url = self.url_get_all_organizations + \
                "?per_page=100&page=" + str(page)
            result = self.https_get(
                url=url, user=self.user, password=self.password)
            if result['status_code'] == 200:
                if 'subtotal' in result['data']:
                    total = result['data']['subtotal']
                    if 'results' in result['data']:
                        for i in result['data']['results']:
                            orgs.append(i)
                    if len(orgs) >= total:
                        break
                page += 1
            else:
                raise Exception(result)
        return orgs

     # Host level functionality

    # Host Level Facts
    def get_all_hosts(self, search_string=None):
        '''
        Gets all the hosts available to the user and returns a list

        :return: list
        '''
        self.url_get_all_hosts = self.url_base + "/api/hosts?"
        if search_string:
            self.url_get_all_hosts += 'search=' + search_string
        page = 1
        hosts = []
        total = 0
        while True:
            url = self.url_get_all_hosts + "per_page=100&page=" + str(page)
            result = self.https_get(
                url=url, user=self.user, password=self.password)
            if result['status_code'] == 200:
                if 'subtotal' in result['data']:
                    total = result['data']['subtotal']
                    if 'results' in result['data']:
                        for i in result['data']['results']:
                            hosts.append(i)
                    if len(hosts) >= total:
                        break
                    page += 1
            else:
                raise Exception(result)
        return hosts

    def add_new_host(self, host):
        '''
        Function to create a new host entry in foreman

        :param host: dict(host details)
        :return: dict
        '''
        self.url_new_host = self.url_base + "/api/hosts"
        header = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        result = self.https_post(url=self.url_new_host, user=self.user, password=self.password,
                                 payload=host,
                                 header=header)

        if result['status_code'] == 201:
            return result
        else:
            raise Exception(result)

    def modify_host(self, id, details):
        '''
        Function to edit an existing host entry in foreman

        :param id: int or str (Id of host in foreman)
        :param details: dict(host details)
        :return: dict
        '''
        self.url_update_host = self.url_base + \
            "/api/hosts/" + str(id) if type(id) == int else id
        header = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        result = self.https_put(url=self.url_update_host, user=self.user, password=self.password,
                                payload=details,
                                header=header)
        if result['status_code'] == 200:
            return result
        else:
            pprint(result)
            raise Exception(result)

    def remove_host(self, id):
        '''
        Function to remove host entry in foreman

        :param id: int or str (Id of host in foreman)
        :return: dict
        '''
        self.url_delete_host = self.url_base + "/api/hosts/" + \
            (str(id) if type(id) == int else id)
        print(self.url_delete_host)
        result = self.https_delete(
            url=self.url_delete_host, user=self.user, password=self.password, payload={})
        if result['status_code'] == 200:
            return result
        else:
            raise Exception(result)

    def get_host(self, name):
        '''
        Function to get the details of a particular host
        :param name: str
        :return: dict
        '''
        self.url_get_host = self.url_base + "/api/hosts/" + name
        result = self.https_get(url=self.url_get_host,
                                user=self.user, password=self.password)
        if result['status_code'] == 200:
            return result['data']
        else:
            syslog.syslog(syslog.LOG_ERR, self.url_get_host + result.__str__())
            raise Exception("Http error: {}".format(result['status_code']))

    def get_host_facts(self, name):
        '''
        Function to get the facts of a particular host
        :param name: str
        :return: dict
        '''
        self.url_get_host_fact = self.url_base + \
            "/api/hosts/{}/facts?".format(name)
        page = 1
        per_page = 100
        facts = {}
        while True:
            result = self.https_get(url=self.url_get_host_fact +
                                    "per_page={}&page={}".format(
                                        str(per_page), str(page)),
                                    user=self.user, password=self.password)
            if result['status_code'] == 200:
                if len(result['data']['results']) <= 0:
                    break
                facts.update(result['data']['results'][name])
                page += 1
            else:
                syslog.syslog(syslog.LOG_ERR,
                              self.url_get_host + result.__str__())
                raise Exception("Http error: {}".format(result['status_code']))
        return facts

    # Reports Level functionality
    def get_last_report(self, host_name):
        self.url_get_last_report = self.url_base + \
            "/api/hosts/" + host_name + "/config_reports/last"
        result = self.https_get(
            url=self.url_get_last_report, user=self.user, password=self.password)
        if result['status_code'] == 200:
            return result['data']
        else:
            syslog.syslog(syslog.LOG_ERR,
                          self.url_get_last_report + result.__str__())
            return result['data']

    # --------------------------------------------------------------------------------------------------------  #
    #                              Below functions are common for syncing                                       #
    # --------------------------------------------------------------------------------------------------------  #

    def order_hierarchy_numbered(self, diffs):
        '''
        Order the hierarchy for creating hgs
        will create a numbered map with elements in higher hierarchy with lower numbered keys
        :param diffs: list(['a/b/c', 'a/d', 'a/b/d'])
        :return: dict({'2':'a/b, '3':['a/b/c', 'a/b/d']})
        '''
        mappy = {}
        for d in diffs:
            if len(d.split("/")) in mappy.keys():
                mappy[len(d.split("/"))].append(d)
            else:
                mappy[len(d.split("/"))] = []
                mappy[len(d.split("/"))].append(d)
        return mappy

    # --------------------------------------------------------------------------------------------------------  #
    #                              Below functions are for syncing the HostGroups                               #
    # --------------------------------------------------------------------------------------------------------  #

    def get_hostgroup_hierarchy_from_foreman(self, environment, hgs=None):
        '''
        Get Foreman HostGroup Hierarchy for ENV

        :param hgs: list(hostgroup)
        :param environment: str(ENV name)
        :return:
        '''
        if not hgs:
            hgs = self.get_all_hostgroup()
        iac_hg = []
        for hg in hgs:
            if 'environment_name' in hg:
                if hg['environment_name']:
                    if environment.upper() == hg['environment_name'].upper():
                        iac_hg.append(hg['title'])
        return iac_hg

    def compare_the_hg_hierarchy(self, local, foreman):
        '''
        Function to find whether the hosgroup hierarchy is matching

        :param local: list(['a/b/c', 'a/d', 'a/b/d'])
        :param foreman: list(['a/b/c', 'a/d', 'a/b'])
        :return: list(['a/b/d']) - The ones that are not in sync with the
        '''
        result = []
        for l in local:
            if l not in foreman:
                result.append(l)
        return result

    def create_hostgroup_hierarchy_on_foreman(self, hierarchy, environment):
        '''
        Takes a single hierarchy 'a/b/c' and creates the hostgroups in foreman that which are not there
        :param hierarchy: str('a/b/c')
        :param environment: Foreman Environment
        :return: None
        '''
        foreman_hgs = self.get_all_hostgroup()
        print('----------------------- Create HGS -----------------------')
        print(hierarchy)
        hgs = hierarchy.split('/')
        iac_hg = []
        # Segregating HG names for finding the ones needed to be created
        # And finding the global detail for the env
        for hg in foreman_hgs:
            if hg['environment_name']:
                if environment.upper() in hg['environment_name'].upper():
                    iac_hg.append(hg['name'])
        # Finding the Environments
        env = None
        envs = self.get_all_environments()
        for e in envs:
            if environment == e['name']:
                env = e
        if not env:
            raise Exception('Couldn\'t find environment (' +
                            environment + ') for the given environment')
        # Finding HGS not in Foreman
        to_create = []
        for h in hgs:
            if h not in iac_hg:
                # we have to create these Host Groups
                to_create.append(h)
        # Creating the hostgroups not in foreman as a direct child of the global
        for i in to_create:
            hg = {
                'hostgroup': {
                    'name': i,
                    'environment_id': env['id'],
                }
            }
            print(hg)
            self.add_new_hostgroup(hg)
            # pprint(self.add_new_hostgroup(hg))
        print('---------------------------------------------------------------')

    def diff_hostgroup_hierarchy(self, local_hierarchy, environment):
        '''
        Does all the comparison and gives the diff wrt to local and Foreman
        :param local_hierarchy: list(['a/b/c', 'a/d', 'a/b/d'])
        :param environment: str()
        :return: dict
        '''
        foreman_hgs = self.get_all_hostgroup()
        # Gets the output of the function Hostgroup.get_hostgroup_hierarchy()
        local_hgs_hierarchy = copy(local_hierarchy)
        diffs = self.compare_the_hg_hierarchy(local=local_hgs_hierarchy,
                                              foreman=self.get_hostgroup_hierarchy_from_foreman(
                                                  hgs=foreman_hgs, environment=environment))
        diffs = self.order_hierarchy_numbered(diffs)
        return diffs

    def order_hostgroup_hierarchy_on_foreman(self, hierarchy, environment):
        '''
        Function to order hostgroup on the foreman side
        Takes a single hierarchy 'a/b/c' and creates a structure in foreman for that which is not in foreman
        :param hierarchy: Example('a/b/c')
        :param environment: Foreman Environment name
        :return: None
        '''
        foreman_hgs = self.get_all_hostgroup()
        print('----------------------- Order HGS -----------------------')
        print(hierarchy)
        lhgs = hierarchy.split('/')
        iac_hg = {}
        # Segregating HG names for finding the ones needed to be created
        # And finding the global detail for the env
        for hg in foreman_hgs:
            if hg['environment_name']:
                if environment.upper() in hg['environment_name'].upper():
                    for lhg in lhgs:
                        if lhg == hg['name']:
                            iac_hg[lhg] = deepcopy(hg)
        # Raising an error if hostgroup is not found on foreman
        if not len(lhgs) == len(iac_hg):
            raise Exception(
                'Couldn\'t find some hostgroup for the given environment in hierarchy:\n', hierarchy)
        # Finding HGS not in Foreman
        for i in range(0, len(lhgs)):
            hg = {
                'hostgroup': {
                    'id': iac_hg[lhgs[i]]['id'],
                }
            }
            if i > 0:
                print(iac_hg[lhgs[i]]['name'])
                hg['hostgroup']['parent_id'] = iac_hg[lhgs[i - 1]]['id']
                hg['hostgroup']['environment_id'] = iac_hg[lhgs[i - 1]
                                                           ]['environment_id']
                pprint(hg)
                self.modify_hostgroup(iac_hg[lhgs[i]]['id'], hg)
        print('---------------------------------------------------------------')

    def sync_hostgroups_to_remote(self, local_hierarchy, environment):
        '''
         Function to sync hostgroup onto foreman
        :param local_hierarchy:
        :param environment:
        :return: None
        '''
        # Finding the hierarchies that are not in sync &
        # Segregating into levels from top to down
        diffs = self.diff_hostgroup_hierarchy(local_hierarchy=local_hierarchy,
                                              environment=environment)
        # Creating the hierarchy level by level
        levels = list(diffs.keys())
        levels.sort()
        print('levels of host group tree affected:\n', levels)
        # Creating and rearranging the hostGroup Hierarchy
        for l in levels:
            for d in diffs[l]:
                # Creating any hostgroup that are not present in foreman
                self.create_hierarchy_on_foreman(
                    hierarchy=d, environment=environment)
                # Ordering the hostgroups hierarchy in foreman to be in sync with the local
                self.order_hostgroup_hierarchy_on_foreman(d, environment)

    # --------------------------------------------------------------------------------------------------------  #
    #                              Below functions are for syncing the Organizations                            #
    # --------------------------------------------------------------------------------------------------------  #

    def get_orgs_from_foreman(self):
        '''
        Get Foreman organization Hierarchy
        :return: list
        '''
        orgs = []
        for org in self.get_all_organizations():
            if 'title' in org:
                orgs.append(org['title'])
        return orgs

    def compare_the_org_hierarchy(self, local, foreman):
        '''
        Function to find whether the org hierarchy is matching

        :param local: list(['a/b/c', 'a/d', 'a/b/d'])
        :param foreman: list(['a/b/c', 'a/d', 'a/b'])
        :return: list(['a/b/d']) - The ones that are not in sync with the
        '''
        result = []
        for l in local:
            if l not in foreman:
                result.append(l)
        return result

    def create_org_hierarchy_on_foreman(self, hierarchy):
        '''
        Takes a single hierarchy 'a/b/c' and creates the organization in foreman that which are not there
        :param hierarchy: str('a/b/c')
        :return: None
        '''
        foreman_orgs = []
        for org in self.get_all_organizations():
            foreman_orgs.append(org['name'])
        print('----------------------- Create Orgs -----------------------')
        print(hierarchy)
        orgs = hierarchy.split('/')
        # Finding Orgs not in Foreman
        to_create = []
        for org in orgs:
            if org not in foreman_orgs:
                # we have to create these Host Groups
                to_create.append(org)
        # Creating the hostgroups not in foreman as a direct child of the global
        for i in to_create:
            hg = {
                'organization': {
                    'name': i,
                }
            }
            print(hg)
            self.add_new_hostgroup(hg)
            # pprint(self.add_new_hostgroup(hg))
        print('---------------------------------------------------------------')

    def diff_organization_hierarchy(self, local_hierarchy):
        '''
        Does all the comparison and gives the diff wrt to local and Foreman
        :param local_hierarchy: list(['a/b/c', 'a/d', 'a/b/d'])
        :return: dict
        '''
        foreman_hgs = self.get_all_hostgroup()
        local_hgs_hierarchy = copy(local_hierarchy)
        diffs = self.compare_the_org_hierarchy(local=local_hgs_hierarchy,
                                               foreman=self.get_orgs_from_foreman())
        diffs = self.order_hierarchy_numbered(diffs)
        return diffs

    def order_organization_hierarchy_on_foreman(self, hierarchy):
        '''
        Function to order hostgroup on the foreman side
        Takes a single hierarchy 'a/b/c' and creates a structure in foreman for that which is not in foreman
        :param hierarchy: Example('a/b/c')
        :return: None
        '''
        foreman_orgs = self.get_orgs_from_foreman()
        print('----------------------- Order organization -----------------------')
        print(hierarchy)
        lorgs = hierarchy.split('/')
        up_org = {}
        # Segregating organization names for finding the ones needed to be created
        for org in foreman_orgs:
            for lorg in lorgs:
                if lorg == org['name']:
                    up_org[lorg] = deepcopy(org)
        # Raising an error if organization is not found on foreman
        if not len(lorgs) == len(up_org):
            raise Exception(
                'Couldn\'t find some orgs for the given hierarchy:\n', hierarchy)
        # Ordering organization on Foreman
        for i in range(0, len(lorgs)):
            org = {
                'organization': {
                    'id': up_org[lorgs[i]]['id'],
                }
            }
            if i > 0:
                print(org[lorgs[i]]['name'])
                org['organization']['parent_id'] = up_org[lorgs[i - 1]]['id']
                pprint(org)
                self.modify_organization(up_org[lorgs[i]]['id'], org)
        print('---------------------------------------------------------------')

    def sync_organizations_to_remote(self, local_hierarchy):
        '''
         Function to sync organization onto foreman
        :param local_hierarchy:
        :return: None
        '''
        # Finding the hierarchies that are not in sync &
        # Segregating into levels from top to down
        diffs = self.diff_organization_hierarchy(
            local_hierarchy=local_hierarchy)
        # Creating the hierarchy level by level
        levels = list(diffs.keys())
        levels.sort()
        print('levels of organization tree affected:\n', levels)
        # Creating and rearranging the organization Hierarchy
        for l in levels:
            for d in diffs[l]:
                # Creating any organization that are not present in foreman
                self.create_org_hierarchy_on_foreman(hierarchy=d)
                # Ordering the organization hierarchy in foreman to be in sync with the local
                self.order_organization_hierarchy_on_foreman(d)
