import sys
import os
import pprint

from .. import get_build_dir_path

from ..main.tex import get_includes



def get_project_tree() -> dict:

    # pt: project tree
    pt = dict()
   
 
    build_dir_path = get_build_dir_path()
    assert os.path.isdir(build_dir_path), build_dir_path


    includes = get_includes()

    assert isinstance(includes, list), (includes, type(includes))
    assert 1 <= len(includes), (includes, len(includes))

    # ch: chapter 
    for ch in includes:

        assert isinstance(ch, str), (ch, type(ch))
        
        # cdn: chapter dir name
        # cfn: chapter file name
        cdn__cfn = ch.split('/')
        assert 2 == len(cdn__cfn), (cdn__cfn, len(cdn__cfn))

        cdn, cfn = cdn__cfn
        del cdn__cfn

        assert cdn == cfn, (cdn, cfn)

        # cdp: chapter dir path
        cdp = os.path.join(build_dir_path, cdn)
        assert os.path.isdir(cdp), cdp

        # cfp: chapter file path
        cfp = ch_file_path = os.path.join(cdp, f'{cfn}.tex')
        assert os.path.isfile(cfp), cfp
        assert 0 < os.path.getsize(cfp), cfp

        # cf: chapter file
        with open(cfp, 'rt') as cf:
            ch_file_str = cf.read()
        del cf
        assert isinstance(ch_file_str, str), (ch_file_str, type(ch_file_str))
        assert 0 < len(ch_file_str), (ch_file_str, len(ch_file_str))
        if '\n' == ch_file_str[-1:]:
            ch_file_str = ch_file_str[:-1]

        ch_file_str = ch_file_str.replace('%\\input{', '\\input{')


        ch_file_lines = ch_file_str.split('\n')
        assert 1 < len(ch_file_lines), (ch_file_lines, len(ch_file_lines))

       
        begin_str = f'% BEGIN src/{cdn}/{cfn}.tex'
        assert begin_str == ch_file_lines[0], (ch_file_path, begin_str, ch_file_lines[0])
        del begin_str

        end_str = f'% END src/{cdn}/{cfn}.tex'
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
        del cl

        
        assert cfn not in pt, ([k for k in pt.keys()], cfn)
        pt[cfn] = \
            {
                'ch_file_path': cfp,
                'secs'        : dict()
            }
        
        for line_idx, line in enumerate(ch_file_lines[3:-1], start=3):

            assert isinstance(line, str), (line, type(line))

            if '' == line:
                continue

            assert '\\input{' == line[:7], (ch_file_path, line_idx, line[:7])
            assert '}' == line[-1:], (ch_file_path, line_idx, line[-1:])

            # ip: input path
            ip = line[7:-1]
            
            # ipc: input path components
            ipc = ip.split('/')
            assert len(ipc) in (2, 3), (ipc, len(ipc))

            # _cdn: chapter dir name
            _cdn = ipc.pop(0)
            assert cdn == _cdn, (ch_file_path, line_idx, cdn, _cdn)
            del _cdn

            if 1 == len(ipc):

                # sfn: section file name
                assert 'sfn' not in locals()
                sfn = ipc.pop(0)
                del ipc

                assert cfn != sfn, (cfn, sfn)

                assert '.tex' not in sfn, (ch_file_path, line_idx, line, sfn)
                assert 'sfn_tex' not in locals()
                sfn_tex = f'{sfn}.tex'

                # cdp: chapter dir path
                assert os.path.isdir(cdp), cdp

                # sfp: section file path
                assert 'sfp' not in locals()
                sfp = os.path.join(cdp, sfn_tex)
                del sfn_tex
                assert os.path.isfile(sfp), sfp
                assert 0 < os.path.getsize(sfp), sfp

                assert sfn not in pt[cfn]['secs'], sfn
                pt[cfn]['secs'][sfn] = \
                    {
                        'sec_is_leaf'  : True,
                        'sec_file_path': sfp,
                    }
                del sfn, sfp
            else:
                assert 2 == len(ipc), len(ipc)

                # sdn: section dir name 
                assert 'sdn' not in locals()
                sdn = ipc.pop(0)

                # sfn: section file name
                assert 'sfn' not in locals()
                sfn = ipc.pop(0)

                assert 0 == len(ipc), len(ipc)
                del ipc

                assert sdn == sfn, (sdn, sfn)


                assert '.tex' not in sfn, (ch_file_path, line_idx, line, sfn)
                assert 'sfn_tex' not in locals()
                sfn_tex = f'{sfn}.tex'


                assert os.path.isdir(cdp), cdp

                # cdp: chapter dir path
                # sdp: section dir path
                assert 'sdp' not in locals()
                sdp = os.path.join(cdp, sdn)
                assert os.path.isdir(sdp), sdp

                # sfp: section file path
                assert 'sfp' not in locals()
                sfp = os.path.join(sdp, sfn_tex)
                del sfn_tex
                assert os.path.isfile(sfp), sfp
                assert 0 < os.path.getsize(sfp)

                assert sfn not in pt[cfn]['secs'], sfn
                pt[cfn]['secs'][sfn] = \
                    {
                        'sec_is_leaf'  : False,
                        'sec_file_path': sfp,
                        'sec_dir_path' : sdp,
                        'subsecs'      : dict()
                    }
                del sdn, sfn, sdp, sfp

        del cdn, cfn


    # pt : project tree
    # cfn: chapter file name
    # cd : chapter dict
    assert 'cfn' not in locals()
    assert 'cd'  not in locals()
    for cfn, cd in pt.items():

        # cdn: chapter dir name
        cdn = cfn

        assert 2 == len(cd), len(cd)
        assert 'ch_file_path' in cd
        assert 'secs' in cd

        # sfn: section file name
        # sd : section dict
        assert 'sfn' not in locals()
        assert 'sd'  not in locals()
        for sfn, sd in cd['secs'].items():

            # sdn: section dir name
            sdn = sfn

            assert 2 <= len(sd), len(sd)
            assert len(sd) <= 4, len(sd)

            assert 'sec_is_leaf' in sd
            assert 'sec_file_path' in sd

            if sd['sec_is_leaf'] is True:

                assert 2 == len(sd), len(sd)

                del sfn, sd

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

            sec_str = sec_str.replace('%\\input{', '\\input{')
            
            sec_lines = sec_str.split('\n')
            assert 1 < len(sec_lines)
            
            begin_str = f'% BEGIN src/{cdn}/{sdn}/{sfn}.tex'
            assert begin_str == sec_lines[0], (sec_file_path, begin_str, sec_lines[0])
            del begin_str

            end_str = f'% END src/{cdn}/{sdn}/{sfn}.tex'
            assert end_str == sec_lines[-1], (sec_file_path, end_str, sec_lines[-1])
            del end_str

            assert '\\section{' == sec_lines[1][:9], (sec_file_path, sec_lines[1])
            assert '}' == sec_lines[1][-1:], (sec_file_path, sec_lines[1])

            assert '\\label{' == sec_lines[2][:7], (sec_file_path, sec_lines[2])
            assert '}' == sec_lines[2][-1:], (sec_file_path, sec_lines[2])

            # sl: section label
            sl = sec_lines[2][7:-1]
            del sl

            for line_idx, line in enumerate(sec_lines[3:-1], start=3):
                
                assert isinstance(line, str), (line, type(line))

                if '' == line:
                    continue

                
                assert '\\input{' == line[:7], (sec_file_path, line_idx, line, line[:7])
                assert '}' == line[-1:], (sec_file_path, line_idx, line, line[-1:])

                # ip: input path
                ip = line[7:-1]
                
                # ipc: input path components
                ipc = ip.split('/')
                assert len(ipc) in (3, 4), (ipc, len(ipc))

                # _cdn: chapter dir name
                assert '_cdn' not in locals()
                _cdn = ipc.pop(0)
                assert cdn == _cdn, (sec_file_path, line_idx, line, cdn, _cdn)
                del _cdn

                
                # _sdn: section dir name 
                assert '_sdn' not in locals()
                _sdn = ipc.pop(0)
                assert sdn == _sdn, (sec_file_path, line_idx, line, sdn, _sdn)
                del _sdn

                if 1 == len(ipc):

                    # ssfn: subsection file name
                    assert 'ssfn' not in locals()
                    ssfn = ipc.pop(0)

                    assert 0 == len(ipc), len(ipc)
                    del ipc


                    assert '.tex' not in ssfn, (sec_file_path, line_idx, line, ssfn)
                    assert 'ssfn_tex' not in locals()
                    ssfn_tex = f'{ssfn}.tex'


                    assert os.path.isdir(sec_dir_path), sec_dir_path

                    # ssfp: subsection file path
                    assert 'ssfp' not in locals()
                    ssfp = os.path.join(sec_dir_path, ssfn_tex)
                    del ssfn_tex
                    assert os.path.isfile(ssfp), (sec_file_path, line_idx, line, ssfp)
                    assert 0 < os.path.getsize(ssfp), (sec_file_path, line_idx, line, ssfp)

                    assert ssfn not in subsecs, ([k in subsecs.keys()], ssfn)
                    subsecs[ssfn] = \
                        {
                            'subsec_is_leaf'  : True,
                            'subsec_file_path': ssfp
                        }
                    del ssfn, ssfp

                else:
                    assert 2 == len(ipc)

                    # ssdn: subsection dir name
                    assert 'ssdn' not in locals()
                    ssdn = ipc.pop(0)

                    # ssfn: subsection file name
                    assert 'ssfn' not in locals()
                    ssfn = ipc.pop(0)

                    assert 0 == len(ipc), len(ipc)
                    del ipc

                    assert '.tex' not in ssfn, (sec_file_path, line_idx, line, ssfn)
                    assert 'ssfn_tex' not in locals()
                    ssfn_tex = f'{ssfn}.tex'
                    
                    
                    assert os.path.isdir(sec_dir_path), sec_dir_path

                    # ssdp: subsection dir path
                    assert 'ssdp' not in locals()
                    ssdp = os.path.join(sec_dir_path, ssdn)
                    
                    assert os.path.isdir(ssdp), ssdp

                    # ssfp: subsection file path
                    assert 'ssfp' not in locals()
                    ssfp = os.path.join(ssdp, ssfn_tex)
                    del ssfn_tex
                    assert os.path.isfile(ssfp), ssfp
                    assert 0 < os.path.getsize(ssfp), ssfp

                    assert ssfn not in subsecs, ([k in subsecs.keys()], ssfn)
                    subsecs[ssfn] = \
                        {
                            'subsec_is_leaf'  : False,
                            'subsec_file_path': ssfp,
                            'subsec_dir_path' : ssdp,
                            'subsubsecs'      : dict(),
                        }
                    del ssdn, ssfn, ssdp, ssfp

            del sfn, sd

    assert isinstance(pt, dict), (pt, type(pt))
    assert 1 <= len(pt), (pt, len(pt))

    return pt



def main() -> int:
    pprint.pprint(get_project_tree())
    return 0



if '__main__' == __name__:
    sys.exit(main())





