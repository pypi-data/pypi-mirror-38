import os
import time
import pytest
from rhcephcompose.compose import Compose
from kobo.conf import PyConfigParser
import py.path


@pytest.fixture
def conf(fixtures_dir):
    conf_file = os.path.join(fixtures_dir, 'basic.conf')
    conf = PyConfigParser()
    conf.load_from_file(conf_file)
    return conf


class TestCompose(object):

    def test_constructor(self, conf):
        c = Compose(conf)
        assert isinstance(c, Compose)
        assert c.target == 'trees'

    @pytest.mark.parametrize(('compose_type', 'suffix'), [
        ('production', ''),
        ('nightly', '.n'),
        ('test', '.t'),
        ('ci', '.ci'),
    ])
    def test_output_dir(self, conf, tmpdir, monkeypatch, compose_type, suffix):
        monkeypatch.chdir(tmpdir)
        conf['compose_type'] = compose_type
        c = Compose(conf)
        compose_date = time.strftime('%Y%m%d')
        expected = 'trees/RHCEPH-2.0-Ubuntu-x86_64-{0}{1}.0'.format(
            compose_date, suffix)
        assert c.output_dir == expected

    @pytest.mark.parametrize(('release_version', 'expected'), [
        ('2', 'RHCEPH-2-Ubuntu-x86_64-latest'),
        ('2.0', 'RHCEPH-2-Ubuntu-x86_64-latest'),
        ('2.0.0', 'RHCEPH-2.0-Ubuntu-x86_64-latest'),
    ])
    def test_latest_name(self, conf, release_version, expected):
        conf['release_version'] = release_version
        c = Compose(conf)
        assert c.latest_name == expected

    def test_symlink_latest(self, conf, tmpdir, monkeypatch):
        monkeypatch.chdir(tmpdir)
        c = Compose(conf)
        os.makedirs(c.output_dir)
        c.symlink_latest()
        result = os.path.realpath('trees/RHCEPH-2-Ubuntu-x86_64-latest')
        assert result == os.path.realpath(c.output_dir)

    def test_create_repo(self, conf, tmpdir, monkeypatch):
        monkeypatch.chdir(tmpdir)
        c = Compose(conf)
        # TODO: use real list of binaries here
        c.create_repo(str(tmpdir), 'xenial', [])
        distributions_path = tmpdir.join('conf/distributions')
        assert distributions_path.check(file=True)

        expected = '''\
Codename: xenial
Suite: stable
Components: main
Architectures: amd64 i386
Origin: Red Hat, Inc.
Description: Ceph distributed file system
DebIndices: Packages Release . .gz .bz2
DscIndices: Sources Release .gz .bz2
Contents: .gz .bz2

'''
        assert distributions_path.read() == expected


class TestComposeValidate(object):

    @pytest.fixture
    def tmp_fixtures_dir(self, fixtures_dir, tmpdir):
        """ Copy our fixture files to a tmpdir for modification. """
        orig = py.path.local(fixtures_dir)
        orig.copy(tmpdir)
        return tmpdir

    def test_ok(self, tmp_fixtures_dir, conf, monkeypatch):
        monkeypatch.chdir(tmp_fixtures_dir)
        c = Compose(conf)
        # validate() should not raise RuntimeError here.
        c.validate()

    def test_no_builds(self, tmp_fixtures_dir, conf, monkeypatch):
        monkeypatch.chdir(tmp_fixtures_dir)
        c = Compose(conf)
        c.builds = {}
        with pytest.raises(RuntimeError):
            c.validate()

    def test_missing_builds_file(self, tmp_fixtures_dir, conf, monkeypatch):
        monkeypatch.chdir(tmp_fixtures_dir)
        c = Compose(conf)
        tmp_fixtures_dir.remove(c.builds['trusty'])
        with pytest.raises(RuntimeError):
            c.validate()

    def test_missing_comps_file(self, tmp_fixtures_dir, conf, monkeypatch):
        monkeypatch.chdir(tmp_fixtures_dir)
        c = Compose(conf)
        tmp_fixtures_dir.remove(c.comps['trusty'])
        with pytest.raises(RuntimeError):
            c.validate()

    def test_missing_variants_file(self, tmp_fixtures_dir, conf, monkeypatch):
        monkeypatch.chdir(tmp_fixtures_dir)
        c = Compose(conf)
        tmp_fixtures_dir.remove(c.variants_file)
        with pytest.raises(RuntimeError):
            c.validate()

    def test_missing_extra_file(self, tmp_fixtures_dir, conf, monkeypatch):
        monkeypatch.chdir(tmp_fixtures_dir)
        c = Compose(conf)
        extra_file = os.path.join('extra_files', c.extra_files[0]['file'])
        tmp_fixtures_dir.remove(extra_file)
        with pytest.raises(RuntimeError):
            c.validate()

    def test_wrong_dist(self, tmp_fixtures_dir, conf, monkeypatch):
        monkeypatch.chdir(tmp_fixtures_dir)
        c = Compose(conf)
        # Re-assign our "xenial" builds list so it will contain an (incorrect)
        # build with "trusty" in the Name-Version-Release.
        c.builds['xenial'] = c.builds['trusty']
        with pytest.raises(RuntimeError):
            c.validate()


class TestComposeReleaseVersion(object):

    def test_product_version_fallback(self, conf, tmpdir, monkeypatch):
        monkeypatch.chdir(tmpdir)
        del conf['release_version']
        conf['product_version'] = '3'
        c = Compose(conf)
        assert c.release_version == '3'


class TestComposeReleaseShort(object):

    @pytest.fixture
    def newconf(self, conf):
        conf['release_short'] = 'FOOPRODUCT'
        return conf

    def test_output_dir(self, newconf, tmpdir, monkeypatch):
        monkeypatch.chdir(tmpdir)
        c = Compose(newconf)
        compose_date = time.strftime('%Y%m%d')
        expected = 'trees/FOOPRODUCT-2.0-Ubuntu-x86_64-%s.t.0' % compose_date
        assert c.output_dir == expected

    def test_symlink_latest(self, newconf, tmpdir, monkeypatch):
        monkeypatch.chdir(tmpdir)
        c = Compose(newconf)
        os.makedirs(c.output_dir)
        c.symlink_latest()
        result = os.path.realpath('trees/FOOPRODUCT-2-Ubuntu-x86_64-latest')
        assert result == os.path.realpath(c.output_dir)
