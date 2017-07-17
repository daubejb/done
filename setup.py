from setuptools import setup, find_packages

setup(
    name='done',
    version='1.0',
    author='Jeffrey B. Daube',
    author_email='daubejb@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url="http://www.github.com/daubejb/done",
    description='tdod app to manage todo list from terminal with \
                data residing on a google sheet',
    keywords='todo to do list application done daube design \
             dabedesign',
    install_requires=[
        'terminalTables',
        'prompt_toolkit',
        'apiclient',
        'oauth2client',
        'colorama'],
    entry_points={
        'console_scripts': [
            'd=main:main',
        ],
    },
)
