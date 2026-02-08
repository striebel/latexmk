import sys
import os
import pprint

from ... import get_build_dir_path

from ...main.tex import get_includes

from .. import INIT


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

        assert isinstance(cdn, str), type(cdn)
        assert isinstance(cfn, str), type(cfn)
        assert 0 < len(cdn)
        assert 0 < len(cfn)
        assert INIT == cfn, (INIT, cfn)

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


        # pt : project tree
        # cfn: chapter file name
        assert cdn not in pt, ([k for k in pt.keys()], cdn)
        pt[cdn] = \
            {
                'ch_is_leaf'  : False,
                'ch_file_path': cfp,
                'ch_dir_path' : cdp,
                'secs'        : dict(),
            }
        
        for line_idx, line in enumerate(ch_file_lines[3:-1], start=3):

            assert isinstance(line, str), (line, type(line))

            if '' == line:
                continue

            assert '\\input{' == line[:7], (ch_file_path, line_idx, line[:7])
            assert '}' == line[-1:], (ch_file_path, line_idx, line[-1:])

            # ip: input path
            assert 'ip' not in locals()
            ip = line[7:-1]
            
            # ipc: input path components
            ipc = ip.split('/')
            del ip
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
                
                
                assert sfn not in pt[cdn]['secs'], sfn
                pt[cdn]['secs'][sfn] = \
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

                assert isinstance(sdn, str), type(sdn)
                assert isinstance(sfn, str), type(sfn)
                assert 0 < len(sdn)
                assert 0 < len(sfn)
                assert INIT == sfn, (INIT, sfn)

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

                assert sdn not in pt[cdn]['secs'], sdn
                pt[cdn]['secs'][sdn] = \
                    {
                        'sec_is_leaf'  : False,
                        'sec_file_path': sfp,
                        'sec_dir_path' : sdp,
                        'subsecs'      : dict()
                    }
                del sdn, sfn, sdp, sfp

        del cfp
        del cdn, cfn


    # pt : project tree
    # cn : chapter      name
    # cdn: chapter dir  name
    # cfn: chapter file name
    # cd : chapter dict
    # sn : section      name
    # sdn: section dir  name
    # sfn: section file name
    assert 'pt'      in locals()
    assert 'cn'  not in locals()
    assert 'cdn' not in locals()
    assert 'cfn' not in locals()
    assert 'cd'  not in locals()
    assert 'sn'  not in locals()
    assert 'sdn' not in locals()
    assert 'sfn' not in locals()
    for cn, cd in pt.items():
#   BEGIN for cn, cd in pt.items()
#   {
        assert isinstance(cn, str), type(cn)
        assert isinstance(cd, dict), type(cd)
        assert 4 == len(cd), [k for k in cd]
        assert 'ch_is_leaf'   in cd
        assert 'ch_file_path' in cd
        assert 'ch_dir_path'  in cd
        assert 'secs'         in cd

        # sn: section name
        # sd: section dict
        assert 'sn' not in locals()
        assert 'sd'  not in locals()
        for sn, sd in cd['secs'].items():
#       BEGIN for sn, sd in cd['secs'].items()
#       {
            assert len(sd) in (2, 4), len(sd)

            assert 'sec_is_leaf' in sd
            assert 'sec_file_path' in sd

            if sd['sec_is_leaf'] is True:

                assert 2 == len(sd), len(sd)

                del sn, sd

                continue

            assert sd['sec_is_leaf'] is False

            assert 4 == len(sd), len(sd)

            assert 'sec_dir_path' in sd
            assert 'subsecs' in sd

            sec_file_path = sd['sec_file_path']
            sec_dir_path  = sd['sec_dir_path' ]
            subsecs       = sd['subsecs'      ]
            del sd

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
            
            begin_str = f'% BEGIN src/{cn}/{sn}/{INIT}.tex'
            assert begin_str == sec_lines[0], (sec_file_path, begin_str, sec_lines[0])
            del begin_str

            end_str = f'% END src/{cn}/{sn}/{INIT}.tex'
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
#           BEGIN for line in sec init file
#           {
                assert isinstance(line, str), (line, type(line))

                if '' == line:
                    continue

                
                assert '\\input{' == line[:7], (sec_file_path, line_idx, line, line[:7])
                assert '}' == line[-1:], (sec_file_path, line_idx, line, line[-1:])

                # ip: input path
                assert 'ip' not in locals()
                ip = line[7:-1]
                
                # ipc: input path components
                ipc = ip.split('/')
                del ip
                assert len(ipc) in (3, 4), (ipc, len(ipc))

                # _cdn: chapter dir name
                assert '_cdn' not in locals()
                _cdn = ipc.pop(0)
                assert cn == _cdn, (sec_file_path, line_idx, line, cn, _cdn)
                del _cdn

                
                # _sdn: section dir name 
                assert '_sdn' not in locals()
                _sdn = ipc.pop(0)
                assert sn == _sdn, (sec_file_path, line_idx, line, sn, _sdn)
                del _sdn

                if 1 == len(ipc):
