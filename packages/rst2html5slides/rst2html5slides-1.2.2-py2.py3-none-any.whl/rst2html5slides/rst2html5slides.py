#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: André Felipe Dias <andref.dias@pronus.eng.br>

from __future__ import unicode_literals

import re
import sys
import docutils
import shutil
from os import makedirs
from os.path import join, dirname, basename, isfile, exists, curdir, split, splitext, abspath

from docutils import nodes
from docutils.frontend import OptionParser
from docutils.io import FileOutput
from docutils.parsers.rst.directives.html import MetaBody as Meta
from docutils.transforms import Transform
from genshi.builder import tag
from rst2html5_ import HTML5Translator, HTML5Writer

try:
    from urllib.parse import urlparse
except ImportError:  # Python 2
    from urlparse import urlparse


"""
Translates a restructuredText document into a HTML5 slideshow
"""
__version__ = '1.2.2'
__docformat__ = 'reStructuredText'


# monkeypatch OptionParser to set 'version'
OptionParser.version_template = '%%prog %s (Docutils %s%s, Python %s, on %s)' % (
    __version__, docutils.__version__,
    docutils.__version_details__ and ' [%s]' % docutils.__version_details__ or '',
    sys.version.split()[0], sys.platform
)


class slide_contents(nodes.Element):
    pass


class SlideTransform(Transform):

    '''
    State Machine to transform default doctree to one with slideshow structure:
    section, header, contents.
    '''

    default_priority = 851

    # node classes that should be ignored to not form new slides
    force_new_slide = (nodes.field_list,)
    skip_classes = (Meta.meta, nodes.docinfo) + force_new_slide

    def apply(self):
        self.contents = []
        self.header = []
        self.slides = []
        self.slide = nodes.section()
        self.inner_level = 0
        self.visit(self.document.children)
        self.document.extend(self.slides)
        return

    def visit(self, children):
        self.inner_level += 1
        while children:
            node = children.pop(0)
            if isinstance(node, self.skip_classes):
                if isinstance(node, self.force_new_slide):
                    # meta and docinfo doesn't close slide
                    # see meta_tag_and_slides in test/cases.py
                    self.close_slide()
                self.slides.append(node)
                continue
            self.parse(node)
        self.inner_level -= 1
        if self.inner_level <= 1:
            self.close_slide()
        return

    def parse(self, node):
        if isinstance(node, nodes.transition):
            self.close_slide()
            self.slide.update_all_atts(node)
        elif isinstance(node, nodes.section):
            # All subsections are flattened to the same level.
            if self.inner_level == 1:
                self.close_slide()
                self.slide.update_all_atts(node)
            self.visit(node.children)
        elif isinstance(node, (nodes.title, nodes.subtitle)):
            # Titles and subtitles are converted to nodes.title and
            # their heading levels are defined later during translation
            self.header.append(node)
        else:
            self.contents.append(node)
        return

    def close_slide(self):
        if not (self.contents or self.header):
            return
        if self.header:
            header = nodes.header()
            header.extend(self.header)
            self.slide.append(header)
            self.header = []
        if self.contents:
            contents = slide_contents()
            contents.extend(self.contents)
            self.contents = []
            self.slide.append(contents)
        self.slides.append(self.slide)
        self.slide = nodes.section()
        return


class SlideWriter(HTML5Writer):

    def __init__(self):
        HTML5Writer.__init__(self)
        self.translator_class = SlideTranslator

    def rebuild_output(self):

        def copy_file(origin, destination):
            dest_dir = dirname(destination)
            if not exists(dest_dir):
                makedirs(dest_dir)
            shutil.copy(origin, destination)

        def roundrobin(*iterables):
            """
            roundrobin('ABC', 'D', 'EF') --> A D E B F C

            see: https://docs.python.org/3.4/library/itertools.html#itertools-recipes
            """
            from itertools import cycle, islice
            pending = len(iterables)
            # small modification to run under both Python 3 and 2
            next_attr = '__next__' if hasattr(iter(iterables[0]), '__next__') else 'next'
            nexts = cycle(getattr(iter(it), next_attr) for it in iterables)
            while pending:
                try:
                    for next in nexts:
                        yield next()
                except StopIteration:
                    pending -= 1
                    nexts = cycle(islice(nexts, pending))

        output = self.output
        href_pattern = re.compile('href="[^#].*?"|src=".*?"')
        path_pattern = re.compile(r'"(.*?)([#|\?].*?)?"')   # e.g. "mercurial.svg#logo"
        hrefs = re.findall(href_pattern, output)
        save_to_destination = self.destination.destination_path not in ('<stdout>', '<string>')
        dest_dir = dirname(self.destination.destination_path)
        for i, href in enumerate(hrefs):
            path, fragment = re.findall(path_pattern, href)[0]
            parsed_url = urlparse(path)
            if parsed_url.scheme or parsed_url.netloc or parsed_url.path.startswith('/'):
                # not a local reference or it is an absolute path
                continue
            href_path = re.findall(r'^(?:\.+/)*(.*)', path)[0]
            hrefs[i] = re.sub('".*?"', '"%s%s"' % (href_path, fragment), href)
            if save_to_destination:
                # search for possible paths where reference could be
                possible_paths = set()
                for dependency in self.document.settings.record_dependencies.list:
                    possible_paths.add(abspath(join(dirname(dependency), path)))
                if self.document.settings._source:
                    source_dir = dirname(self.document.settings._source)
                    possible_paths.add(abspath(join(source_dir, path)))
                    possible_paths.add(abspath(join(curdir, path)))
                possible_paths.add(abspath(join(dirname(self.document.settings.template), path)))
                source_path = None
                for search_path in possible_paths:
                    if isfile(search_path):
                        source_path = search_path
                        break
                if not source_path:
                    self.document.reporter.error('file not found: %s' % path)
                    continue
                copy_file(source_path, join(dest_dir, href_path))
        # rebuild output references
        splitted = re.split(href_pattern, output)
        self.output = ''.join(roundrobin(splitted, hrefs))
        return

    def translate(self):
        destination_path = self.destination.destination_path
        if destination_path not in ('<stdout>', '<string>'):  # there is a specified destination
            dest_dir, extension = splitext(destination_path)
            if extension:  # there is a filename in the destination
                dest_dir, dest_filename = split(destination_path)
            else:  # The specified destination is a directory. A new filename is necessary
                dest_filename = splitext(basename(self.document.settings._source))[0] + '.html'
            self.destination = FileOutput(destination_path=join(dest_dir, dest_filename),
                                          encoding='utf-8')
        HTML5Writer.translate(self)
        self.rebuild_output()
        return

    def get_transforms(self):
        return HTML5Writer.get_transforms(self) + [SlideTransform]


