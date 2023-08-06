from setuptools import find_packages
from setuptools import setup

setup(
    name='netapp-lib',
    packages=find_packages(exclude=['*.tests', '*.tests.*',
                                    'tests.*', '*.tools', '*.tools.*',
                                    'tools.*', 'tests', 'tools']),
    version='2018.11.13',
    license='Proprietary::NetApp',
    description='netapp-lib is required for OpenStack and Ansible deployments to '
                'interact with NetApp storage systems.',
    author='NetApp, Inc.',
    author_email='ng-openstack-pypi@netapp.com',
    install_requires=[
        'xmltodict',
        'lxml'
    ],
    package_data={
        '': ['*.txt', '*.rst'],
    },
    include_package_data=True,
    keywords=['openstack', 'netapp', 'cinder', 'manila', 'netapp_lib', 'ansible'],
    classifiers=['Environment :: OpenStack'],
)
