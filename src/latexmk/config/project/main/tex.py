import sys
import os


from .. import get_build_main_tex_file_path



def set_title(title_str) -> None:
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



def set_date(date_str) -> None:
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




def _remove_comments(tex_str) -> str:
   
    spans = []

    i = 0
 
    while True:

        start_idx = tex_str.find('%', i)

        if -1 == start_idx:
            break
        
        end_idx = tex_str.find('\n', start_idx)
        if -1 == end_idx:
            end_idx = len(tex_str)

        spans.append((start_idx, end_idx))

        i = end_idx + 1

    del i

    for j in range(len(spans)-1, -1, -1):

        start_idx, end_idx = spans[j]

        assert '%' == tex_str[start_idx]
        assert '\n' == tex_str[end_idx] or len(spans)-1 == j

        tex_str = tex_str[:start_idx] + '%\n' + tex_str[end_idx+1:]

    return tex_str



def get_includes() -> list:
    '''
    Return the list of all chapters that are specified in "\\include"
    macros in build/main.tex
    '''

    include_chapters_list = []

    build_main_tex_file_path = get_build_main_tex_file_path()
    assert os.path.isfile(build_main_tex_file_path), build_main_tex_file_path

    with open(build_main_tex_file_path, 'rt') as build_main_tex_file:
        build_main_tex_str = build_main_tex_file.read()

    del build_main_tex_file
    del build_main_tex_file_path

    start_str = '\\include{'
    end_str   = '}'

    a = build_main_tex_str; del build_main_tex_str

    a = _remove_comments(a)

    while True:
        start_idx = a.find(start_str)

        if -1 < start_idx:

            a = a[start_idx+len(start_str):]

            end_idx = a.find(end_str)
            assert 0 < end_idx, end_idx

            chapter = a[:end_idx].strip()

            a = a[end_idx+len(end_str):]

            include_chapters_list.append(chapter)
        else:
            break

    return include_chapters_list



def assert_chapters_lists_equal(cla, clb, log_indent=0, error_exit_status=3) -> None:
    '''
    cla : chapters_list_a
    clb : chapters_list_b
    '''
    assert isinstance(cla, list), type(cla)
    assert isinstance(clb, list), type(clb)

    assert len(set(cla)) == len(cla)
    assert len(set(clb)) == len(clb)

    for (x_name, clx), (y_name, cly) in (
        (('a', cla), ('b', clb)),
        (('b', clb), ('a', cla))
    ):
        for x in clx: 
            if not x in cly: 
                sys.stderr.write(f'{" "*log_indent}error: cl{x_name} (chapters_list_{x_name}) contains "{x}"\n') 
                sys.stderr.write(f'{" "*(log_indent+4)}but cl{y_name} list does not and rather contains only:\n') 
                for y in cly: 
                    sys.stderr.write(f'{" "*(log_indent+8)}{y}\n') 
                sys.exit(error_exit_status) 
   
    assert len(cla) == len(clb) 
    assert cla == clb

    return None




def get_includeonly() -> list:
    '''
    Returns the list of chapters given in the \\includeonly macro in build/main.tex
    '''

    build_main_tex_file_path = get_build_main_tex_file_path()
    assert os.path.isfile(build_main_tex_file_path), build_main_tex_file_path

    with open(build_main_tex_file_path, 'rt') as build_main_tex_file:
        build_main_tex_str = build_main_tex_file.read()

    del build_main_tex_file
    del build_main_tex_file_path

    start_str = '\\includeonly{'
    end_str   = '}\n'

    start_idx = build_main_tex_str.index(start_str)
    end_idx   = build_main_tex_str.index(end_str, start_idx) + len(end_str)

    # io: includeonly
    io_chapters_str = build_main_tex_str[start_idx:end_idx]

    del start_idx
    del end_idx
    del build_main_tex_str

    io_chapters_str = io_chapters_str.replace(start_str, '')
    io_chapters_str = io_chapters_str.replace(end_str  , '')
    io_chapters_str = io_chapters_str.replace('%'      , '')

    if '' == all_chapters_str.strip():
        io_chapters_list = []
    else:
        io_chapters_list = [ch.strip() for ch in io_chapters_str.split(',')]
    del io_chapters_str

    include_chapters_list = get_includes()
    for ch in io_chapters_list:
        assert ch in include_chapters_list, (include_chapters_list, ch)
    del include_chapters_list

    return io_chapters_list




def set_includeonly(includeonly_chapters_list) -> list:
    '''
    Argument: list of chapters to include
    Returns : list of all available chapters of which "include_chapters_list"
                  will have been a subset
    '''
    assert isinstance(includeonly_chapters_list, list), \
        (includeonly_chapters_list, type(includeonly_chapters_list))

    assert 1 <= len(includeonly_chapters_list), len(includeonly_chapters_list)

    build_main_tex_file_path = get_build_main_tex_file_path()
    assert os.path.isfile(build_main_tex_file_path), build_main_tex_file_path

    with open(build_main_tex_file_path, 'rt') as build_main_tex_file:
        build_main_tex_str = build_main_tex_file.read()

    start_str = '\\includeonly{'
    end_str   = '}\n'

    start_idx = build_main_tex_str.index(start_str)
    end_idx   = build_main_tex_str.index(end_str, start_idx) + len(end_str)

    # pio: previous includeonly
    pio_chapters_str = build_main_tex_str[start_idx:end_idx]

    pio_chapters_str = pio_chapters_str.replace(start_str, '')
    pio_chapters_str = pio_chapters_str.replace(end_str  , '')
    pio_chapters_str = pio_chapters_str.replace('%'      , '')

    if '' == pio_chapters_str.strip():
        pio_chapters_list = []
    else:
        pio_chapters_list = [ch.strip() for ch in pio_chapters_str.split(',')]
    del pio_chapters_str

    include_chapters_list = get_includes()

    body_str = ''
    for ch in includeonly_chapters_list:
        assert ch in include_chapters_list, (include_chapters_list, ch)
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

    # pio_chapters_list: previous_includeonly_chapters_list
    return pio_chapters_list












