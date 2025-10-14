import os

from .. import get_build_main_aux_file_path



def set_atinputs(includeonly_chapters_list, include_chapters_list) -> None:
    '''
    includeonly_chapters_list: the chapters to be included in this pdf build
    
    include_chapters_list    : all existing chapters in the project, which means
                               all possible chapters that could be included in
                               this pdf build
    '''

    assert isinstance(includeonly_chapters_list, list)
    assert isinstance(include_chapters_list, list)

    assert set(includeonly_chapters_list).issubset(include_chapters_list)

    build_main_aux_file_path = get_build_main_aux_file_path()
    assert os.path.isfile(build_main_aux_file_path), build_main_aux_file_path

    with open(build_main_aux_file_path, 'rt') as build_main_aux_file:
        build_main_aux_str = build_main_aux_file.read()

    del build_main_aux_file


    for chapter in include_chapters_list:
        
        a = f'\\@input{"{"}{chapter}.aux{"}"}\n'

        assert a in build_main_aux_str, a

        if chapter not in includeonly_chapters_list:
            
            b = f'%{a}'
            build_main_aux_str = build_main_aux_str.replace(a, b)
    

    with open(build_main_aux_file_path, 'wt') as build_main_aux_file:
        build_main_aux_file.write(build_main_aux_str)

    del build_main_aux_str
    del build_main_aux_file
    del build_main_aux_file_path
    
    return None






