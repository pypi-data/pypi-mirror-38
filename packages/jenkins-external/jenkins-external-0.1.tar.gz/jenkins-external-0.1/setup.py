import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='jenkins-external',
    version='0.1',
    py_modules=['jenkins_external'],

    entry_points={
        'console_scripts': [
            'jenkins-external = jenkins_external:main',
        ],

    },

    author='quantum',
    author_email='quantum2048@gmail.com',
    url='https://github.com/quantum5/jenkins-external',
    description='Runs a command, and sends its output to a Jenkins external job.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='jenkins command report',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
    ],
)