#               BEGIN case where subsec is leaf
#               {
                    # ssn : subsection      name
                    # ssfn: subsection file name
                    assert 'ssn'  not in locals()
                    assert 'ssfn' not in locals()
                    ssfn = ipc.pop(0)

                    assert 0 == len(ipc), len(ipc)
                    del ipc


                    assert '.tex' not in ssfn, (sec_file_path, line_idx, line, ssn)
                    assert 'ssn'      not in locals()
                    assert 'ssfn'         in locals()
                    assert 'ssn_tex'  not in locals()
                    assert 'ssfn_tex' not in locals()
                    ssfn_tex = f'{ssfn}.tex'
                    
                    # ssn: subsection name
                    ssn = ssfn
                    del ssfn

                    assert os.path.isdir(sec_dir_path), sec_dir_path

                    # ssfp: subsection file path
                    assert 'ssfp' not in locals()
                    ssfp = os.path.join(sec_dir_path, ssfn_tex)
                    del ssfn_tex
                    assert os.path.isfile(ssfp), (sec_file_path, line_idx, line, ssfp)
                    assert 0 < os.path.getsize(ssfp), (sec_file_path, line_idx, line, ssfp)
                    
                    assert ssn not in subsecs, ([k for k in subsecs.keys()], ssn)
                    subsecs[ssn] = \
                        {
                            'subsec_is_leaf'  : True,
                            'subsec_file_path': ssfp
                        }
                    del ssn, ssfp

#               }
#               END case where subsec is leaf
                else:
                    assert 2 == len(ipc)
#               BEGIN case where subsec is *not* leaf
#               {
                    # ssn : subsection     name
                    # ssdn: subsection dir name
                    assert 'ssn'  not in locals()
                    assert 'ssdn' not in locals()
                    ssdn = ipc.pop(0)

                    # ssn : subsection      name
                    # ssfn: subsection file name
                    assert 'ssn'  not in locals()
                    assert 'ssfn' not in locals()
                    ssfn = ipc.pop(0)

                    assert 0 == len(ipc), len(ipc)
                    del ipc


                    assert isinstance(ssdn, str), type(ssdn)
                    assert isinstance(ssfn, str), type(ssfn)
                    assert 0 < len(ssdn)
                    assert 0 < len(ssfn)
                    assert INIT == ssfn, (INIT, ssfn)


                    assert '.tex' not in ssfn, (sec_file_path, line_idx, line, ssfn)
                    assert 'ssfn_tex' not in locals()
                    ssfn_tex = f'{ssfn}.tex'
                    del ssfn

                    
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


                    assert 'ssn'  not in locals()
                    assert 'ssdn'     in locals()
                    ssn = ssdn
                    del ssdn


                    assert ssn not in subsecs, ([k for k in subsecs.keys()], ssn)
                    subsecs[ssn] = \
                        {
                            'subsec_is_leaf'  : False,
                            'subsec_file_path': ssfp,
                            'subsec_dir_path' : ssdp,
                            'subsubsecs'      : dict(),
                        }
                    del ssn, ssdp, ssfp
#               }
#               END case where subsec is *not* leaf

#           }
#           END for line in sec init file

            del sn
#       }
#       END for sn, sd in cd['secs'].items()

        del cn,cd

