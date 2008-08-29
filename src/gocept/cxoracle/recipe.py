# Copyright (c) 2008 gocept gmbh & co. kg
# See also LICENSE.txt

import re
import os
import os.path
import shutil
import subprocess
import tempfile


class CxOracle(object):

    client_library_pattern = re.compile(
        r'^(libclntsh)\.([[a-z]+)\.([\d.]+)$')

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.part_directory = os.path.join(
            buildout['buildout']['parts-directory'],
            name)

    def install(self):
        if os.path.isdir(self.part_directory):
            shutil.rmtree(self.part_directory)
        os.mkdir(self.part_directory)
        self.prepare_oracle_home()
        return self.part_directory

    def prepare_oracle_home(self):
        self.unzip(self.options['instant-client'])
        self.unzip(self.options['instant-sdk'])

        symlink_source = None
        for filename in os.listdir(self.part_directory):
            m = self.client_library_pattern.match(filename)
            if m is not None:
                library_base_name = m.group(2)
                library_kind = m.group(2)
                version = m.group(3)
                symlink_source = filename
                break
        if symlink_source is None:
            raise Exception('Could not find libclntsh.')

        symlink_target = '%s.%s' % (library_base_name, library_kind)
        os.symlink(os.path.join(self.part_directory, symlink_source),
                   os.path.join(self.part_directory, symlink_target))

    def unzip(self, filename):
        extract_dir = tempfile.mkdtemp()
        try:

            call = ['unzip', filename, '-d', extract_dir]
            retcode = subprocess.call(call)
            if retcode != 0:
                raise Exception('Extraction of file %r failed' % extract_dir)

            contents = os.listdir(extract_dir)
            assert len(contents) == 1
            root = os.path.join(extract_dir, contents[0])
            for filename in os.listdir(root):
                shutil.move(os.path.join(root, filename),
                            os.path.join(self.part_directory, filename))
        finally:
            shutil.rmtree(extract_dir)
