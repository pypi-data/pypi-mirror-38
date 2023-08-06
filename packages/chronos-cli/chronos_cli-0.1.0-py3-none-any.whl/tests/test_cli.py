import pytest

from chronoslib.cli import (
    main,
    # infer,
    # commit,
    # NoGitTagsError
)


def test_main_prints_help_with_no_args(capsys):
    with pytest.raises(SystemExit):
        main([''])
    captured = capsys.readouterr()
    assert 'usage:' in captured.err


def test_main_prints_help_with_invalid_args(capsys):
    with pytest.raises(SystemExit):
        for i in ['--invalid-option'], ['invalid-sub-command'], ['wrong']:
            main(i)
            captured = capsys.readouterr()
            assert 'usage:' in captured.err


# def test_infer_raises_no_git_tags_error_with_empty_git_tags_str(capsys):
#     parser: argparse.ArgumentParser = argparse.ArgumentParser()
#     args: argparse.Namespace = parser.parse_args('')
#     with pytest.raises(NoGitTagsError):
#         infer(args=args, git_tags_str='')


# def test_infer_returns_correct_value(capsys):
#     parser: argparse.ArgumentParser = argparse.ArgumentParser()
#     args: argparse.Namespace = parser.parse_args('')
#     infer(args=args, git_tags_str='v33.3.3\nv2.2.2\n')
#     captured = capsys.readouterr()
#     assert '33.3.3' in captured.out


# def test_commit(capsys):
#     parser: argparse.ArgumentParser = argparse.ArgumentParser()
#     args: argparse.Namespace = parser.parse_args(['--invalid-option'])
#     with pytest.raises(SystemExit):
#         commit(args)
#         captured = capsys.readouterr()
#         assert 'usage:' in captured.err
