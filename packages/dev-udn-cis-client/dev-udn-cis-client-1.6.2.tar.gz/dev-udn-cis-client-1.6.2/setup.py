from setuptools import setup
from setuptools.command.install import install
import subprocess


class PostInstallCommand(install):
    def run(self):
        try:
            # works at least for Ubuntu and Centos
            # TODO for other OS
            add_autocompletion = 'cp udn-cis-client-complete.sh /etc/bash_completion.d/'
            ret = subprocess.call(add_autocompletion.split())
            if ret == 0:
                print("bash_completion was installed")
            else:
                print('Warning: bash_completion was not installed!')
        except Exception as e:
            print('Warning: Can not install bash_completion:')
            print(e)
        install.run(self)


setup(
    name='dev-udn-cis-client',
    version='1.6.2',
    description='DEV UDN CIS client tool',
    packages=[
        'cis_client',
        'cis_client.commands',
        'cis_client.lib',
        'cis_client.lib.aaa',
        'cis_client.lib.cis_north',
        'cis_client.lib.cis_south',
        'cis_client.lib.cis_gateway',
    ],
    include_package_data=True,
    install_requires=[
        'click',
        'terminaltables',
        'requests',
        'progressbar2',
        'paramiko',
        'future',
        'futures',
        'pycurl',
        'retrying',
    ],
    entry_points='''
        [console_scripts]
        udn-cis-client=cis_client.cli:cli
    ''',
    data_files=[
        ('.', ['udn-cis-client-complete.sh']),
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    zip_safe=False,
    script_name='setup.py',
    author='Marian Horban',
    author_email='mhorban@vidscale.com'
)
