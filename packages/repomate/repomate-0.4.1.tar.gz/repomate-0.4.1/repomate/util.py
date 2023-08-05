"""Some general utility functions.

.. module:: util
    :synopsis: Miscellaneous utility functions that don't really belong anywhere else.

.. moduleauthor:: Simon Larsén
"""
import os
import sys
import pathlib
import random
from typing import Iterable, Generator, Union, Tuple, Mapping, List
from repomate import tuples


def validate_non_empty(**kwargs) -> None:
    r"""Validate that arguments are not empty. Raise ValueError if any argument
    is empty.

    Args:
        **kwargs: Mapping on the form {param_name: argument} where param_name
        is the name of the parameter and argument is the value passed in.
    """
    for param_name, argument in kwargs.items():
        if not argument:
            raise ValueError("{} must not be empty".format(param_name))


def validate_types(**kwargs) -> None:
    r"""Validate argument types. Raise TypeError if there is a mismatch.

    Args:
        **kwargs: Mapping on the form {param_name: (argument, expected_type)},
        where param_name is the name of the parameter, argument is the passed
        in value and expected type is either a single type, or a tuple of
        types.
    """
    for param_name, (argument, expected_types) in kwargs.items():
        if not isinstance(argument, expected_types):
            if isinstance(expected_types, tuple):
                exp_type_str = " or ".join(
                    [t.__name__ for t in expected_types])
            else:
                exp_type_str = expected_types.__name__
            raise TypeError(
                "{} is of type {.__class__.__name__}, expected {}".format(
                    param_name, argument, exp_type_str))


def read_issue(issue_path: str) -> tuples.Issue:
    """Attempt to read an issue from a textfile. The first line of the file
    is interpreted as the issue's title.

    Args:
        issue_path: Local path to textfile with an issue.
    """
    if not os.path.isfile(issue_path):
        raise ValueError("{} is not a file".format(issue_path))
    with open(issue_path, 'r', encoding=sys.getdefaultencoding()) as file:
        return tuples.Issue(file.readline().strip(), file.read())


def generate_repo_name(team_name: str, master_repo_name: str) -> str:
    """Construct a repo name for a team.
    
    Args:
        team_name: Name of the associated team.
        master_repo_name: Name of the template repository.
    """
    validate_non_empty(team_name=team_name, master_repo_name=master_repo_name)
    return "{}-{}".format(team_name, master_repo_name)


def generate_repo_names(team_names: Iterable[str],
                        master_repo_names: Iterable[str]) -> Iterable[str]:
    """Construct all combinations of generate_repo_name(team_name, master_repo_name) for the provided
    team names and master repo names.

    Args:
        team_names: One or more names of teams.
        master_repo_names: One or more names of master repositories.

    Returns:
        a list of repo names for all combinations of team and master repo.
    """
    validate_non_empty(
        team_names=team_names, master_repo_names=master_repo_names)
    master_repo_names = list(
        master_repo_names)  # needs to be traversed multiple times
    return [
        generate_repo_name(team_name, master_name)
        for master_name in master_repo_names for team_name in team_names
    ]


def generate_review_team_name(student: str, master_repo_name: str) -> str:
    """Generate a review team name.

    Args:
        student: A student username.
        master_repo_name: Name of a master repository.

    Returns:
        a review team name for the student repo associated with this master
        repo and student.
    """
    return generate_repo_name(student, master_repo_name) + "-review"


def repo_name(repo_url: str) -> str:
    """Extract the name of the repo from its url.

    Args:
        repo_url: A url to a repo.
    """
    repo_name = repo_url.split("/")[-1]
    if repo_name.endswith('.git'):
        return repo_name[:-4]
    return repo_name


def is_git_repo(path: str) -> bool:
    """Check if a directory has a .git subdirectory.
    
    Args:
        path: Path to a local directory.
    Returns:
        True if there is a .git subdirectory in the given directory.
    """
    return os.path.isdir(path) and '.git' in os.listdir(path)


def _ends_with_ext(path: Union[str, pathlib.Path],
                   extensions: Iterable[str]) -> bool:
    _, ext = os.path.splitext(str(path))
    return ext in extensions


def find_files_by_extension(root: Union[str, pathlib.Path], *extensions: str
                            ) -> Generator[pathlib.Path, None, None]:
    """Find all files with the given file extensions, starting from root.

    Args:
        root: The directory to start searching.
        extensions: One or more file extensions to look for.
    Returns:
        a generator that yields a Path objects to the files.
    """
    if not extensions:
        raise ValueError("must provide at least one extension")
    for cwd, _, files in os.walk(root):
        for file in files:
            if _ends_with_ext(file, extensions):
                yield pathlib.Path(cwd) / file


def generate_review_allocations(master_repo_name: str, students: Iterable[str],
                                num_reviews: int) -> Mapping[str, List[str]]:
    """Generate a (peer_review_team -> reviewers) mapping for each student
    repository (i.e. <student>-<master_repo_name>), where len(reviewers) =
    num_reviews.

    .. important::
            
        There must be strictly more students than reviewers per repo
        (`num_reviews`). Otherwise, allocation is impossible.

    Args:
        master_repo_name: Name of a master repository.
        students: Students for which to generate peer review allocations.
        num_reviews: Amount of reviews each student should perform (and
        consequently amount of reviewers per repo)
    Returns:
        a (peer_review_team -> reviewers) mapping for each student repository.
    """
    if num_reviews >= len(students):
        raise ValueError("num_reviews must be less than len(students)")
    if num_reviews <= 0:
        raise ValueError("num_reviews must be greater than 0")

    students = list(students)
    random.shuffle(students)

    # create a list of lists, where each non-first list is a left-shifted
    # version of the previous list (lists wrap around)
    # e.g. for students [4, 3, 1] and num_reviews = 2, the result is
    # allocations = [[4, 3, 1], [3, 1, 4], [1, 4, 3]] and means that
    # student 4 gets reviewed by 3 and 1, 3 by 1 and 4 etc.
    allocations = [students]
    for _ in range(num_reviews):
        next_reviewers = list(allocations[-1])
        next_reviewers.append(next_reviewers.pop(0))  # shift list left
        allocations.append(next_reviewers)

    review_allocations = {
        generate_review_team_name(reviewee, master_repo_name): reviewers
        for reviewee, *reviewers in zip(*allocations)
    }
    return review_allocations
