from setuptools import setup, find_packages

setup(
    name='bagga',
    packages=find_packages(),
    install_requires=[
        'pyyaml==3.11',
    ],
    version='0.0.5',
    description='Docker command tool',
    author='Vitalii Omelchenko',
    author_email='vitaly.om25@gmail.com',
    url='https://github.com/kai25/docker-command-tool',
    keywords=['Docker', 'cli'],
    entry_points={
            'console_scripts': ['bagga=docker_command_tool:main'],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

)
