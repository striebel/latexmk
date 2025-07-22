import sys
import os


from .. import get_build_main_tex_file_path



def title(title_str) -> None:
    assert isinstance(title_str, str), (type(title_str), title_str)

    build_main_tex_file_path = get_build_main_tex_file_path()
    assert os.path.isfile(build_main_tex_file_path), build_main_tex_file_path

    with open(build_main_tex_file_path, 'rt') as build_main_tex_file:
        build_main_tex_str = build_main_tex_file.read()

    old_title = '\\title{Dissertation Title}'
    new_title = f'\\title{"{"}{title_str}{"}"}'
    del title_str

    assert old_title in build_main_tex_str, (old_title, len(build_main_tex_str))
    assert 1 == build_main_tex_str.count(old_title)

    build_main_tex_str = build_main_tex_str.replace(old_title, new_title)
    del old_title
    del new_title

    with open(build_main_tex_file_path, 'wt') as build_main_tex_file:
        build_main_tex_file.write(build_main_tex_str)

    return None



def date(date_str) -> None:
    assert isinstance(date_str, str), (type(date_str), date_str)

    build_main_tex_file_path = get_build_main_tex_file_path()
    assert os.path.isfile(build_main_tex_file_path), build_main_tex_file_path

    with open(build_main_tex_file_path, 'rt') as build_main_tex_file:
        build_main_tex_str = build_main_tex_file.read()

    old_date = '\\date{Month Year}'
    new_date = f'\\date{"{"}{date_str}{"}"}'
    del date_str
    
    assert old_date in build_main_tex_str, (len(build_main_tex_str), old_date)
    assert 1 == build_main_tex_str.count(old_date)

    build_main_tex_str = build_main_tex_str.replace(old_date, new_date)
    del old_date
    del new_date

    with open(build_main_tex_file_path, 'wt') as build_main_tex_file:
        build_main_tex_file.write(build_main_tex_str)

    return None



def includeonly(include_chapters_list) -> list:
    '''
    Argument: list of chapters to include
    Returns : list of all available chapters of which "include_chapters_list"
                  will have been a subset
    '''
    assert isinstance(include_chapters_list, list), (include_chapters_list, type(include_chapters_list))
    assert 1 <= len(include_chapters_list), len(include_chapters_list)

    build_main_tex_file_path = get_build_main_tex_file_path()
    assert os.path.isfile(build_main_tex_file_path), build_main_tex_file_path

    with open(build_main_tex_file_path, 'rt') as build_main_tex_file:
        build_main_tex_str = build_main_tex_file.read()

    start_str = '\\includeonly{%\n'
    end_str   = '}\n'

    start_idx = build_main_tex_str.index(start_str)
    end_idx   = build_main_tex_str.index(end_str, start_idx) + len(end_str)

    all_chapters_str = build_main_tex_str[start_idx:end_idx]

    all_chapters_str = all_chapters_str.replace(start_str, '')
    all_chapters_str = all_chapters_str.replace(end_str  , '')
    all_chapters_str = all_chapters_str.replace('%'      , '')

    all_chapters_list = [ch.strip() for ch in all_chapters_str.split(',')]

    body_str = ''
    for ch in include_chapters_list:
        assert ch in all_chapters_list, (all_chapters_list, ch)
        body_str += f'{" "*4}{ch},%\n'
    del include_chapters_list

    assert ',%\n' == body_str[-3:]
    body_str = body_str[:-3] + body_str[-2:]

    includeonly_str = start_str + body_str + end_str
    del start_str
    del body_str
    del end_str

    build_main_tex_str = build_main_tex_str[:start_idx] + includeonly_str + build_main_tex_str[end_idx:]
    del start_idx
    del end_idx

    with open(build_main_tex_file_path, 'wt') as build_main_tex_file:
        build_main_tex_file.write(build_main_tex_str)

    return all_chapters_list