#   }
#   END for cn, cd in pt.items()



    #BEGIN level-order tree traversal

    # lhs : [current-]level headings
    # nlhs: next-level      headings
    # hn  : heading name
    # hd  : heading dict
    assert 'lhs'  not in locals()
    assert 'nlhs' not in locals()
    lhs  = [(hn,hd) for hn,hd in pt.items()]
    nlhs = []

    # lsn: level short name
    # lln: level long  name
    assert 'lsn_lln' not in locals()
    lsn_lln = \
        (
            ('ch'       , 'chapter'      ),
            ('sec'      , 'section'      ),
            ('subsec'   , 'subsection'   ),
            ('subsubsec', 'subsubsection'),
            ('par'      , 'paragraph'    ),
            ('subpar'   , 'subparagraph' ),
            ('subsubpar', None           ),
        )

    #   li:      [current]level index
    #   sn:      [current level] short name
    #   ln:      [current level] long  name
    #  nsn:      next    [level] short name
    #  nln:      next    [level] long  name
    # nnsn: next next    [level] short name
    # nnln: next next    [level] long  name
    assert   'sn' not in locals()
    assert   'ln' not in locals()
    assert  'nsn' not in locals()
    assert  'nln' not in locals()
    assert 'nnsn' not in locals()
    assert 'nnln' not in locals()
    for li,((sn,ln),(nsn,nln),(nnsn,nnln)) in enumerate(
        zip(lsn_lln,lsn_lln[1:],lsn_lln[2:])
    ):
#   BEGIN for each level
#   {
        # hn : heading name
        # hd : heading dict
        # lhs: [current-]level headings
        assert 'hn' not in locals()
        assert 'hd' not in locals()
        for hn, hd in lhs:
#       BEGIN for each heading at current level
#       {
            # fpk: file path key
            assert 'fpk' not in locals()
            fpk = f'{sn}_file_path'
            assert fpk in hd, ([k for k in hd], fpk)

            # fp: file path
            fp = hd[fpk]
            del fpk
            assert isinstance(fp, str)    , (csn, hn, type(fp))
            assert os.path.isfile(fp)     , (csn, hn, fp)
            assert 0 < os.path.getsize(fp), (csn, hn, fp)
            del fp

            # ilk: is leaf key
            assert 'ilk' not in locals()
            ilk = f'{sn}_is_leaf'
            assert ilk in hd, ([k for k in hd], ilk)

            # il: is leaf
            il = hd[ilk]
            del ilk
            if il is True:
                del il
                assert 2 == len(hd), len(hd)

                del hn, hd

                continue
            assert il is False, il
            del il
            
            assert 4 == len(hd), len(hd)
            
            # dpk: dir path key
            assert 'dpk' not in locals()
            dpk = f'{sn}_dir_path'
            assert dpk in hd, ([k for k in hd], dpk)
            
            # dp: dir path
            assert 'dp' not in locals()
            dp = hd[dpk]
            del dpk
            assert isinstance(dp, str)     , (csn, hn, type(dp))
            assert os.path.isdir(dp)       , (csn, hn, dp)
            assert 2 <= len(os.listdir(dp)), (csn, hn, dp)
            
            #   hn   :          heading name
            # onhn   : one next heading name
            #   hd   :          heading dict
            # onhd   : one next heading dict
            #  nhscd :     next headings container dict
            #  nhscdk:     next headings container dict key
            assert 'nhscdk' not in locals()
            nhscdk = f'{nsn}s'
            assert nhscdk in hd, (csn, hn, [k for k in hd], nhscdk)
            
            # nhd: next heading dict
            assert 'nhd' not in locals()
            nhscd = hd[nhscdk]
            del nhscdk
            assert isinstance(nhscd, dict), (csn, hn, type(nhscd))
            
            if 0 < len(nhscd):
                assert nsn in ('sec', 'subsec'), nsn
                assert 1 <= len(nhscd)
                assert len(nhscd) <= len(os.listdir(dp)) - 1
#           BEGIN case where next level has already been added
#                 to the project tree
#           {
                pass
#           }
#           END case where next level has already been added
#               to the project tree
            else:
                assert 0 == len(nhscd)
                assert nsn in ('subsubsec', 'par', 'subpar')
#           BEGIN case where next level has *not* been added
#                 to the project tree
#           {
                assert 1 == os.listdir(dp).count(f'{INIT}.tex')
                
                # cn: child name
                assert 'cn' not in locals(), cn
                for cn in os.listdir(dp):
                    if f'{INIT}.tex' == cn:
                        del cn
                        continue

                    # cp: child path
                    assert 'cp' not in locals()
                    cp = os.path.join(dp, cn)
                    if os.path.isfile(cp) and '.tex' != cp[-4:]:
                        del cn
                        del cp
                        continue
