# -*- coding: utf-8 -*-
#
# Copyright © 2015,2016 Mathieu Duponchelle <mathieu.duponchelle@opencreed.com>
# Copyright © 2015,2016 Collabora Ltd
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

"""
Core of the core.
"""
import os
import io
import re
import linecache
import shutil

from collections import OrderedDict

from hotdoc.core import inclusions
from hotdoc.core.extension import Extension
from hotdoc.core.comment import Tag
from hotdoc.core.config import Config
from hotdoc.core.tree import Tree, PageResolutionResult
from hotdoc.utils.loggable import info, error
from hotdoc.utils.configurable import Configurable
from hotdoc.utils.utils import OrderedSet
from hotdoc.utils.signals import Signal
from hotdoc.parsers.sitemap import SitemapParser


LANG_MAPPING = {
    'js': 'javascript',
    'xml': 'markup',
    'html': 'markup',
    'py': 'python'
}


class CoreExtension(Extension):
    """
    Banana banana
    """
    extension_name = 'core'

    def format_page(self, page, link_resolver, output):
        proj = self.project.subprojects.get(page.source_file)
        if proj:
            proj.format(link_resolver, output)
            page.title = proj.tree.root.title
        else:
            super(CoreExtension, self).format_page(
                page, link_resolver, output)

    def write_out_page(self, output, page):
        proj = self.project.subprojects.get(page.source_file)
        if proj:
            proj.tree.write_out(output)
        else:
            super(CoreExtension, self).write_out_page(
                output, page)

    def setup(self):
        super(CoreExtension, self).setup()
        inclusions.include_signal.disconnect(CoreExtension.include_file_cb)
        inclusions.include_signal.connect_after(CoreExtension.include_file_cb)

    def _resolve_placeholder(self, tree, name, include_paths):
        ext = os.path.splitext(name)[1]
        if ext != '.json':
            return None

        conf_path = inclusions.find_file(name, include_paths)
        if not conf_path:
            error('invalid-config',
                  '(%s) Could not find subproject config file %s' % (
                      self.project.sanitized_name, name))

        self.project.add_subproject(name, conf_path)
        return PageResolutionResult(True, None, None, None)

    @staticmethod
    def include_file_cb(include_path, line_ranges, symbol):
        """
        Banana banana
        """
        lang = ''
        if include_path.endswith((".md", ".markdown")):
            lang = 'markdown'
        else:
            split = os.path.splitext(include_path)
            if len(split) == 2:
                ext = split[1].strip('.')
                lang = LANG_MAPPING.get(ext) or ext

        if line_ranges:
            res = []
            for line_range in line_ranges:
                for lineno in range(line_range[0] + 1, line_range[1] + 1):
                    line = linecache.getline(include_path, lineno)
                    if not line:
                        return None
                    res.append(line)
            return ''.join(res), lang

        with io.open(include_path, 'r', encoding='utf-8') as _:
            return _.read(), lang


