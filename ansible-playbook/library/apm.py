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

    apm = APM(module)

    try:
        if not apm.is_valid_package():
            module.fail_json(msg='Module name: {} not found'.format(apm.name))

        if apm.should_install():
            changed = True
            apm.install()
        elif apm.should_upgrade():
            changed = True
            apm.upgrade()
        elif apm.should_uninstall():
            changed = True
            apm.uninstall()
        else:
            changed = False
    except Exception as e:
        module.fail_json(msg=e.message)
    else:
        module.exit_json(changed=changed)


class APM(object):

    def __init__(self, module):
        self.module = module
        self.name = module.params['name']
        self.state = module.params['state']

    def get_installed_packages(self, links=False):
        output = self.__run_json([
            'apm', 'list', '--json', '--links={}'.format(links)
        ])
        return {pkg['name']: pkg['version'] for pkg in output['user']}

    def get_installed_version(self):
        return self.get_installed_packages().get(self.name)

    def should_install(self):
        return self.state in ['present', 'latest'] and not self.is_installed()

    def should_upgrade(self):
        return self.state == 'latest' and self.is_installed() and not self.is_latest_version()

    def should_uninstall(self):
        return self.state == 'absent' and self.is_installed()

    def install(self):
        assert self.__run(['apm', 'install', self.name]) == 0

    def upgrade(self):
        assert self.__run(['apm', 'upgrade', '--confirm=False', self.name]) == 0

    def uninstall(self):
        assert self.__run(['apm', 'uninstall', self.name]) == 0

    def is_valid_package(self):
        return self.__run(['apm', 'view', self.name]) == 0

    def is_installed(self):
        return self.name in self.get_installed_packages()

    def is_latest_version(self):
        output = self.__run_json([
            'apm', 'view', self.name, '--json', '--compatible'
        ])
        return self.get_installed_version() == output['version']

    def __run(self, cmd):
        rc, stdout, stderr = self.module.run_command(cmd)
        return rc

    def __run_json(self, cmd):
        rc, stdout, stderr = self.module.run_command(cmd)
        assert rc == 0
        return json.loads(stdout)


if __name__ == '__main__':
    main()
