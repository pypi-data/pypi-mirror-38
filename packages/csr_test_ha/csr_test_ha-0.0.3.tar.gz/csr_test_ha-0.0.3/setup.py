from distutils.core import setup
from setuptools.command.install import install
from subprocess import check_call
import subprocess


project_name = 'csr_test_ha'
project_ver = '0.0.3'



class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        print "We are running in the postInstallCommand"
        subprocess.call(['pip', 'install', 'csr_azure_utils==0.0.98', '--user'])
        subprocess.call(['pip', 'install', 'csr_ha','--user'])
        install.run(self)


setup(
    name=project_name,
    version=project_ver,
    description='Utilities for csr1000v on Azure',
    author='Christopher Reder',
    author_email='creder@cisco.com',
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-azure/csr_test_ha',
    download_url='https://github4-chn.cisco.com/csr1000v-azure/' + project_name + '/archive/' + \
        project_ver + '.tar.gz',
    keywords=['cisco', 'azure', 'guestshell', 'csr1000v'],
    classifiers=[],
    license="MIT",
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
    }
)


