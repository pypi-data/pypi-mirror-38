# -*- encoding: utf-8 -*-
from pathlib import Path
from setuptools import find_packages, setup


basedir = Path(__file__).parent
with (basedir / 'README.rst').open(encoding='utf-8') as f:
    readme = f.read()
with (basedir / 'CHANGELOG.rst').open(encoding='utf-8') as f:
    changelog = f.read()
long_description = '\n'.join([readme, changelog])


setup(
    name='rst2html5slides',
    version='1.2.2',
    license='MIT License',
    author='André Felipe Dias',
    author_email='andref.dias@gmail.com',
    keywords=['restructuredText', 'slide', 'docutils', 'presentation', 'html5'],
    description='rst2html5slides generates a slideshow from a reStructuredText file.',
    long_description=long_description,
    platforms='any',
    install_requires=[
        'docutils>=0.14',
        'genshi>=0.7',
        'micawber>=0.3.5',
        'rst2html5>=1.9.5',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
    packages=find_packages(),
    package_data={
        'rst2html5slides': [
            'template/*',
            'css/*.css',
            'js/*.js',
            'js/greensock/*.js',
            'js/greensock/plugins/*.js',
            'js/greensock/utils/*.js',
            'js/greensock/easing/*.js',
        ]
    },
    entry_points={
        'console_scripts': [
            'rst2html5slides = rst2html5slides.rst2html5slides:main',
        ],
    },
)
