# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from io import open
from os import makedirs, urandom
from os.path import exists, join
from shutil import rmtree
from tempfile import mkdtemp
from docutils.core import publish_file, publish_string
from rst2html5slides import SlideWriter


class TestSlideWriter(object):

    presentation = '''\
.. role:: small

.. class:: capa

Presentation Title
==================

Agenda
======

* Topic 1
* Topic 2
* Topic 3

|logotipo|

.. class:: chapter

Chapter 1
=========

Schema
======

|tdd cycle|

----

|python logo|


.. include:: junit.rst


.. title:: Testes Automatizados de Software
.. meta::
    :generator: rst2html5slides https://bitbucket.org/andre_felipe_dias/rst2html5slides
    :author: André Felipe Dias

.. |logotipo| image:: imagens/logotipo.png
.. |tdd cycle| image:: imagens/tdd_cycle.png
.. |python logo| image:: https://www.python.org/static/community_logos/python-logo-master-v3-TM.png
'''
    junit = '''\
JUnit
=====

JUnit is a testing framework'''
    css = 'div {background-color: red}'

    def setup(self):
        self.dest_dir = mkdtemp()
        self.source_dir = mkdtemp()
        self.source_path = join(self.source_dir, 'presentation.rst')
        makedirs(join(self.source_dir, 'imagens'))
        makedirs(join(self.source_dir, 'css'))
        with open(self.source_path, 'w', encoding='utf-8') as f:
            f.write(self.presentation)
        with open(join(self.source_dir, 'junit.rst'), 'w', encoding='utf-8') as f:
            f.write(self.junit)
        with open(join(self.source_dir, 'css', 'style.css'), 'w', encoding='utf-8') as f:
            f.write(self.css)
        with open(join(self.source_dir, 'imagens', 'tdd_cycle.png'), 'wb') as f:
            f.write(urandom(2 ** 16))
        with open(join(self.source_dir, 'imagens', 'not_used.png'), 'wb') as f:
            f.write(urandom(2 ** 11))
        with open(join(self.source_dir, 'imagens', 'logotipo.png'), 'wb') as f:
            f.write(urandom(2 ** 15))

    def teardown(self):
        rmtree(self.source_dir)
        rmtree(self.dest_dir)

    def test_destination_dir(self):
        output = publish_file(
            writer=SlideWriter(), source_path=self.source_path,
            destination_path=self.dest_dir,
            settings_overrides={'stylesheet': [join('css', 'style.css')]}
        )
        assert exists(join(self.dest_dir, 'presentation.html'))
        assert exists(join(self.dest_dir, 'css', 'style.css'))
        assert exists(join(self.dest_dir, 'imagens', 'tdd_cycle.png'))
        assert exists(join(self.dest_dir, 'imagens', 'logotipo.png'))
        # assert exists(join(self.dest_dir, 'css', 'slideshow.css'))
        assert exists(join(self.dest_dir, 'js'))
        assert not exists(join(self.dest_dir, 'imagens', 'not_used.png'))
        assert str('href="css/slideshow.css"') in output
        assert str('<script src="js/jquery.min.js">') in output
        assert str('src="https://www.python.org') in output

    def test_destination_path(self):
        output = publish_file(
            writer=SlideWriter(), source_path=self.source_path,
            destination_path=join(self.dest_dir, 'slides.html'),
            settings_overrides={'stylesheet': [join('css', 'style.css')]}
        )
        assert exists(join(self.dest_dir, 'slides.html'))
        assert not exists(join(self.dest_dir, 'presentation.html'))
        assert exists(join(self.dest_dir, 'css', 'style.css'))
        assert exists(join(self.dest_dir, 'imagens', 'tdd_cycle.png'))
        assert exists(join(self.dest_dir, 'imagens', 'logotipo.png'))
        assert not exists(join(self.dest_dir, 'imagens', 'not_used.png'))
        assert exists(join(self.dest_dir, 'css', 'slideshow.css'))
        assert exists(join(self.dest_dir, 'js'))
        assert str('href="css/slideshow.css"') in output
        assert str('<script src="js/jquery.min.js">') in output
        assert str('src="https://www.python.org') in output

    def test_no_destination(self):
        output = publish_string(
            writer=SlideWriter(), source=self.junit,
            settings_overrides={'stylesheet': [join(self.source_dir, 'css', 'style.css')],
                                'output_encoding': 'unicode'}
        )
        assert not exists(join(self.dest_dir, 'presentation.html'))
        assert not exists(join(self.dest_dir, 'css', 'style.css'))
        assert not exists(join(self.dest_dir, 'imagens', 'tdd_cycle.png'))
        assert not exists(join(self.dest_dir, 'imagens', 'logotipo.png'))
        assert not exists(join(self.dest_dir, 'imagens', 'not_used.png'))
        assert not exists(join(self.dest_dir, 'css', 'slideshow.css'))
        assert not exists(join(self.dest_dir, 'js'))
        assert str('href="css/slideshow.css"') in output
        assert str('<script src="js/jquery.min.js">') in output

    def test_stylesheet_from_current_dir(self):
        '''
        Test if a stylesheet located at current directory is correctly copied to output directory
        '''
        other_dir = mkdtemp()
        try:
            os.chdir(other_dir)
            makedirs(join(other_dir, 'css'))
            with open(join(other_dir, 'css', 'custom.css'), 'w') as f:
                f.write('a {text-decoration: none}')
            output = publish_string(
                writer=SlideWriter(), source=self.presentation, source_path=self.source_path,
                destination_path=join(self.dest_dir, 'slides.html'),
                settings_overrides={'stylesheet': [join('css', 'style.css'), join('css', 'custom.css')],
                                    'output_encoding': 'unicode'}
            )
            assert exists(join(self.dest_dir, 'slides.html'))
            assert not exists(join(self.dest_dir, 'presentation.html'))
            assert exists(join(self.dest_dir, 'css', 'style.css'))
            assert exists(join(self.dest_dir, 'css', 'custom.css'))
            assert exists(join(self.dest_dir, 'imagens', 'tdd_cycle.png'))
            assert exists(join(self.dest_dir, 'imagens', 'logotipo.png'))
            assert not exists(join(self.dest_dir, 'imagens', 'not_used.png'))
            assert exists(join(self.dest_dir, 'css', 'slideshow.css'))
            assert exists(join(self.dest_dir, 'js'))
            assert str('href="css/custom.css"') in output
        finally:
            rmtree(other_dir)

    def test_href(self):
        try:
            from io import StringIO
        except ImportError:
            from StringIO import StringIO
        errors = StringIO()
        source = '''
    internal_ mail_ javascript_ external_ image_ abspath_

    .. _abspath: %s
    .. _internal: #id1
    .. _mail: mailto:andre.dias@pronus.io
    .. _javascript: javascript:void()
    .. _external: https://pypi.python.org/pypi/rst2html5
    .. _image: %s''' % (__file__, join('imagens', 'logotipo.png'))
        output = publish_string(
            writer=SlideWriter(), source=source,
            destination_path=join(self.dest_dir, 'hrefs.html'),
            settings_overrides={'output_encoding': 'unicode', 'warning_stream': errors}
        )
        assert not exists(join(self.dest_dir, 'imagens', 'logotipo.png'))
        assert 'file not found: imagens/logotipo.png' in errors.getvalue(), errors.getvalue()
        assert str('href="%s"' % __file__) in output
        assert str('href="#id1"') in output
        assert str('href="mailto:andre.dias@pronus.io"') in output
        assert str('href="javascript:void()"') in output
        assert str('href="https://pypi.python.org/pypi/rst2html5"') in output
        assert str('href="%s"' % join('imagens', 'logotipo.png')) in output

    def test_discover_path(self):
        '''
        rst2html5slides should find a relative path even if the rst file is included elsewhere
        '''
        other_dir = mkdtemp()
        try:
            os.chdir(other_dir)
            makedirs(join(other_dir, 'css'))
            css_filename = join(other_dir, 'css', 'custom.css')
            with open(css_filename, 'w') as f:
                f.write('a {text-decoration: none}')
            include = '''
.. stylesheet:: {css}

Include other file

.. include:: {presentation}'''.format(css=css_filename, presentation=self.source_path)
            include_filename = join(other_dir, 'include_presentation.rst')
            with open(include_filename, 'w') as f:
                f.write(include)
            output = publish_file(
                writer=SlideWriter(), source_path=include_filename,
                destination_path=join(self.dest_dir, 'slides.html'),
                settings_overrides={'output_encoding': 'unicode'}
            )
        finally:
            rmtree(other_dir)

        assert exists(join(self.dest_dir, 'slides.html'))
        assert not exists(join(self.dest_dir, 'presentation.html'))
        assert not exists(join(self.dest_dir, 'css', 'style.css'))
        assert exists(join(self.dest_dir, 'imagens', 'tdd_cycle.png'))
        assert exists(join(self.dest_dir, 'imagens', 'logotipo.png'))
        assert not exists(join(self.dest_dir, 'imagens', 'not_used.png'))
        assert exists(join(self.dest_dir, 'js'))
        assert str('href="%s"' % css_filename) in output