#               BEGIN for each sub heading in the heading dir
#               {
                    if os.path.isfile(cp):
                        assert '.tex' == cp[-4:], cp

                        # onhn: one next heading name
                        # onhd: one next heading dict
                        assert cn[:-4] not in nhscd
                        nhscd[cn[:-4]] = \
                            {
                                f'{nsn}_is_leaf'  : True,
                                f'{nsn}_file_path': cp,
                            }
                    else:
                        assert os.path.isdir(cp)

                        # cfp: child file path
                        assert 'cfp' not in locals()
                        cfp = os.path.join(cp, f'{INIT}.tex')
                        assert os.path.isfile(cfp), cfp

                        assert cn not in nhscd
                        nhscd[cn] = \
                            {
                                f'{nsn}_is_leaf'  : False,
                                f'{nsn}_file_path': cfp,
                                f'{nsn}_dir_path' : cp,
                                f'{nnsn}s'        : dict(),
                            }
                        del cfp

                    del cp
                    del cn
#               }
#               END for each sub heading in the heading dir

#           }
#           END case where next level has *not* been added
#               to the project tree

            assert 1 <= len(nhscd)
            assert len(nhscd) <= len(os.listdir(dp)) - 1

            #BEGIN add each next-level heading to the
            #      next-level headings list

            # onhn   : one next heading name
            # onhd   : one next heading dict
            #  nhscd :     next headings container dict
            # nlhs   : next-level headings
            assert 'onhn'   not in locals()
            assert 'onhd'   not in locals()
            assert  'nhscd'     in locals()
            assert 'nlhs'       in locals()
            for onhn, onhd in nhscd.items():
                assert isinstance(onhn, str)
                assert isinstance(onhd, dict)
                nlhs.append((onhn,onhd))
                del onhn, onhd

            #END add each next-level heading to the
            #    next-level headings list


            #BEGIN confirm that the contents of the
            #      next headings container dict matches
            #      the init file in the current heading dir

            # fp: file path
            # dp: dir  path
            assert 'fp' not in locals()
            assert 'dp'     in locals()
            fp = os.path.join(dp, f'{INIT}.tex')
            assert os.path.isfile(fp), (sn,hn,fp)

            # fo : file object
            # fls: file lines
            assert 'fo'  not in locals() 
            assert 'fls' not in locals()
            with open(fp, 'rt') as fo:
                fls = [fl for fl in fo]
            del fo
            assert isinstance(fls, list), type(fls)
            assert 5 <= len(fls)
            assert 'fl' not in locals()
            for fl in fls:
                assert isinstance(fl, str), type(fl)
                del fl

            assert '% BEGIN src/' == fls[ 0][:len('% BEGIN src/')], fls[ 0]
            assert '% END src/'   == fls[-1][:len('% END src/'  )], fls[-1]

            assert f'/{INIT}.tex\n' == fls[ 0][-len(f'/{INIT}.tex\n'):], fls[ 0]
            assert f'/{INIT}.tex\n' == fls[-1][-len(f'/{INIT}.tex\n'):], fls[-1]
            
            # ln: [current level] long name 
            assert f'\\{ln}{{' == fls[1][:len(f'\\{ln}{{')], fls[1]
            assert '}\n'       == fls[1][-2:]              , fls[1]
            
            assert '\\label{' == fls[2][:len('\\label{')], fls[2]
            assert '}\n'      == fls[2][-2:]             , fls[2]


            # nhscd: next headings container dict
            # ips  : input paths
            assert 'ips' not in locals()
            ips = []

            # fls: file lines
            # fl : file line
            assert 'fl' not in locals()
            for fl in fls[3:-1]:
                if '\n' == fl:
                    del fl
                    continue
                #
                assert '\\input{' == fl[           :len('\\input{')], fl
                assert '}\n'      == fl[-len('}\n'):               ], fl

                # ip: input path
                assert 'ip' not in locals(), ip
                ip = fl[len('\\input{'):-len('}\n')]

                ips.append(ip)
                del ip

                del fl
            del fls

            assert len(ips) == len(nhscd), (len(ips), len(nhscd))
            del ips, nhscd

            #END confirm that the contents of the
            #    next headings container dict matches
            #    the init file in the current heading dir

            del dp
            del hn, hd
#       }
#       END for each heading at current level

        lhs = nlhs
        nlhs = []
        
        del li,sn,ln,nsn,nln,nnsn,nnln
#   }
#   END for each level

    #END level-order tree traversal

    assert isinstance(pt, dict), (pt, type(pt))
    assert 1 <= len(pt), (pt, len(pt))

    return pt



def main() -> int:
    pprint.pprint(get_project_tree())
    return 0



if '__main__' == __name__:
    sys.exit(main())





