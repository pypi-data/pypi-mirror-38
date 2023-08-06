from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(name='cherry-python',
      version='0.1.4',
      description='Cherry Servers API client',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://bitbucket.org/cherryservers/cherry-python-api',
      author='Aarturas Razinskij',
      author_email='arturas.razinskij@cherryservers.com',
      license='LGPL v3',
      packages=['cherry'],
      install_requires='requests',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
    ]
)