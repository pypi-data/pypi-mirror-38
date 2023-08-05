from setuptools import setup, find_packages


setup(
    name="sweeter",
    version="0.0.1",
    author="Leo Tong",
    author_email="tonglei@qq.com",
    description="Web UI Autotest with Selenium & Excel",
    #long_description=open("README.rst").read(),
    license="Apache License, Version 2.0",
    url="https://github.com/tonglei100/sweeter",
    packages=['sweeter', 'sweeter.keywords', 'sweeter.lib','sweeter.example'],
    package_data={'sweeter': ['*.py', 'example/sweetest_example.zip']},
    install_requires=[
        'selenium',
        'xlrd',
        'xlsxwriter',
        'requests',
        'injson',
        'Appium-Python-Client'
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': [
            'sweeter=sweeter:sweeter'
        ]
    }
)
