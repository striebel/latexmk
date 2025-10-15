import sys
import os
import pprint

from . import get_build_dir_path

from .main.tex import get_includeonly



def get_project_tree() -> dict:

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
        if '\n' == ch_file_str[-1:]:
            ch_file_str = ch_file_str[:-1]

        ch_file_lines = ch_file_str.split('\n')
        assert 1 < len(ch_file_lines), (ch_file_lines, len(ch_file_lines))

       
        begin_str = f'% BEGIN src/{dn}/{fn}.tex'
        assert begin_str == ch_file_lines[0], (ch_file_path, begin_str, ch_file_lines[0])
        del begin_str

        end_str = f'% END src/{dn}/{fn}.tex'
        assert end_str == ch_file_lines[-1], (ch_file_path, end_str, ch_file_lines[-1])
        if end_str != ch_file_lines[-1]:
            sys.stderr.write(f'end_str != ch_file_lines[-1]\n')
            sys.stderr.write(ch_file_str)
            sys.exit(3)


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
        
        assert cn not in pt, ([k in pt.keys()], cn)
        pt[cn] = \
            {
                'ch_file_path': ch_file_path,
                'secs'        : dict()
            }
        
        for line_idx, line in enumerate(ch_file_lines[3:-1], start=3):

            assert isinstance(line, str), (line, type(line))

            if '' == line:
                continue

            elif '%' == line[:1]:
                assert '\\input{' not in line, (ch_file_path, line_idx, line)
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
                _sfn_tex = f'{_sfn}.tex'

                assert os.path.isdir(ch_dir_path), ch_dir_path
                # _sfp: sub file path
                _sfp = os.path.join(ch_dir_path, _sfn_tex)
                del _sfn_tex
                assert os.path.isfile(_sfp), _sfp
                assert 0 < os.path.getsize(_sfp), _sfp

                assert _sfn not in pt[cn]['secs'], _sfn
                pt[cn]['secs'][_sfn] = \
                    {
                        'sec_is_leaf'  : True,
                        'sec_file_path': _sfp,
                    }
                del _sfn, _sfp
            else:
                assert 2 == len(ipc), len(ipc)

                # _sdn: sub dir name 
                _sdn = ipc.pop(0)

                # _sfn: sub file name
                _sfn = ipc.pop(0)

                assert 0 == len(ipc), len(ipc)
                del ipc

                assert '.tex' not in _sfn, (ch_file_path, line_idx, line, _sfn)
                _sfn_tex = f'{_sfn}.tex'
                del _sfn

                assert os.path.isdir(ch_dir_path), ch_dir_path
                # _sdp: sub dir path
                _sdp = os.path.join(ch_dir_path, _sdn)
                assert os.path.isdir(_sdp), _sdp

                # _sfp: sub file path
                _sfp = os.path.join(_sdp, _sfn_tex)
                del _sfn_tex
                assert os.path.isfile(_sfp), _sfp
                assert 0 < os.path.getsize(_sfp)

                assert _sdn not in pt[cn]['secs'], _sdn
                pt[cn]['secs'][_sdn] = \
                    {
                        'sec_is_leaf'  : False,
                        'sec_file_path': _sfp,
                        'sec_dir_path' : _sdp,
                        'subsecs'      : dict()
                    }
                del _sdn, _sfp

    # pt: project tree
    # cn: chapter name
    # cd: chapter dict
    for cn, cd in pt.items():

        assert 2 == len(cd), len(cd)
        assert 'ch_file_path' in cd
        assert 'secs' in cd

        # sn: section name
        # sd: section dict
        for sn, sd in cd['secs'].items():

            assert 2 <= len(sd), len(sd)
            assert len(sd) <= 4, len(sd)

            assert 'sec_is_leaf' in sd
            assert 'sec_file_path' in sd

            if sd['sec_is_leaf'] is True:

                assert 2 == len(sd), len(sd)
                continue

            assert sd['sec_is_leaf'] is False

            assert 4 == len(sd), len(sd)

            assert 'sec_dir_path' in sd
            assert 'subsecs' in sd

            sec_file_path = sd['sec_file_path']
            sec_dir_path  = sd['sec_dir_path' ]
            subsecs       = sd['subsecs'      ]

            assert isinstance(subsecs, dict), (subsecs, type(subsecs))
            assert 0 == len(subsecs), len(subsecs)
            
            
            assert os.path.isfile(sec_file_path), sec_file_path
            assert 0 < os.path.getsize(sec_file_path), sec_file_path
            with open(sec_file_path, 'rt') as sec_file:
                sec_str = sec_file.read()
            del sec_file
            assert 0 < len(sec_str)
            if '\n' == sec_str[-1:]:
                sec_str = sec_str[:-1]
            
            sec_lines = sec_str.split('\n')
            assert 1 < len(sec_lines)
            
            begin_str = f'% BEGIN src/{cn}/{sn}/{sn}.tex'
            assert begin_str == sec_lines[0], (sec_file_path, begin_str, sec_lines[0])
            del begin_str

            end_str = f'% END src/{cn}/{sn}/{sn}.tex'
            assert end_str == sec_lines[-1], (sec_file_path, end_str, sec_lines[-1])
            del end_str

            assert '\\section{' == sec_lines[1][:9], (sec_file_path, sec_lines[1])
            assert '}' == sec_lines[1][-1:], (sec_file_path, sec_lines[1])

            assert '\\label{' == sec_lines[2][:7], (sec_file_path, sec_lines[2])
            assert '}' == sec_lines[2][-1:], (sec_file_path, sec_lines[2])

            # sl: section label
            sl = sec_lines[2][7:-1]
            assert 2 == sl.count(':')

            # slc: section label components
            slc = sl.split(':')
            assert 3 == len(slc), (sec_file_path, slc, len(slc))
            assert 'sec' == slc[0], (sec_file_path, sl, slc[0])
            assert cn    == slc[1], (sec_file_path, cn, sl, slc[1])
            assert sn    == f'{cn}{slc[2]}', (sec_file_path, sn, sl, slc[2])
            del sl, slc

            for line_idx, line in enumerate(sec_lines[3:-1], start=3):
                
                assert isinstance(line, str), (line, type(line))

                if '' == line:
                    continue

                elif '%' == line[:1]:
                    assert '\\input{' not in line, (sec_file_path, line_idx, line)
                    continue
                
                assert '\\input{' == line[:7], (sec_file_path, line_idx, line, line[:7])
                assert '}' == line[-1:], (sec_file_path, line_idx, line, line[-1:])

                # ip: input path
                ip = line[7:-1]
                
                # ipc: input path components
                ipc = ip.split('/')
                assert 3 == len(ipc), (ipc, len(ipc))

                # _cdn: chapter dir name
                _cdn = ipc.pop(0)
                assert dn == _cdn, (sec_file_path, line_idx, line, dn, _cdn)
                del _cdn

                # _sdn: section dir name 
                _sdn = ipc.pop(0)
                del _sdn

                # _ssfn: subsection file name
                _ssfn = ipc.pop(0)

                assert 0 == len(ipc), len(ipc)
                del ipc


                assert '.tex' not in _ssfn, (sec_file_path, line_idx, line, _ssfn)
                _ssfn_tex = f'{_ssfn}.tex'

                assert os.path.isdir(sec_dir_path), sec_dir_path
                # _ssfp: subsection file path
                _ssfp = os.path.join(sec_dir_path, _ssfn_tex)
                assert os.path.isfile(_ssfp), (sec_file_path, line_idx, line, _ssfp)
                assert 0 < os.path.getsize(_ssfp), (sec_file_path, line_idx, line, _ssfp)

                assert _ssfn not in sd, ([k in sd.keys()], _ssfn)
                sd[_ssfn] = \
                    {
                        'subsec_is_leaf'  : True,
                        'subsec_file_path': _ssfp
                    }
                del _ssfn, _ssfp

    assert isinstance(pt, dict), (pt, type(pt))
    assert 1 <= len(pt), (pt, len(pt))

    return pt



def main() -> int:
    pprint.pprint(get_project_tree())
    return 0



if '__main__' == __name__:
    sys.exit(main())