class SlideTranslator(HTML5Translator):

    tag_name_re = re.compile(r'^\w+')
    class_re = re.compile(r'\.([\w\-]+)')
    id_re = re.compile(r'#([\w|\-]+)')

    def __init__(self, *args):
        self.rst_terms['section'] = ['slide', 'visit_section', 'depart_section']  # [0] might be replaced later
        self.rst_terms['slide_contents'] = ('section', 'default_visit', 'default_departure')
        self.rst_terms['title'] = (None, 'visit_title', 'depart_title')  # flatten titles
        HTML5Translator.__init__(self, *args)
        self.metatags.append(tag.meta(generator='rst2html5slides'))
        self.metatags.append(tag.meta(generator_homepage='https://pypi.python.org/pypi/rst2html5slides'))
        self._reset_settings()
        return

    def _compacted_paragraph(self, node):
        '''
        a single node followed by a single field list should also be compacted
        '''
        field_list_sibling = len([n for n in node.parent
                                  if not isinstance(n, (nodes.field_list))]) == 1
        return not node['classes'] and \
            (HTML5Translator._compacted_paragraph(self, node) or field_list_sibling)

    def visit_section(self, node):
        if 'id' in self.slide_attributes:
            node['ids'] = [self.slide_attributes['id']]
        node.attributes.update(self.slide_attributes)
        self.slide_attributes = {}
        self.default_visit(node)
        return

    def depart_section(self, node):
        self.heading_level = 0  # a new section reset title level
        self.default_departure(node)
        return

    def visit_title(self, node):
        '''
        In rst2html5slides, subsections are flattened and every title node is grouped
        inside the same header as a nodes.title.
        According to their position, the title node should become h1, h2, h3 etc.

        Example:

        <header>
            <title 1>
            <title 2>
            <title 3>

        becomes:

        <header>
            <h1>Title 1</h1>
            <h2>Subtitle</h2>
            <h3>Subsubtitle</h3>

        see test/cases.py  h2 and h3
        '''
        self.default_visit(node)
        self.heading_level += 1
        return

    def depart_document(self, node):
        if len(self.context.stack[0]):
            deck = tag.deck(*self.context.stack[0])
            self.context.stack = ['\n', deck, '\n']
        # _reset is necessary to run the several test cases
        self._reset_settings()
        return

    def visit_field(self, node):
        field_name = node.children[0].astext()
        field_value = self._strip_spaces(node.children[1].astext())
        visit_field_func = getattr(self, 'visit_field_' + field_name.replace('-', '_'), None)
        if visit_field_func:
            visit_field_func(field_value)
        else:
            self.slide_attributes[field_name] = field_value
        raise nodes.SkipNode

    def visit_field_class(self, value):
        self.slide_attributes['classes'] = value.split()
        return

    def visit_field_classes(self, value):
        self.visit_field_class(value)
        return

    def _reset_settings(self):
        self.slide_attributes = {}
        settings = self.document.settings
        template = 'default.html'
        settings.template = settings.template or abspath(join(dirname(__file__), curdir, 'template', template))
        return


def main():
    from docutils.core import publish_cmdline, default_description
    description = ('Translates a restructuredText document to a HTML5 slideshow.  ' +
                   default_description)
    publish_cmdline(writer=SlideWriter(), description=description)
    return


if __name__ == '__main__':
    main()
