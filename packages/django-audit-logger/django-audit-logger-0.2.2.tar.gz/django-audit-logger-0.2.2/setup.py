"""
setuptools config
"""
import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-audit-logger',
    version='0.2.2',
    author='Sander Heling, Jasper Koops, et al',
    author_email='info@wend.nl',
    description='A logger to be used internally',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
    install_requires=[
        'boto3',
        'celery',
        'mock',
        'django',
        'redis',
    ],
)
