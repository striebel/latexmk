import sys
import os
import stat
import shutil

from .config.user import get_pdflatex_file_path
from .config.user import get_bibtex_file_path
from .config.user import get_pythontex_file_path

from .config.project import get_src_dir_path
from .config.project import get_cache_dir_path
from .config.project import get_build_dir_path
from .config.project import get_build_cache_dir_path

from .config.project import get_build_main_pdf_file_path
from .config.project import get_main_pdf_file_path

from .shutil import copytree_as_symlinks



def build_dir_exists() -> bool:

    build_dir_path = get_build_dir_path()

    return os.path.isdir(build_dir_path)


def clean_build_dir() -> None:

    build_dir_path = get_build_dir_path()

    assert os.path.isdir(build_dir_path), build_dir_path

    shutil.rmtree(build_dir_path)

    assert not os.path.isdir(build_dir_path), build_dir_path

    return None



def init_build_dir() -> None:

    src_dir_path = get_src_dir_path()
    assert os.path.isdir(src_dir_path), src_dir_path

    build_dir_path = get_build_dir_path()
    assert not os.path.isdir(build_dir_path), build_dir_path

    shutil.copytree(src_dir_path, build_dir_path)
    assert os.path.isdir(src_dir_path), src_dir_path
    assert os.path.isdir(build_dir_path), build_dir_path


    cache_dir_path = get_cache_dir_path()
    if os.path.isdir(cache_dir_path):

        build_cache_dir_path = get_build_cache_dir_path()
        assert not os.path.isdir(build_cache_dir_path)

        copytree_as_symlinks(cache_dir_path, build_cache_dir_path)

        assert os.path.isdir(cache_dir_path), cache_dir_path
        assert os.path.isdir(build_cache_dir_path), build_cache_dir_path

    return None


def update_main_pdf_file() -> None:
    build_main_pdf_file_path = get_build_main_pdf_file_path()
    assert os.path.isfile(build_main_pdf_file_path), build_main_pdf_file_path

    main_pdf_file_path = get_main_pdf_file_path()
    if not os.path.isfile(main_pdf_file_path):
        sys.stderr.write('latexmk: info: os.path.isfile(main_pdf_file_path) is False\n')

    shutil.copy(build_main_pdf_file_path, main_pdf_file_path)
    return None



def _execute(argv : tuple) -> int:

    assert isinstance(argv, tuple), (type(argv), argv)

    assert 2 <= len(argv), (len(argv), argv)

    for i, arg in enumerate(argv):
        assert isinstance(argv[i], str), (i, type(argv[i]), argv[i])

    assert os.path.isfile(argv[0]), argv[0]


    # Confirm that the file is executable

    assert bool(0o100 & os.stat(argv[0]).st_mode)


    build_dir_path = get_build_dir_path()

    assert os.path.isdir(build_dir_path), build_dir_path


    pid = os.fork()

    assert isinstance(pid, int)

    if 0 == pid: # child branch

        assert os.getcwd() != build_dir_path
        assert os.getcwd() == os.environ['PWD']

        os.chdir(build_dir_path)

        assert os.getcwd() == build_dir_path
        assert os.getcwd() != os.environ['PWD']

        os.environ['PWD'] = os.getcwd()

        os.execve(
            path = argv[0],
            argv = argv,
            env  = os.environ
        )

        sys.stderr.write('error: unexpected behavior: execve returned\n')
        sys.exit(3)

    child_pid, raw_wait_status = os.wait()

    assert isinstance(child_pid, int)
    assert pid == child_pid
    assert isinstance(raw_wait_status, int)
    assert 0 <= raw_wait_status

    wait_status = os.waitstatus_to_exitcode(raw_wait_status)

    assert isinstance(wait_status, int)

    return wait_status



def execute_pdflatex() -> int:

    pdflatex_file_path = get_pdflatex_file_path()

    assert os.path.isfile(pdflatex_file_path), pdflatex_file_path

    argv = \
        (
            pdflatex_file_path,
            '-interaction=nonstopmode', # do not stop for user input
                                        # at any point; if an error occurs,
                                        # keep processing.
            '-halt-on-error',           # if an error occurs, exit immediately
            'main'
        )

    wait_status = _execute(argv)

    assert isinstance(wait_status, int)

    return wait_status



def execute_bibtex() -> int:

    bibtex_file_path = get_bibtex_file_path()

    assert os.path.isfile(bibtex_file_path), bibtex_file_path

    argv = (bibtex_file_path, 'main')

    wait_status = _execute(argv)

    assert isinstance(wait_status, int)

    return wait_status



def execute_pythontex() -> int:

    pythontex_file_path = get_pythontex_file_path()

    assert os.path.isfile(pythontex_file_path), pythontex_file_path

    argv = (pythontex_file_path, 'main')

    wait_status = _execute(argv)

    assert isinstance(wait_status, int)

    return wait_status




