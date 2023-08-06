"""
setuptools config
"""
import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-audit-logger',
    version='1.0.1',
    author='Wend BV',
    author_email='info@wend.nl',
    description='A logger to be used internally',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    install_requires=[
        'boto3',
        'celery',
        'mock;python_version=="2.7"',
        'django>=1.4',
        'redis',
    ],
)
