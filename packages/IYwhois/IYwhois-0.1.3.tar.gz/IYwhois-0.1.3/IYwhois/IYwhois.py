from collections import defaultdict
import re
import subprocess
import logging


class LookUp:
    def __init__(self, domain):
        self.domain = domain
        self._logger = logging.getLogger('IYwhois')
        self.data = {
            "domain": self.domain,
            "sources": None,
            "text": None
        }
        self._lookup()

    @staticmethod
    def _format(required_string):
        ''' reformatting string output of whois query'''
        edit = []
        for element in required_string.split('  '):
            if element == '':
                pass
            elif '>' in element:
                element = element.replace('>', '')
                element = element.replace('<', '')
                edit.append(element)
            else:
                edit.append(element)
        edit_to_str = '~'.join(edit).replace('~', ' ')
        result_sets = re.findall('(.*?):(.*?)\n', edit_to_str)
        result_dicts = [{key.strip(): value.strip()}
                        for key, value in result_sets]
        del result_sets

        for item in result_dicts:
            for k, v in item.items():
                if k.islower():
                    pass
                else:
                    if ' ' in k:
                        item[k.lower().replace(' ', '_')] = item.pop(k)
                    else:
                        item[k.lower()] = item.pop(k)
        return result_dicts

    @staticmethod
    def _storing_data(info_list):
        dd = defaultdict(list)
        for element in tuple(info_list):
            for key, value in element.items():
                try:
                    dd[key].append(value)
                except AttributeError:
                    dd[key] = value
            for key, value in element.items():
                if 'phone' in key or 'fax' in key:
                    dd[key] = re.sub('[^\d+]', '', value)
                elif key == 'domain_name':
                    dd[key] = list(set(dd[key]))
        if 'address' in dd.keys():
            if len(dd['address']) > 1:
                dd['address'] = ','.join(dd['address'])
            else:
                pass
        if 'terms_of_use' in dd.keys():
            dd.pop('terms_of_use')
        return dd

    def _find_contacts(self, in_list):
        contacts = []
        counter = 0
        c_start_index = 0
        c_end_index = 0
        for element in in_list:
            try:
                for key, value in element.items():
                    if key == 'contact':
                        counter += 1
            except AttributeError:
                self._logger.error("Something went wrong while enumerating contacts")
        if counter > 1:
            start_indexes = []
            end_indexes = []
        for index, element in enumerate(in_list):
            for key, value in element.items():
                if key == 'contact':
                    start_indexes.append(index)
                elif key == 'e-mail':
                    end_indexes.append(index)
        for i in range(len(start_indexes)):
            contact = in_list[start_indexes[i]:end_indexes[i] + 1]
            temp_contact = {contact[0]['contact']: contact[1:]}
            contacts.append(temp_contact)
            del temp_contact
            del contact
        for contact in contacts:
            for key, value in contact.items():
                for item in contact[key]:
                    for element in in_list:
                        if item == element:
                            del in_list[in_list.index(element)]
                        elif 'contact' in element.keys():
                            del in_list[in_list.index(element)]
        contacts_ = {}
        for contact in contacts:
            for key, value in contact.items():
                dd = {}
                contacts_.update({key: self._storing_data(contact[key])})
        self.data['sources'].update({'tld': self._storing_data(in_list)})
        self.data['sources']['tld'].update({'contacts': contacts_})
        del contacts

    def _lookup(self):
        junk_query = subprocess.run(
            f'whois {self.domain}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='UTF-8')
        self.data.update({"text": junk_query})
        # creating pretty output
        junk_query = [x for x in junk_query.stdout.strip().split('\n')
                      if x != '']
        working_query = []
        for element in junk_query:
            if element.startswith('%'):
                pass  # delete all comments strings
            else:
                working_query.append(element)
        clean_indexes = []
        for element in working_query:
            if 'Last update of whois database' in element or 'Last update of WHOIS database' in element:
                clean_indexes.append(working_query.index(element))
        if len(clean_indexes) == 0 or len(clean_indexes) == 1:
            pass
        else:
            markers = []
            for element in clean_indexes:
                for item in working_query[element:]:
                    if 'Domain Name' in item or 'domain name' in item or 'Domain name' in item:
                        markers.append(working_query.index(item))
            if len(markers) == 0:
                pass
            else:
                temp_resp = '\n'.join(working_query)
                junk = re.findall('<<<(.*?)\\nDomain|<<<(.*?)\\ndomain|<<<(.*?)$', temp_resp, re.DOTALL)
                for element in junk:
                    if type(element) == tuple:
                        element = list(filter(None, element))
                        temp_resp = temp_resp.replace(''.join(element), '')
                working_query = temp_resp.split('\n')
        response = '\n'.join(working_query)
        del junk_query
        del working_query

        try:
            # no data update required: No info on current domain
            # return False
            # parse response to result and update sources
            split_args = re.search(
                '(whois:[\s\t\n]+(?!:\/\/)([a-zA-Z0-9-_]+\.)*[a-zA-Z0-9][a-zA-Z0-9-_]+\.[a-zA-Z]{2,11}?)\n', response, re.DOTALL).group(1)
            parted = response.split(split_args)
            if len(parted) == 1 or len(parted) == 2:
                pass
            else:
                self._logger.error("Partition error")

            tld_info = parted[0]
            sld_info = parted[1]
            assumption = re.search(
                '(.*?source.*?\w+)\\n', parted[1], re.DOTALL).group(1)
            sld_info = sld_info.replace(assumption, '')
            tld_info = tld_info + assumption
            del parted

            tld = LookUp._format(tld_info)
            sld = LookUp._format(sld_info)
            sources = {"sld": self._storing_data(sld)}
            self.data.update({"sources": sources})
            self._find_contacts(tld)
        except AttributeError:
            # There is no splitting required
            # Users operating system is other than Mac OS
            info = LookUp._format(response)
            data = self._storing_data(info)
            sources = {"sld": data}
            self.data.update({"sources":sources})
            try:
                self._find_contacts(info)
            except:
                self._logger.error("No contacts found")
