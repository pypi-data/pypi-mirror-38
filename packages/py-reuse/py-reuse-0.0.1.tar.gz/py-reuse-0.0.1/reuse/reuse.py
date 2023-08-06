""" Collection of useful python functions. """
import glob
import os


def check_exists(path):
    """ Check if the directory exists.

    Args:
        path (str): path to a directory or a file.

    Returns:
        bool: if path exist, return True, else return False

    Example:
        >>> dir_path = '/path/to/not/exist/dir'
        >>> check_dir_exists(dir_path)
        False

    """
    run_assert(isinstance(path, str), 'path must be a str')

    return os.path.exists(path)


def create_dir_if_not_exist(dir_path):
    """ Create the directory if it didn't exist.

    Args:
        dir_path (str): path to directory that to create.

    Example:
        >>> dir_path = '/path/to/dir1'
        >>> create_dir_if_not_exist(dir_path)

    """
    run_assert(isinstance(dir_path, str), 'dir_path must be a str')

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def concat_path(parts):
    """ Concatenate multiple parts to get a complete path.

    Args:
        parts (list): list contains each part of the path.

    Returns:
        str: concatenated path.

    Examples:
        >>> parts = ['home', 'myname', 'project']
        >>> path = concat_path(parts)
        >>> print(path)
        /home/myname/project

    """
    run_assert(all(isinstance(p, str) for p in parts), 'each element in parts must be a str')

    return os.path.join(*parts)


def list_file(path, ptn=None, sort=True):
    """ List files in given directory.

    Args:
        path (str): path of target directory.
        ptn (str): pattern to selected certain type of file. Defeault: None.
        sort (bool): if set to True, return sorted list of files.

    Returns:
        list: files in the directory that match the pattern.

    Example:
        >>> path = '/path/to/my/dir'
        >>> ptn = "*.py" # only choose *.py file
        >>> list_file(path, ptn=ptn, sort=True)
        ['/path/to/my/dir/1.py', '/path/to/my/dir/2.py']

    """
    run_assert(isinstance(path, str), 'path must be a str')
    if ptn is not None:
        run_assert(isinstance(ptn, str), 'ptn must be a str')

    if ptn is not None:
        path = os.path.join(path, ptn)

    files = glob.glob(path)

    if sort:
        files = sorted(files)

    return files


def list_dir(path, sort=True):
    """ List directories in given directory.

    Args:
        path (str): path of target directory.
        sort (bool): if set to True, return sorted list of dirs.

    Returns:
        list: a list contains subdirectories in the directory.

    Example:
        >>> path = '/path/to/my/dir'
        >>> list_dir(path)
        ['/path/to/my/dir/dir1', '/path/to/my/dir/dir2']

    """
    run_assert(isinstance(path, str), 'path must be a str')

    all_in_dir = glob.glob(path)
    dirs = [d for d in all_in_dir if os.path.isdir(d)]

    if sort:
        dirs = sorted(dirs)

    return dirs


def run_cmd(cmd):
    """ Run a Bash command in python.

    Args:
        cmd (str or list): the Shell command to execute.

    Returns:
        int: 0 if runs successfully, other value if fails.

    Example:
        >>> cmd = 'ls -l'
        >>> run_cmd(cmd)
        -rw-rw-r-- 1 user user  4651 Nov 10 20:19 reuse.py
        >>> cmd = ['ls', '-l']
        >>> run_cmd(cmd)
        -rw-rw-r-- 1 user user  4651 Nov 10 20:19 reuse.py

    """
    if isinstance(cmd, str):
        return os.system(cmd)

    if isinstance(cmd, list):
        run_assert(all(isinstance(c, str) for c in cmd), 'each element in cmd must be a str')
        cmd = ' '.join(cmd)
        return os.system(cmd)


def run_assert(cond, out):
    """ Run assert and output out if failed.

    Args:
        cond (func): condtion to judge True or False.
        out (str): output when assert fails.

    Example:
        >>> i = 20
        >>> run_assert(isinstance(i, str), 'i must be a str')
        AssertionError: i must be a str

    """
    assert cond, out


def read_from_file(file_name):
    """ Read content in a text file.

    Args:
        file_name (str): name of a text file.

    Returns:
        str: all content in the text file.

    Example:
        >>> content = read_from_file('/path/to/a.txt')
        >>> print(content)
        print('hello')

    """
    run_assert(os.path.exists(file_name), 'file doesn\'t exist.')

    with open(file_name) as f:
        return f.read()


def write_to_file(content, file_name):
    """ Write content to a text file.

    Args:
        content (str): content wanted to write to file.
        file_name (str): name of file to wirte.

    Example:
        >>> content = 'line1\nline2\nline3'
        >>> write_to_file(content, 'a.txt')

    """
    run_assert(isinstance(content, str), 'content must be a str')
    run_assert(os.path.exists(os.path.dirname(file_name)), 'parent dir of file_name doesn\'t exist')

    with open(file_name, 'w') as f:
        f.write(content)


def flat_list(ll):
    """ Flatten a list of list to a list.

    Args:
        ll (list): a list has elments of type list.

    Returns:
        list: one dimension list.

    Examples:
        >>> lol = [[1, 2], [3, 4]]
        >> l = flat_list(lol)
        >> print(l)
        [1, 2, 3, 4]

    """
    return [e for l in ll for e in l]
