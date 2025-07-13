import sys
import os
import json



def get_config_file_path() -> str:
    return os.path.join(os.path.expanduser('~'), '.latexmk.json')


def get_default_config_dict() -> dict:
    default_config_dict = \
        {
            'pdflatex_file_path' : '/usr/bin/pdflatex',
            'bibtex_file_path'   : '/usr/bin/bibtex',
            'pythontex_file_path': '/usr/share/texlive/texmf-dist/scripts/pythontex/pythontex3.py'
        } 
    return default_config_dict


def read_config_file() -> dict:
    config_file_path = get_config_file_path()
    assert os.path.isfile(config_file_path), config_file_path
    with open(config_file_path, 'rt') as config_file:
        config_dict = json.load(fp=config_file)

    default_config_dict = get_default_config_dict()
    assert default_config_dict.keys() == config_dict.keys()
    del default_config_dict

    return config_dict


def write_config_file(config_dict) -> None:
    default_config_dict = get_default_config_dict()
    assert default_config_dict.keys() == config_dict.keys()
    del default_config_dict

    config_file_path = get_config_file_path()
    with open(config_file_path, 'wt') as config_file:
        json.dump(fp=config_file, obj=config_dict, indent=4)
    return None


def write_default_config_file() -> None:
    config_file_path = get_config_file_path()
    assert not os.path.isfile(config_file_path), config_file_path
    del config_file_path

    default_config_dict = get_default_config_dict()
    return write_config_file(default_config_dict)


def update_config_value(key, value) -> None:
    return None
    
    


def get_pdflatex_file_path() -> str:

    pdflatex_file_path = \
        os.path.join(
            '/',
            'usr',
            'bin',
            'pdflatex'
        )

    return pdflatex_file_path



def get_bibtex_file_path() -> str:

    bibtex_file_path = \
        os.path.join(
            '/',
            'usr',
            'bin',
            'bibtex'
        )

    return bibtex_file_path



def get_pythontex_file_path() -> str:

    pythontex_file_path = \
        os.path.join(
            '/',
            'usr',
            'share',
            'texlive',
            'texmf-dist',
            'scripts',
            'pythontex',
            'pythontex3.py'
        )

    return pythontex_file_path



def main() -> int:

    config_file_path = get_config_file_path()

    if not os.path.isfile(config_file_path):
        write_default_config_file()
        sys.stderr.write('config file "~/.latexmk.json" written\n')
        return 0
    else:
        sys.stderr.write('config file "~/.latexmk.json" already exists\n')
        return 1



if '__main__' == __name__:
    sys.exit(main())







