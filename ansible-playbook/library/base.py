#!/usr/bin/python

from abc import ABCMeta
from abc import abstractmethod
import json


class PackageManager(object):

    __metaclass__ = ABCMeta

    def __init__(self, module):
        self.__module = module

    @property
    def module(self):
        return self.__module

    @property
    def name(self):
        return self.__module.params['name']

    @property
    def state(self):
        return self.__module.params['state']

    @abstractmethod
    def install(self):
        raise NotImplementedError

    @abstractmethod
    def upgrade(self):
        raise NotImplementedError

    @abstractmethod
    def uninstall(self):
        raise NotImplementedError

    @abstractmethod
    def is_valid_package(self):
        raise NotImplementedError

    @abstractmethod
    def is_latest_version(self):
        raise NotImplementedError

    @abstractmethod
    def get_installed_packages(self, links=False):
        raise NotImplementedError

    def get_installed_version(self):
        return self.get_installed_packages().get(self.name)

    def should_install(self):
        return self.state in ['present', 'latest'] and not self.is_installed()

    def should_upgrade(self):
        return self.state == 'latest' and self.is_installed() and not self.is_latest_version()

    def should_uninstall(self):
        return self.state == 'absent' and self.is_installed()

    def is_installed(self):
        return self.name in self.get_installed_packages()

    def _run(self, cmd):
        rc, stdout, stderr = self.module.run_command(cmd)
        return rc

    def _get_json_via_subprocess(self, cmd):
        rc, stdout, stderr = self.module.run_command(cmd)
        assert rc == 0
        return json.loads(stdout)
