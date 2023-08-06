import re
import pytest

from chronoslib.helpers import (
    last_git_release_tag,
    git_tag_to_semver,
    git_commits_since_last_tag,
    parse_commit_log,
    NonexistentGitTagError
)


@pytest.fixture()
def git_tags_dummy() -> str:
    return (
        '23.235.23\n'
        'v324.23.34\n'
        'sfsfsdf\n'
        '342.23.3\n'
        'release-3.3.3\n'
    )


@pytest.fixture()
def semver_re():
    return re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+$')


@pytest.fixture()
def mock_git_tags() -> str:
    return (
        'rel-34.3.3\n'
        '23.33.33\n'
        'v3.34.3\n'
        'test-ab'
    )


@pytest.fixture()
def mock_commit_log_pat() -> str:
    return (
        '1e51ed35487fae022a98ab521ecbfa987e5027b1 test: add test for infer \n'
        '0a1a6b19e2e62b3315e3672ada885f0c7b40491c ci: separate tests and pr\n'
        '59d16365c1232ec447def8cabb4eed83d2a73dda ci: re-add tests dir to s\n'
        '6f7d9222f9b06741115119e73a90438a36cc1c84 ci: exclude conventional_\n'
        '6f87f6c6d7274904cd734d0b7a60386bb0c7f6cb chore: add conventional_c\n'
        '3eb2c6d29478700fead33de003f84c7a21711e50 refactor: rewrite helpers\n'
        '0f58df4be476401bb7427f9806ebd5ca6dfa934a refactor: add line breaks\n'
        'cc8873ee20cd06d659469dac6c348c1a0c7d349f docs: add docstrings to \n'
        '2126282fe7bf1e1433c76052b114a1a2d49b5170 ci: fix sonar-scanner com\n'
        '42b1ee6fa20f93e2655dacac27c3f172d9328e8e ci: generate coverage rep\n'
        '5700ccc2310469282d23a8d6b2203d81ab35c448 refactor: replace ambiqu\n'
        '96504d9ceefae2f1b7caf3665ad43641b64d4487 test: add tests for cli m\n'
        '05580e034374467953f1eb2f71f5659b9c49cdb9 chore: partially implemen\n'
        'e524ca35a9643c636e1e5b68a83bcb495f46bb6a chore: enable branch cove\n'
        '86d64e9f1b8f42181f2452ce534ab18c896726ee ci: generate coverage rep\n'
        'aff7b1a19bf0c0a4b71a26c13bc01a23c8d0ec90 style: indent .yaml and .\n'
        '6644159319fd82ad916bc9fc8a5de4aa1ab2aa84 ci: move ansible files i\n'
    )


@pytest.fixture()
def mock_commit_log_min() -> str:
    return (
        '1e51ed35487fae022a98ab521ecbfa987e5027b1 test: add test for infer \n'
        '0a1a6b19e2e62b3315e3672ada885f0c7b40491c ci: separate tests and pr\n'
        '59d16365c1232ec447def8cabb4eed83d2a73dda ci: re-add tests dir to s\n'
        '6f7d9222f9b06741115119e73a90438a36cc1c84 ci: exclude conventional_\n'
        '6f87f6c6d7274904cd734d0b7a60386bb0c7f6cb chore: add conventional_c\n'
        '3eb2c6d29478700fead33de003f84c7a21711e50 feat: rewrite helpers\n'
        '0f58df4be476401bb7427f9806ebd5ca6dfa934a feat(123): add line breaks\n'
        'cc8873ee20cd06d659469dac6c348c1a0c7d349f docs: add docstrings to \n'
        '2126282fe7bf1e1433c76052b114a1a2d49b5170 ci: fix sonar-scanner com\n'
        '42b1ee6fa20f93e2655dacac27c3f172d9328e8e ci: generate coverage rep\n'
        '5700ccc2310469282d23a8d6b2203d81ab35c448 refactor: replace ambiqu\n'
        '96504d9ceefae2f1b7caf3665ad43641b64d4487 test: add tests for cli m\n'
        '05580e034374467953f1eb2f71f5659b9c49cdb9 chore: partially implemen\n'
        'e524ca35a9643c636e1e5b68a83bcb495f46bb6a chore: enable branch cove\n'
        '86d64e9f1b8f42181f2452ce534ab18c896726ee ci: generate coverage rep\n'
        'aff7b1a19bf0c0a4b71a26c13bc01a23c8d0ec90 style: indent .yaml and .\n'
        '6644159319fd82ad916bc9fc8a5de4aa1ab2aa84 ci: move ansible files i\n'
    )


@pytest.fixture()
def mock_commit_log_maj() -> str:
    return (
        '1e51ed35487fae022a98ab521ecbfa987e5027b1 test: add test for infer \n'
        '0a1a6b19e2e62b3315e3672ada885f0c7b40491c ci: separate tests and pr\n'
        '59d16365c1232ec447def8cabb4eed83d2a73dda ci: re-add tests dir to s\n'
        '6f7d9222f9b06741115119e73a90438a36cc1c84 ci: exclude conventional_\n'
        '6f87f6c6d7274904cd734d0b7a60386bb0c7f6cb chore: add conventional_c\n'
        '3eb2c6d29478700fead33de003f84c7a21711e50 feat: rewrite helpers\n'
        '0f58df4be476401bb7427f9806ebd5ca6dfa934a BREAKING CHANGE: ne breaks\n'
        'cc8873ee20cd06d659469dac6c348c1a0c7d349f docs: add docstrings to \n'
        '2126282fe7bf1e1433c76052b114a1a2d49b5170 ci: fix sonar-scanner com\n'
        '42b1ee6fa20f93e2655dacac27c3f172d9328e8e ci: generate coverage rep\n'
        '5700ccc2310469282d23a8d6b2203d81ab35c448 refactor: replace ambiqu\n'
        '96504d9ceefae2f1b7caf3665ad43641b64d4487 test: add tests for cli m\n'
        '05580e034374467953f1eb2f71f5659b9c49cdb9 BREAKING CHANGE(123): emen\n'
        'e524ca35a9643c636e1e5b68a83bcb495f46bb6a chore: enable branch cove\n'
        '86d64e9f1b8f42181f2452ce534ab18c896726ee ci: generate coverage rep\n'
        'aff7b1a19bf0c0a4b71a26c13bc01a23c8d0ec90 style: indent .yaml and .\n'
        '6644159319fd82ad916bc9fc8a5de4aa1ab2aa84 ci: move ansible files i\n'
    )


def test_last_git_release_tag_returns_correct_value(semver_re, mock_git_tags):
    assert last_git_release_tag(mock_git_tags) == 'rel-34.3.3'


def test_git_tag_to_semver_returns_correct_value():
    out = git_tag_to_semver('v3.2.5')
    assert out.version == '3.2.5'


def test_git_commits_since_last_tag_bad_tag_raises_error():
    with pytest.raises(NonexistentGitTagError):
        git_commits_since_last_tag('git-tag-that-does-not-exist')


def test_parse_commit_log_returns_pat(mock_commit_log_pat):
    out = parse_commit_log(mock_commit_log_pat)
    assert out == 'pat'


def test_parse_commit_log_returns_min(mock_commit_log_min):
    out = parse_commit_log(mock_commit_log_min)
    assert out == 'min'


def test_parse_commit_log_returns_maj(mock_commit_log_maj):
    out = parse_commit_log(mock_commit_log_maj)
    assert out == 'maj'
