import sys
import os
import pprint

from . import get_build_dir_path

from .main.tex import get_includeonly



def traverse() -> dict:

    # pt: project tree
    pt = dict()
   
 
    build_dir_path = get_build_dir_path()
    assert os.path.isdir(build_dir_path), build_dir_path


    # io: includeonly 
    io = get_includeonly()

    assert isinstance(io, list), (io, type(io))
    assert 1 <= len(io), (io, len(io))
    
    # ch: chapter 
    for ch in io:

        assert isinstance(ch, str), (ch, type(ch))
        
        # dn: dir name
        # fn: file name
        dn__fn = ch.split('/')
        assert 2 == len(dn__fn), (dn__fn, len(dn__fn))

        dn, fn = dn__fn
        del dn__fn

        assert dn == fn, (dn, fn)

        ch_dir_path = os.path.join(build_dir_path, dn)
        assert os.path.isdir(ch_dir_path), ch_dir_path

        ch_file_path = os.path.join(ch_dir_path, f'{fn}.tex')
        assert os.path.isfile(ch_file_path), ch_file_path
        assert 0 < os.path.getsize(ch_file_path), ch_file_path

        with open(ch_file_path, 'rt') as ch_file:
            ch_file_str = ch_file.read()
        del ch_file
        assert isinstance(ch_file_str, str), (ch_file_str, type(ch_file_str))
        assert 0 < len(ch_file_str), (ch_file_str, len(ch_file_str))

        ch_file_lines = ch_file_str.split('\n')
        assert 1 < len(ch_file_lines), (ch_file_lines, len(ch_file_lines))

       
        begin_str = f'% BEGIN src/{dn}/{fn}.tex'
        assert begin_str == ch_file_lines[0], (begin_str, ch_file_lines[0])
        del begin_str

        end_str = f'% END src/{dn}/{fn}.tex'
        assert end_str == ch_file_lines[-1], (end_str, ch_file_lines[-1])

        assert '\\chapter{' == ch_file_lines[1][:9], ch_file_lines[1][:9]
        assert '}' == ch_file_lines[1][-1:], ch_file_lines[1][-1:]

        assert '\\label{' == ch_file_lines[2][:7], ch_file_lines[2][:7]
        assert '}' == ch_file_lines[2][-1:], ch_file_lines[2][-1:]
        # cl: chapter label
        cl = ch_file_lines[2][7:-1]

        assert 'sec:' == cl[:4], cl[:4]
        
        # cn: chapter name
        cn = cl[4:]
        assert fn == cn, (ch_file_path, fn, cn)
        
        
        for line_idx, line in enumerate(ch_file_lines[3:-1], start=3):

            assert isinstance(line, str), (line, type(line))

            if '' == line:
                continue
            elif '%' == line[:1]:
                continue
            
            assert '\\input{' == line[:7], (ch_file_path, line_idx, line[:7])
            assert '}' == line[-1:], (ch_file_path, line_idx, line[-1:])

            # ip: input path
            ip = line[7:-1]
            
            # ipc: input path components
            ipc = ip.split('/')
            assert len(ipc) in (2, 3), (ipc, len(ipc))

            # _dn: dir name
            _dn = ipc.pop(0)
            assert dn == _dn, (ch_file_path, line_idx, dn, _dn)
            del _dn

            if 1 == len(ipc):

                # _sfn: sub file name
                _sfn = ipc.pop(0)
                del ipc

                assert fn != _sfn, (fn, _sfn)

                assert '.tex' not in _sfn, (ch_file_path, line_idx, line, _sfn)
                _sfn = f'{_sfn}.tex'

                assert os.path.isdir(ch_dir_path), ch_dir_path
                # _sfp: sub file path
                _sfp = os.path.join(ch_dir_path, _sfn)
                del _sfn
                assert os.path.isfile(_sfp), _sfp
                assert 0 < os.path.getsize(_sfp), _sfp
                del _sfp

            else:
                assert 2 == len(ipc), len(ipc)

                # sdn: sub dir name 
                _sdn = ipc.pop(0)

                # 

        
        print(ch_file_path) 
        for l in ch_file_lines:
            print(l)

        sys.exit(33)

    return project_tree


def main() -> int:
    pprint.pprint(traverse())
    return 0


if '__main__' == __name__:
    sys.exit(main())





