# coding: utf-8
"""Setup config file to package the configuration database."""
import os
from setuptools import setup


def package_files(directory):
    """Get list of data files to add to the package."""
    paths = []
    for (path, _, file_names) in os.walk(directory):
        for filename in file_names:
            paths.append(os.path.join('..', path, filename))
    return paths


DATA = package_files('config_db/data')
TEST_DATA = package_files('config_db/tests/data')


with open('README.md', 'r') as file:
    LONG_DESCRIPTION = file.read()


setup(name='skasip_config_db',
      version='1.0.15',
      author='SKA SDP SIP team.',
      description='SIP Execution Control Configuration Database library.',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      url='https://github.com/SKA-ScienceDataProcessor/integration-prototype'
          '/tree/master/sip/execution_control/configuration_db',
      packages=['config_db', 'config_db/utils', 'config_db/tests'],
      scripts=[
          'config_db/scripts/skasip_config_db_init',
          'config_db/scripts/skasip_config_db_add_sbi',
          'config_db/scripts/skasip_config_db_update_state',
      ],
      package_data={'': DATA + TEST_DATA},
      include_package_data=True,
      install_requires=[
          'redis>=2.10.6',
          'jsonschema>=2.6.0',
          'jinja2>=2.10',
          'PyYaml>=3.13'
      ],
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python :: 3 :: Only",
          "Development Status :: 1 - Planning",
          "License :: OSI Approved :: BSD License"
      ]
      )
