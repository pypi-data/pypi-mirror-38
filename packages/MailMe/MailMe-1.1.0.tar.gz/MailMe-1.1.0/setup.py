"""
MailMe
------

Library created to abstract work with SMTP servers to
send e-mails. Its use is mainly in projects structured
as micro services, since it has can be integrated with
RabbitMQ servers, allowing the sending of many queued
emails.
"""
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as file:
    long_desc = file.read()

setup(
    name='MailMe',
    version='1.1.0',
    url='http://github.com/otoru/mailme',
    license='MIT',
    author='Vitor Hugo de Olveira Vargas',
    author_email='vitor.hov@gmail.com',
    description='Send e-mails with python.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=['email', 'mail', 'python'],
    zip_safe=False,
    include_package_data=True,
    platforms=['any'],
    project_urls = {
        'Documentation': 'http://github.com/otoru/mailme/README.md',
        'Source Code': 'http://github.com/otoru/mailme/mailme/',
        'Bug Tracker': 'http://github.com/otoru/mailme/issues',
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Email',
        'Topic :: Utilities'
    ]
)
