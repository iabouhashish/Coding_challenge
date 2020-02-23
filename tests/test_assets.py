import pytest
import os
from lookup import Assets


def create_users_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "users.json"
    content = "[{\"id\": 1, \"name\": \"Foo\",\"tags\": [\"a\", \"b\"]}]"
    p.write_text(content)
    assert p.read_text() == content
    assert len(list(d.iterdir())) == 1


def create_jobs_file(tmp_path):
    d = tmp_path / "sub"
    p = d / "jobs.json"
    content = "[{\"id\": 1,\"title\": \"Foo developer\", \"company\": \"Bar industries\",\"tags\": [\"a\", \"b\", " \
              "\"c\"]}]"
    p.write_text(content)
    assert p.read_text() == content
    assert len(list(d.iterdir())) == 2


def delete_files(tmpdir):
    p = tmpdir.remove()


@pytest.fixture
def asset():
    return Assets()


class TestAssets:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """ setup any state tied to the execution of the given function.
        Invoked for every test function in the module.
        """
        create_users_file(tmp_path)
        create_jobs_file(tmp_path)

    def test_update_users(self, tmpdir, asset):
        users_json = tmpdir + "\\sub\\users.json"
        asset.create_tables()
        asset.update_users(users_json)
        assert len(asset.users) == 1

    def test_users(self, tmpdir, asset):
        users_json = tmpdir + "\\sub\\users.json"
        asset.update_users(users_json)
        assert asset.users[0] == 1

    def test_print_users(self, tmpdir, asset, capsys):
        users_json = tmpdir + "\\sub\\users.json"
        asset.update_users(users_json)
        asset.print_users()
        captured = capsys.readouterr()
        assert captured.out == "{'id': 1, 'name': 'Foo'}\n"

    def test_update_jobs(self, tmpdir, asset):
        jobs_json = tmpdir + "\\sub\\jobs.json"
        asset.create_tables()
        asset.update_jobs(jobs_json)
        assert len(asset.jobs) == 1

    def test_jobs(self, tmpdir, asset):
        jobs_json = tmpdir + "\\sub\\jobs.json"
        asset.update_jobs(jobs_json)
        assert asset.jobs[0] == 1

    def test_print_jobs(self, tmpdir, asset, capsys):
        jobs_json = tmpdir + "\\sub\\jobs.json"
        asset.update_jobs(jobs_json)
        asset.print_jobs()
        captured = capsys.readouterr()
        assert captured.out == "{'id': 1, 'title': 'Foo developer', 'company': 'Bar industries'}\n"

    def test_find_tag_match(self, tmpdir, asset, capsys):
        users_json = tmpdir + "\\sub\\users.json"
        asset.update_users(users_json)
        jobs_json = tmpdir + "\\sub\\jobs.json"
        asset.update_jobs(jobs_json)
        asset.find_tag_match()
        captured = capsys.readouterr()
        assert captured.out == "User 1 matched to {'id': '1', 'title': 'Foo developer', 'company': 'Bar industries'," \
                               " 'tags': ['a', 'b', 'c']}\n"
