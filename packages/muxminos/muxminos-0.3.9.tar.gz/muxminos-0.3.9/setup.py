from setuptools import setup

setup(
    name='muxminos',
    version='0.3.9',
    author='hujianxin',
    author_email='hujianxin@xiaomi.com',
    include_package_data=True,
    install_requires=['Click', 'gitpython', 'pyyaml', 'configobj'],
    license='Apache License',
    description='A cmd tool for tmuxinator generating configuration file for minos',
    packages=['muxminos'],
    entry_points={
        'console_scripts': [
            'muxminos=muxminos.cmd:cli',
            'mm=muxminos.cmd:cli'
        ]
    }
)
