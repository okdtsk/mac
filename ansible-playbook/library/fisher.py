#!/usr/bin/python

import json

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec={
            'name': {'required': True},
            'state': {'default': 'present',
                      'choices': ['present', 'absent', 'latest']},
        },
    )

    fisher = Fisher(module)

    try:
        if not fisher.is_valid_package():
            module.fail_json(msg='Module name: {} not found'.format(fisher.name))

        if fisher.should_install():
            changed = True
            fisher.install()
        elif fisher.should_upgrade():
            changed = True
            fisher.upgrade()
        elif fisher.should_uninstall():
            changed = True
            fisher.uninstall()
        else:
            changed = False
    except Exception as e:
        module.fail_json(msg=e.message)
    else:
        module.exit_json(changed=changed)


class Fisher(object):

    def __init__(self, module):
        self.module = module
        self.name = module.params['name']
        self.state = module.params['state']

    def get_installed_packages(self, links=False):
        return self.__run_stdout('fisher ls -l')

    def get_installed_version(self):
        return self.name in self.get_installed_packages()

    def should_install(self):
        return self.state in ['present', 'latest'] and not self.is_installed()

    def should_upgrade(self):
        return self.state == 'latest' and self.is_installed() and not self.is_latest_version()

    def should_uninstall(self):
        return self.state == 'absent' and self.is_installed()

    def install(self):
        assert self.__run('fisher install {}'.format(self.name)) == 0

    def upgrade(self):
        assert self.__run('fisher update {}'.format(self.name)) == 0

    def uninstall(self):
        assert self.__run('fisher rm {}'.format(self.name)) == 0

    def is_valid_package(self):
        return self.__run('fisher ls-remote {}'.format(self.name)) == 0

    def is_installed(self):
        return self.name in self.get_installed_packages()

    def is_latest_version(self):
        return False  # Currently we cannot fetch latest version num via fisher

    def __run(self, cmd):
        rc, stdout, stderr = self.__run_as_fish(cmd)
        return rc

    def __run_stdout(self, cmd):
        rc, stdout, stderr = self.__run_as_fish(cmd)
        assert rc == 0
        return stdout

    def __run_as_fish(self, cmd):
        return self.module.run_command(['fish', '-c', cmd])


if __name__ == '__main__':
    main()