# pylint: disable=too-many-instance-attributes
class Project(Configurable):
    """
    Banana banana
    """

    def __init__(self, app, dependency_map=None, page_map=None):
        self.app = app
        self.tree = None
        self.include_paths = None
        self.extensions = OrderedDict()
        self.tag_validators = {}
        self.project_name = None
        self.project_version = None
        self.sanitized_name = None
        self.sitemap_path = None
        self.subprojects = {}
        self.extra_asset_folders = OrderedSet()
        self.extra_assets = {}

        if dependency_map is None:
            self.dependency_map = {}
        else:
            self.dependency_map = dependency_map

        if page_map is None:
            self.page_map = {}
        else:
            self.page_map = page_map

        if os.name == 'nt':
            self.datadir = os.path.join(
                os.path.dirname(__file__), '..', 'share')
        else:
            self.datadir = "/usr/share"

        self.formatted_signal = Signal()
        self.written_out_signal = Signal()

        self.is_toplevel = False

    def register_tag_validator(self, validator):
        """
        Banana banana
        """
        self.tag_validators[validator.name] = validator

    def persist(self):
        """
        Banana banana
        """

        if self.app.dry:
            return

        self.tree.persist()
        for proj in self.subprojects.values():
            proj.persist()

    def finalize(self):
        """
        Banana banana
        """
        self.formatted_signal.clear()

    # pylint: disable=no-self-use
    def get_private_folder(self):
        """
        Banana banana
        """
        return self.app.private_folder

    def setup(self):
        """
        Banana banana
        """
        info('Setting up %s' % self.project_name, 'project')

        self.app.database.comment_updated_signal.connect(
            self.__comment_updated_cb)
        for extension in list(self.extensions.values()):
            info('Setting up %s' % extension.extension_name)
            extension.setup()
        self.app.database.comment_updated_signal.disconnect(
            self.__comment_updated_cb)

        sitemap = SitemapParser().parse(self.sitemap_path)
        self.tree.parse_sitemap(sitemap)
        self.page_map.update({p: self for p in self.tree.get_pages().values()})

        info("Resolving symbols", 'resolution')
        self.tree.resolve_symbols(self.app.database, self.app.link_resolver)

    def format(self, link_resolver, output):
        """
        Banana banana
        """
        if not output:
            return

        self.tree.format(link_resolver, output, self.extensions)
        self.formatted_signal(self)

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group(
            'Project', 'project-related options')
        group.add_argument("--project-name", action="store",
                           dest="project_name",
                           help="Name of the documented project")
        group.add_argument("--project-version", action="store",
                           dest="project_version",
                           help="Version of the documented project")
        group.add_argument("-i", "--index", action="store",
                           dest="index", help="location of the "
                           "index file")
        group.add_argument("--sitemap", action="store",
                           dest="sitemap",
                           help="Location of the sitemap file")
        group.add_argument('--include-paths', nargs="+",
                           help='paths to look up included files in',
                           dest='include_paths', action='append',
                           default=[])
        group.add_argument(
            "--extra-assets",
            help="Extra asset folders to copy in the output",
            action='append', dest='extra_assets', default=[])

    def add_subproject(self, fname, conf_path):
        """Creates and adds a new subproject."""
        config = Config(conf_file=conf_path)
        proj = Project(self.app,
                       dependency_map=self.dependency_map,
                       page_map=self.page_map)
        proj.parse_name_from_config(config)
        proj.parse_config(config)
        proj.setup()
        self.subprojects[fname] = proj

    def get_page_for_symbol(self, unique_name):
        """
        Banana banana
        """
        return self.dependency_map.get(unique_name)

    def get_project_for_page(self, page):
        """
        Banana banana
        """
        return self.page_map.get(page)

    def __create_extensions(self):
        for ext_class in list(self.app.extension_classes.values()):
            ext = ext_class(self.app, self)
            self.extensions[ext.extension_name] = ext

    def __comment_updated_cb(self, doc_db, comment):
        self.tree.stale_comment_pages(comment)

    def parse_name_from_config(self, config):
        """
        Banana banana
        """
        self.project_name = config.get('project_name', None)
        if not self.project_name:
            error('invalid-config', 'No project name was provided')

        self.project_version = config.get('project_version', None)
        if not self.project_version:
            error('invalid-config', 'No project version was provided')

        self.sanitized_name = '%s-%s' % (re.sub(r'\W+', '-',
                                                self.project_name),
                                         self.project_version)

    # pylint: disable=arguments-differ
    def parse_config(self, config, toplevel=False):
        """Parses @config setting up @self state."""
        self.sitemap_path = config.get_path('sitemap')

        if self.sitemap_path is None:
            error('invalid-config',
                  'No sitemap was provided')

        self.include_paths = OrderedSet([])

        index_file = config.get_index()
        if index_file:
            if not os.path.exists(index_file):
                error('invalid-config',
                      'The provided index "%s" does not exist' %
                      index_file)
            self.include_paths |= OrderedSet([os.path.dirname(index_file)])

        self.include_paths |= OrderedSet(config.get_paths('include_paths'))

        self.is_toplevel = toplevel

        self.tree = Tree(self, self.app)

        self.__create_extensions()

        for extension in list(self.extensions.values()):
            if toplevel:
                extension.parse_toplevel_config(config)
            extension.parse_config(config)

        if not toplevel and config.conf_file:
            self.app.change_tracker.add_hard_dependency(config.conf_file)

        self.extra_asset_folders = OrderedSet(config.get_paths('extra_assets'))

    def __add_default_tags(self, _, comment):
        for validator in list(self.tag_validators.values()):
            if validator.default and validator.name not in comment.tags:
                comment.tags[validator.name] = \
                    Tag(name=validator.name,
                        description=validator.default)

    def __get_formatter(self, extension_name):
        """
        Banana banana
        """
        ext = self.extensions.get(extension_name)
        if ext:
            return ext.formatter
        return None

    def write_extra_assets(self, output):
        for dest, src in self.extra_assets.items():
            dest = os.path.join(output, 'html', dest)
            destdir = os.path.dirname(dest)
            if not os.path.exists(destdir):
                os.makedirs(destdir)
            shutil.copyfile(src, dest)

        for proj in self.subprojects.values():
            proj.write_extra_assets(output)

    def write_out(self, output):
        """Banana banana
        """
        ext = self.extensions.get(self.tree.root.extension_name)

        self.tree.write_out(output)

        self.write_extra_assets(output)
        ext.formatter.copy_assets(os.path.join(output, 'html', 'assets'))

        # Just in case the sitemap root isn't named index
        ext_folder = ext.formatter.get_output_folder(self.tree.root)
        ref, _ = self.tree.root.link.get_link(self.app.link_resolver)
        index_path = os.path.join(ext_folder, ref)

        default_index_path = os.path.join(output, 'html', 'index.html')

        if not os.path.exists(default_index_path):
            with open(default_index_path, 'w', encoding='utf8') as _:
                _.write('<meta http-equiv="refresh" content="0; url=%s"/>' %
                        index_path)

        self.written_out_signal(self)
