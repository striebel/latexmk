import os


from .user import get_project_dir_path


def get_src_dir_path() -> str:
    project_dir_path = get_project_dir_path()
    assert os.path.isdir(project_dir_path), project_dir_path
    src_dir_path = os.path.join(project_dir_path, 'src')
    return src_dir_path


def get_build_dir_path() -> str:
    project_dir_path = get_project_dir_path()
    assert os.path.isdir(project_dir_path), project_dir_path
    build_dir_path = os.path.join(project_dir_path, 'build')
    return build_dir_path


def _get_project_config_file_path() -> str:
    project_dir_path = get_project_dir_path()
    assert os.path.isdir(project_dir_path), project_dir_path
    project_config_file_path = os.path.join(project_dir_path, '.latexmk.project.json')
    return project_config_file_path


def _project_config_file_exists() -> bool:
    project_config_file_path = _get_project_config_file_path()
    return (
        os.path.isfile(project_config_file_path)
        and
        0 < os.path.getsize(project_config_file_path)
    )

 
def _get_default_project_config_dict() -> dict:
    default_project_config_dict = dict()
    return default_project_config_dict


def _read_project_config_file() -> dict:
    project_config_file_path = _get_project_config_file_path()
    assert os.path.isfile(project_config_file_path), project_config_file_path
    with open(project_config_file_path, 'rt') as project_config_file:
        project_config_dict = json.load(fp=project_config_file)

    default_project_config_dict = _get_default_project_config_dict()
    assert default_project_config_dict.keys() == project_config_dict.keys()
    del default_project_config_dict

    return project_config_dict


def _write_project_config_file(project_config_dict) -> None:
    assert isinstance(project_config_dict, dict), type(project_config_dict)

    default_project_config_dict = _get_default_project_config_dict()
    assert default_project_config_dict.keys() == project_config_dict.keys()
    del default_project_config_dict

    project_config_file_path = _get_project_config_file_path()
    with open(project_config_file_path, 'wt') as project_config_file:
        json.dump(fp=project_config_file, obj=project_config_dict, indent=4)
    return None


def _get_project_config_dict() -> dict:
    global project_config_dict
    if 'project_config_dict' not in globals():
        if _project_config_file_exists():
            project_config_dict = _read_project_config_file()
        else:
            project_config_dict = _get_default_project_config_dict()
            _write_project_config_file(project_config_dict)
    assert 'project_config_dict' in globals()
    assert isinstance(project_config_dict, dict), type(config_dict)
    return project_config_dict



def _update_project_config_value(key, value) -> None:
    project_config_dict = _get_project_config_dict()

    assert key in project_config_dict, key
    project_config_dict[key] = value
    del key
    del value

    return _write_project_config_file(project_config_dict)
    
    
def _get_project_config_value(key) -> str:
    project_config_dict = _get_project_config_dict()
    assert key in project_config_dict, key
    return project_config_dict[key]






