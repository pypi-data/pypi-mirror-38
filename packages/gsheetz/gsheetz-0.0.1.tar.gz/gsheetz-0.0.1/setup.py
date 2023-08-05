from setuptools import setup,find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()
setup(
    name='gsheetz',
    version='0.0.1',
    author='A1Liu',
    author_email='albertymliu@gmail.com',
    description='A small package for accessing the google sheets API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/a1liu/gsheetz',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent'
    ],
    install_requires=[
          'pandas','mr-clean','google-api-python-client','oauth2client'
      ]
)
