from setuptools import setup

setup(
    name='muxminos',
    version='0.3.3',
    author='hujianxin',
    author_email='hujianxin@xiaomi.com',
    include_package_data=True,
    install_requires=['Click', 'gitpython', 'pyyaml', 'configobj'],
    license='Apache License',
    description='A cmd tool for tmuxinator generating configuration file for minos',
    py_modules=['muxminos'],
    entry_points={
        'console_scripts': [
            'muxminos=muxminos:cli',
            'mm=muxminos:cli'
        ]
    }
)
