#!/usr/bin/python
# -*- coding: utf8 -*-
#Copyright:@BaeSystemsAI
#Original author: Heri Sutrisno
#Email:harry.sutrisno@baesystems.com
#Description: base class for foreman-python

import sys
import logging
import log
import socket
import urllib3
from foreman.client import Foreman
from validator import Validator


class ForemanBase:

    def __init__(self, config, loglevel=logging.INFO):
        logging.basicConfig(level=loglevel)
        log.LOGLEVEL = loglevel
        self.config = config['foreman']
        self.loglevel = loglevel
        self.validator = Validator()

    def get_config_section(self, section):
        try:
            cfg = self.config[section]
        except:
            cfg = []
        return cfg

    def get_fm_ip(self):
        hostname = socket.gethostname()
        ip_hostname = socket.gethostbyname(hostname)
        foreman_ip = "https://"
        foreman_ip += ip_hostname
        return foreman_ip

    def get_fm_hostname(self):
        hostname = socket.gethostname()
        return hostname

    def connect(self):
        log.log(log.LOG_INFO, "Establish connection to Foreman server")
        try:
            logging.disable(logging.WARNING)
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            self.fm = Foreman(self.get_fm_ip(), (self.config['auth']['user'], self.config['auth']['pass']), api_version=2, use_cache=False, strict_cache=False)
            # this is nescesary for detecting faulty credentials in yaml
            self.fm.architectures.index()
            logging.disable(self.loglevel-1)
        except:
            log.log(log.LOG_ERROR, "Cannot connect to Foreman-API")
            sys.exit(1)

    def get_api_error_msg(self, e):
        dr = e.res.json()
        try:
            msg = dr['error']['message']
        except KeyError:
            msg = dr['error']['full_messages'][0]

        return msg

    def update(ipaddress, hostname):
        """
        The update function takes the ip address and hostname passed into the function and adds it to the host file.
        :param ipaddress:
        :param hostname:
        """
        if 'linux' in sys.platform:
            filename = '/etc/hosts'
        else:
            log.log(log.LOG_ERROR, "your system platform is not linux base")
            sys.exit(1)

        outputfile = open(filename, 'a')
        entry = "\n" + ipaddress + "\t" + hostname + "\n"
        outputfile.writelines(entry)
        outputfile.close()

    def validip(ipaddress):
        """ str -> bool
        The function takes the IP address as a string and splits it by ".". It then checks to see if there are 4 items
        in the list. If not, it's not valid. Next, it makes sure the last two characters are not ".0", which would signify an
        invalid address. Third it checks the last character to make sure it's not a ".", which would be invalid. Lastly, it
        checks each item to make sure it's greater than 0 or equal to zero but less than or equal to 255.
        :param ipaddress:
        :return:
        """
        parts = ipaddress.split(".")
        if len(parts) != 4:
            return False
        if ipaddress[-2:] == '.0': return False
        if ipaddress[-1] == '.': return False
        for item in parts:
            if not 0 <= int(item) <= 255:
                return False
        return True

    def isValidHostname(hostname):
        """ str -> bool
        First it checks to see if the hostname is too long. Next, it checks to see if the first character is a number.
        If the last character is a ".", it is removed. A list of acceptable characters is then compiled and each section
        of the host name, split by any ".", is checked for valid characters. If there everything is valid, True is returned.
        :param hostname:
        :return:
        """
        if len(hostname) > 255:
            return False
        if hostname[0].isdigit(): return False
        if hostname[-1:] == ".":
            hostname = hostname[:-1] # strip exactly one dot from the right, if present
        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))

        def get_host(self, host_id):
            host = self.fm.hosts.show(id=host_id)
            return host

        def remove_host(self, host_id):
            try:
                self.fm.hosts.destroy(id=host_id)
                return True
            except:
                return False
