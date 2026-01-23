import subprocess
import pytest
from podcast.git_ops import git_add, git_commit, git_push, commit_episode

def test_git_add(mocker):
    """Should run git add with correct paths"""
    mock_run = mocker.patch("subprocess.run")
    git_add(["file1", "file2"])
    mock_run.assert_called_once_with(["git", "add", "file1", "file2"], check=True)

def test_git_commit(mocker):
    """Should run git commit with message"""
    mock_run = mocker.patch("subprocess.run")
    git_commit("My message")
    mock_run.assert_called_once_with(["git", "commit", "-m", "My message"], check=True)

def test_git_push(mocker):
    """Should run git push"""
    mock_run = mocker.patch("subprocess.run")
    git_push()
    mock_run.assert_called_once_with(["git", "push"], check=True)

def test_commit_episode(mocker):
    """Should add, commit with episode title, and push"""
    m_add = mocker.patch("podcast.git_ops.git_add")
    m_commit = mocker.patch("podcast.git_ops.git_commit")
    m_push = mocker.patch("podcast.git_ops.git_push")
    
    commit_episode("Episode Title", ["file1"])
    
    m_add.assert_called_once_with(["file1"])
    m_commit.assert_called_once_with("Add episode: Episode Title")
    m_push.assert_called_once()

def test_commit_episode_no_push(mocker):
    """Should add and commit but skip push when flag set"""
    m_add = mocker.patch("podcast.git_ops.git_add")
    m_commit = mocker.patch("podcast.git_ops.git_commit")
    m_push = mocker.patch("podcast.git_ops.git_push")
    
    commit_episode("Episode Title", ["file1"], push=False)
    
    m_add.assert_called_once()
    m_commit.assert_called_once()
    m_push.assert_not_called()
