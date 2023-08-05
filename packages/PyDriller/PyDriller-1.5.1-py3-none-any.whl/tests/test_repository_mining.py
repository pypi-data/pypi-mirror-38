import logging
from datetime import datetime

import pytest

from pydriller import RepositoryMining

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


# It should fail when no URLs are specified
def test_no_url():
    with pytest.raises(Exception):
        list(RepositoryMining().traverse_commits())


# It should fail when URL is not a string or a List
def test_badly_formatted_repo_url():
    with pytest.raises(Exception):
        list(RepositoryMining(path_to_repo=set('repo')).traverse_commits())


def test_simple_url():
    assert 5 == len(list(RepositoryMining(path_to_repo="test-repos/test1").traverse_commits()))


def test_two_local_urls():
    urls = ["test-repos/test1", "test-repos/test3"]
    assert 11 == len(list(RepositoryMining(path_to_repo=urls).traverse_commits()))


def test_simple_remote_url():
    dt2 = datetime(2018, 10, 20)
    assert 159 == len(
        list(RepositoryMining(path_to_repo="https://github.com/ishepard/pydriller.git", to=dt2).traverse_commits()))


def test_two_remote_urls():
    urls = ["https://github.com/mauricioaniche/repodriller.git", "https://github.com/ishepard/pydriller"]
    dt2 = datetime(2018, 10, 20)
    assert 518 == len(list(RepositoryMining(path_to_repo=urls, to=dt2).traverse_commits()))


def test_2_identical_local_urls():
    urls = ["test-repos/test1", "test-repos/test1"]
    assert 10 == len(list(RepositoryMining(path_to_repo=urls).traverse_commits()))


def test_both_local_and_remote_urls():
    dt2 = datetime(2018, 10, 20)
    assert 164 == len(
        list(RepositoryMining(path_to_repo=["test-repos/test1", "https://github.com/ishepard/pydriller.git"],
                              to=dt2).traverse_commits()))


def test_both_local_and_remote_urls_list():
    dt2 = datetime(2018, 10, 20)
    urls = ["test-repos/test1", "https://github.com/mauricioaniche/repodriller.git", "test-repos/test3",
            "https://github.com/ishepard/pydriller.git"]
    assert 529 == len(list(RepositoryMining(path_to_repo=urls,
                                            to=dt2).traverse_commits()))


def test_badly_formatted_url():
    with pytest.raises(Exception):
        list(RepositoryMining(path_to_repo='https://github.com/ishepard.git/test').traverse_commits())

    with pytest.raises(Exception):
        list(RepositoryMining(path_to_repo='test').traverse_commits())
