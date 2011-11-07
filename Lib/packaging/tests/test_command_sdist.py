"""Tests for packaging.command.sdist."""
import os
import tarfile
import zipfile

try:
    import grp
    import pwd
    UID_GID_SUPPORT = True
except ImportError:
    UID_GID_SUPPORT = False

from shutil import get_archive_formats
from os.path import join
from packaging.dist import Distribution
from packaging.util import find_executable
from packaging.errors import PackagingOptionError
from packaging.command.sdist import sdist, show_formats

from packaging.tests import support, unittest
from packaging.tests import captured_stdout
from packaging.tests.support import requires_zlib


MANIFEST = """\
# file GENERATED by packaging, do NOT edit
inroot.txt
setup.cfg
data%(sep)sdata.dt
scripts%(sep)sscript.py
some%(sep)sfile.txt
some%(sep)sother_file.txt
somecode%(sep)s__init__.py
somecode%(sep)sdoc.dat
somecode%(sep)sdoc.txt
"""


def builder(dist, filelist):
    filelist.append('bah')


class SDistTestCase(support.TempdirManager,
                    support.LoggingCatcher,
                    support.EnvironRestorer,
                    unittest.TestCase):

    restore_environ = ['HOME']

    def setUp(self):
        super(SDistTestCase, self).setUp()
        self.tmp_dir = self.mkdtemp()
        os.environ['HOME'] = self.tmp_dir
        # setting up an environment
        self.old_path = os.getcwd()
        os.mkdir(join(self.tmp_dir, 'somecode'))
        os.mkdir(join(self.tmp_dir, 'dist'))
        # a package, and a README
        self.write_file((self.tmp_dir, 'README'), 'xxx')
        self.write_file((self.tmp_dir, 'somecode', '__init__.py'), '#')
        os.chdir(self.tmp_dir)

    def tearDown(self):
        # back to normal
        os.chdir(self.old_path)
        super(SDistTestCase, self).tearDown()

    def get_cmd(self, metadata=None):
        """Returns a cmd"""
        if metadata is None:
            metadata = {'name': 'fake', 'version': '1.0',
                        'home_page': 'xxx', 'author': 'xxx',
                        'author_email': 'xxx'}
        dist = Distribution(metadata)
        dist.packages = ['somecode']
        dist.include_package_data = True
        cmd = sdist(dist)
        cmd.dist_dir = 'dist'
        return dist, cmd

    @requires_zlib
    def test_prune_file_list(self):
        # this test creates a package with some vcs dirs in it
        # and launch sdist to make sure they get pruned
        # on all systems

        # creating VCS directories with some files in them
        os.mkdir(join(self.tmp_dir, 'somecode', '.svn'))
        self.write_file((self.tmp_dir, 'somecode', '.svn', 'ok.py'), 'xxx')

        os.mkdir(join(self.tmp_dir, 'somecode', '.hg'))
        self.write_file((self.tmp_dir, 'somecode', '.hg',
                         'ok'), 'xxx')

        os.mkdir(join(self.tmp_dir, 'somecode', '.git'))
        self.write_file((self.tmp_dir, 'somecode', '.git',
                         'ok'), 'xxx')

        # now building a sdist
        dist, cmd = self.get_cmd()

        # zip is available universally
        # (tar might not be installed under win32)
        cmd.formats = ['zip']

        cmd.ensure_finalized()
        cmd.run()

        # now let's check what we have
        dist_folder = join(self.tmp_dir, 'dist')
        files = os.listdir(dist_folder)
        self.assertEqual(files, ['fake-1.0.zip'])

        with zipfile.ZipFile(join(dist_folder, 'fake-1.0.zip')) as zip_file:
            content = zip_file.namelist()

        # making sure everything has been pruned correctly
        self.assertEqual(len(content), 2)

    @requires_zlib
    @unittest.skipIf(find_executable('tar') is None or
                     find_executable('gzip') is None,
                     'requires tar and gzip programs')
    def test_make_distribution(self):
        # building a sdist
        dist, cmd = self.get_cmd()

        # creating a gztar then a tar
        cmd.formats = ['gztar', 'tar']
        cmd.ensure_finalized()
        cmd.run()

        # making sure we have two files
        dist_folder = join(self.tmp_dir, 'dist')
        result = sorted(os.listdir(dist_folder))
        self.assertEqual(result, ['fake-1.0.tar', 'fake-1.0.tar.gz'])

        os.remove(join(dist_folder, 'fake-1.0.tar'))
        os.remove(join(dist_folder, 'fake-1.0.tar.gz'))

        # now trying a tar then a gztar
        cmd.formats = ['tar', 'gztar']
        cmd.finalized = False
        cmd.ensure_finalized()
        cmd.run()

        result = sorted(os.listdir(dist_folder))
        self.assertEqual(result, ['fake-1.0.tar', 'fake-1.0.tar.gz'])

    @requires_zlib
    def test_add_defaults(self):

        # http://bugs.python.org/issue2279

        # add_default should also include
        # data_files and package_data
        dist, cmd = self.get_cmd()

        # filling data_files by pointing files
        # in package_data
        dist.package_data = {'': ['*.cfg', '*.dat'],
                             'somecode': ['*.txt']}
        self.write_file((self.tmp_dir, 'setup.cfg'), '#')
        self.write_file((self.tmp_dir, 'somecode', 'doc.txt'), '#')
        self.write_file((self.tmp_dir, 'somecode', 'doc.dat'), '#')

        # adding some data in data_files
        data_dir = join(self.tmp_dir, 'data')
        os.mkdir(data_dir)
        self.write_file((data_dir, 'data.dt'), '#')
        some_dir = join(self.tmp_dir, 'some')
        os.mkdir(some_dir)
        self.write_file((self.tmp_dir, 'inroot.txt'), '#')
        self.write_file((some_dir, 'file.txt'), '#')
        self.write_file((some_dir, 'other_file.txt'), '#')

        dist.data_files = {'data/data.dt': '{appdata}/data.dt',
                           'inroot.txt': '{appdata}/inroot.txt',
                           'some/file.txt': '{appdata}/file.txt',
                           'some/other_file.txt': '{appdata}/other_file.txt'}

        # adding a script
        script_dir = join(self.tmp_dir, 'scripts')
        os.mkdir(script_dir)
        self.write_file((script_dir, 'script.py'), '#')
        dist.scripts = [join('scripts', 'script.py')]

        cmd.formats = ['zip']
        cmd.use_defaults = True

        cmd.ensure_finalized()
        cmd.run()

        # now let's check what we have
        dist_folder = join(self.tmp_dir, 'dist')
        files = os.listdir(dist_folder)
        self.assertEqual(files, ['fake-1.0.zip'])

        with zipfile.ZipFile(join(dist_folder, 'fake-1.0.zip')) as zip_file:
            content = zip_file.namelist()

        # Making sure everything was added. This includes 8 code and data
        # files in addition to PKG-INFO and setup.cfg
        self.assertEqual(len(content), 10)

        # Checking the MANIFEST
        with open(join(self.tmp_dir, 'MANIFEST')) as fp:
            manifest = fp.read()
        self.assertEqual(manifest, MANIFEST % {'sep': os.sep})

    @requires_zlib
    def test_metadata_check_option(self):
        # testing the `check-metadata` option
        dist, cmd = self.get_cmd(metadata={'name': 'xxx', 'version': 'xxx'})

        # this should cause the check subcommand to log two warnings:
        # version is invalid, home-page and author are missing
        cmd.ensure_finalized()
        cmd.run()
        warnings = self.get_logs()
        check_warnings = [msg for msg in warnings if
                          not msg.startswith('sdist:')]
        self.assertEqual(len(check_warnings), 2, warnings)

        # trying with a complete set of metadata
        self.loghandler.flush()
        dist, cmd = self.get_cmd()
        cmd.ensure_finalized()
        cmd.metadata_check = False
        cmd.run()
        warnings = self.get_logs()
        self.assertEqual(len(warnings), 2)
        self.assertIn('using default file list', warnings[0])
        self.assertIn("'setup.cfg' file not found", warnings[1])

    def test_show_formats(self):
        __, stdout = captured_stdout(show_formats)

        # the output should be a header line + one line per format
        num_formats = len(get_archive_formats())
        output = [line for line in stdout.split('\n')
                  if line.strip().startswith('--formats=')]
        self.assertEqual(len(output), num_formats)

    def test_finalize_options(self):
        dist, cmd = self.get_cmd()
        cmd.finalize_options()

        # default options set by finalize
        self.assertEqual(cmd.manifest, 'MANIFEST')
        self.assertEqual(cmd.dist_dir, 'dist')

        # formats has to be a string splitable on (' ', ',') or
        # a stringlist
        cmd.formats = 1
        self.assertRaises(PackagingOptionError, cmd.finalize_options)
        cmd.formats = ['zip']
        cmd.finalize_options()

        # formats has to be known
        cmd.formats = 'supazipa'
        self.assertRaises(PackagingOptionError, cmd.finalize_options)

    @requires_zlib
    def test_template(self):
        dist, cmd = self.get_cmd()
        dist.extra_files = ['include yeah']
        cmd.ensure_finalized()
        self.write_file((self.tmp_dir, 'yeah'), 'xxx')
        cmd.run()
        with open(cmd.manifest) as f:
            content = f.read()

        self.assertIn('yeah', content)

    @requires_zlib
    @unittest.skipUnless(UID_GID_SUPPORT, "requires grp and pwd support")
    @unittest.skipIf(find_executable('tar') is None or
                     find_executable('gzip') is None,
                     'requires tar and gzip programs')
    def test_make_distribution_owner_group(self):
        # building a sdist
        dist, cmd = self.get_cmd()

        # creating a gztar and specifying the owner+group
        cmd.formats = ['gztar']
        cmd.owner = pwd.getpwuid(0)[0]
        cmd.group = grp.getgrgid(0)[0]
        cmd.ensure_finalized()
        cmd.run()

        # making sure we have the good rights
        archive_name = join(self.tmp_dir, 'dist', 'fake-1.0.tar.gz')
        with tarfile.open(archive_name) as archive:
            for member in archive.getmembers():
                self.assertEqual(member.uid, 0)
                self.assertEqual(member.gid, 0)

        # building a sdist again
        dist, cmd = self.get_cmd()

        # creating a gztar
        cmd.formats = ['gztar']
        cmd.ensure_finalized()
        cmd.run()

        # making sure we have the good rights
        archive_name = join(self.tmp_dir, 'dist', 'fake-1.0.tar.gz')
        with tarfile.open(archive_name) as archive:

            # note that we are not testing the group ownership here
            # because, depending on the platforms and the container
            # rights (see #7408)
            for member in archive.getmembers():
                self.assertEqual(member.uid, os.getuid())

    @requires_zlib
    def test_get_file_list(self):
        # make sure MANIFEST is recalculated
        dist, cmd = self.get_cmd()
        # filling data_files by pointing files in package_data
        dist.package_data = {'somecode': ['*.txt']}
        self.write_file((self.tmp_dir, 'somecode', 'doc.txt'), '#')
        cmd.ensure_finalized()
        cmd.run()

        # Should produce four lines. Those lines are one comment, one default
        # (README) and two package files.
        with open(cmd.manifest) as f:
            manifest = [line.strip() for line in f.read().split('\n')
                        if line.strip() != '']
        self.assertEqual(len(manifest), 3)

        # Adding a file
        self.write_file((self.tmp_dir, 'somecode', 'doc2.txt'), '#')

        # make sure build_py is reinitialized, like a fresh run
        build_py = dist.get_command_obj('build_py')
        build_py.finalized = False
        build_py.ensure_finalized()

        cmd.run()

        with open(cmd.manifest) as f:
            manifest2 = [line.strip() for line in f.read().split('\n')
                         if line.strip() != '']

        # Do we have the new file in MANIFEST?
        self.assertEqual(len(manifest2), 4)
        self.assertIn('doc2.txt', manifest2[-1])

    @requires_zlib
    def test_manifest_marker(self):
        # check that autogenerated MANIFESTs have a marker
        dist, cmd = self.get_cmd()
        cmd.ensure_finalized()
        cmd.run()

        with open(cmd.manifest) as f:
            manifest = [line.strip() for line in f.read().split('\n')
                        if line.strip() != '']

        self.assertEqual(manifest[0],
                         '# file GENERATED by packaging, do NOT edit')

    @requires_zlib
    def test_manual_manifest(self):
        # check that a MANIFEST without a marker is left alone
        dist, cmd = self.get_cmd()
        cmd.ensure_finalized()
        self.write_file((self.tmp_dir, cmd.manifest), 'README.manual')
        cmd.run()

        with open(cmd.manifest) as f:
            manifest = [line.strip() for line in f.read().split('\n')
                        if line.strip() != '']

        self.assertEqual(manifest, ['README.manual'])

    @requires_zlib
    def test_manifest_builder(self):
        dist, cmd = self.get_cmd()
        cmd.manifest_builders = 'packaging.tests.test_command_sdist.builder'
        cmd.ensure_finalized()
        cmd.run()
        self.assertIn('bah', cmd.filelist.files)


def test_suite():
    return unittest.makeSuite(SDistTestCase)

if __name__ == "__main__":
    unittest.main(defaultTest="test_suite")
