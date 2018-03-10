#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import re


def main():
    module = AnsibleModule(
        argument_spec={
            'id': {'required': True},
            'state': {'default': 'present',
                      'choices': ['present', 'latest']},
        },
    )

    mas = MAS(module)

    try:
        if mas.should_install():
            changed = True
            mas.install()
        elif mas.should_upgrade():
            changed = True
            mas.upgrade()
        else:
            changed = False
    except Exception as e:
        module.fail_json(msg=e.message)
    else:
        module.exit_json(changed=changed)


class MAS(object):

    RE_LIST = re.compile(r'(?P<app_id>\d+) (?P<app_name>.+) \((?P<app_version>[0-9.]+)\)')
    RE_OUTDATED = re.compile((r'(?P<app_id>\d+) (?P<app_name>.+) \((?P<app_version>[0-9.]+) -> '
                              r'(?P<app_version_latest>[0-9.]+)\)'))

    def __init__(self, module):
        self.module = module
        self.id = module.params['id']
        self.state = module.params['state']

    def get_installed_packages(self):
        return self.__convert_mas_list_to_dict(self.__run_stdout([
            'mas', 'list'
        ]))

    def get_outdated_packages(self):
        return self.__convert_mas_outdated_to_dict(self.__run_stdout([
            'mas', 'outdated'
        ]))

    def get_installed_version(self):
        return self.get_installed_packages().get(self.id).get('app_version')

    def should_install(self):
        return self.state in ['present', 'latest'] and not self.is_installed()

    def should_upgrade(self):
        return self.state == 'latest' and self.is_installed() and not self.is_latest_version()

    def should_uninstall(self):
        return self.state == 'absent' and self.is_installed()

    def install(self):
        assert self.__run(['mas', 'install', self.id]) == 0

    def upgrade(self):
        assert self.__run(['mas', 'upgrade', self.id]) == 0

    def uninstall(self):
        raise NotImplementedError('No support to uninstall any package via mas')

    def is_installed(self):
        return self.id in self.get_installed_packages()

    def is_latest_version(self):
        return self.id not in self.get_outdated_packages()

    def __run(self, cmd):
        rc, stdout, stderr = self.module.run_command(cmd)
        return rc

    def __run_stdout(self, cmd):
        rc, stdout, stderr = self.module.run_command(cmd)
        assert rc == 0
        return stdout

    def __convert_mas_list_to_dict(self, list_output):
        return {d['app_id']: d for d in [self.RE_LIST.match(pkg).groupdict()
                                         for pkg in list_output.strip().splitlines()]}

    def __convert_mas_outdated_to_dict(self, list_output):
        return {d['app_id']: d for d in [self.RE_OUTDATED.match(pkg).groupdict()
                                         for pkg in list_output.strip().splitlines()]}


if __name__ == '__main__':
    main()
