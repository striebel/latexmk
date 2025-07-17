import sys
import os
import json
import argparse



def get_config_file_path() -> str:
    return os.path.join(os.path.expanduser('~'), '.latexmk.global.json')


def config_file_exists() -> bool:
    config_file_path = get_config_file_path()
    return (
        os.path.isfile(config_file_path)
        and
        0 < os.path.getsize(config_file_path)
    )


def get_default_config_dict() -> dict:
    default_config_dict = \
        {
            'pdflatex_file_path' : '/usr/bin/pdflatex',
            'bibtex_file_path'   : '/usr/bin/bibtex',
            'pythontex_file_path': '/usr/share/texlive/texmf-dist/scripts/pythontex/pythontex3.py',
            'project_dir_path'   : None
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
    assert isinstance(config_dict, dict), type(config_dict)

    default_config_dict = get_default_config_dict()
    assert default_config_dict.keys() == config_dict.keys()
    del default_config_dict

    config_file_path = get_config_file_path()
    with open(config_file_path, 'wt') as config_file:
        json.dump(fp=config_file, obj=config_dict, indent=4)
    return None


def get_config_dict() -> dict:
    global config_dict
    if 'config_dict' not in globals():
        if config_file_exists():
            config_dict = read_config_file()
            assert isinstance(config_dict, dict), type(config_dict)
        else:
            config_dict = get_default_config_dict()
            assert isinstance(config_dict, dict), type(config_dict)
            write_config_file(config_dict)
    assert 'config_dict' in globals()
    assert isinstance(config_dict, dict), type(config_dict)
    return config_dict



def _update_config_value(key, value) -> None:
    config_dict = get_config_dict()

    assert key in config_dict, key
    config_dict[key] = value
    del key
    del value

    return write_config_file(config_dict)
    
    
def _get_config_value(key) -> str:
    config_dict = get_config_dict()
    assert key in config_dict, key
    return config_dict[key]


def get_pdflatex_file_path() -> str:
    return _get_config_value('pdflatex_file_path')


def get_bibtex_file_path() -> str:
    return _get_config_value('bibtex_file_path')


def get_pythontex_file_path() -> str:
    return _get_config_value('pythontex_file_path')


def get_project_dir_path() -> str:
    return _get_config_value('project_dir_path')


def update_project_dir_path(project_dir_path) -> None:
    _update_config_value('project_dir_path', project_dir_path)



def main() -> int:

    parser = argparse.ArgumentParser()

    parser.add_argument('key'  , nargs='?', type=str, default=None)
    parser.add_argument('value', nargs='?', type=str, default=None)

    args = parser.parse_args()


    config_dict = get_config_dict()
    
    if args.key is None and args.value is None:
        # print all (key, value) pairs in the config dict

        max_key_width = max(len(k) for k in config_dict.keys())

        for k, v in config_dict.items():
            k = k.ljust(max_key_width)
            sys.stdout.write(f'{k}{" "*2}{v}\n')

    elif isinstance(args.key, str) and args.value is None:
        # print the value pointed to by the given key

        v = get_config_value(args.key)
        sys.stdout.write(f'{v}\n')

    elif isinstance(args.key, str) and isinstance(args.value, str):
        # update the field indicated to the given key to the given value

        _update_config_value(args.key, args.value)

    else:
        raise RuntimeError(f'unexpected (key, value) pair: ({args.key}, {args.value})')

    return 0



if '__main__' == __name__:
    sys.exit(main())







