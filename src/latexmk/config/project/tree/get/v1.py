# In this version (v1), the get_project_tree function is 500 lines
# as opposed to 750 lines in the previous version (v0).
# Also, in this version the subheadings of each parent are given
# as a list, as opposed to a dict in the previous version.
# So in this version the ordering of headings is preserved explicitly.

import sys
import os
import pprint

from ... import get_build_dir_path

from ...main.tex import get_includes

from .. import INIT


def get_project_tree() -> list:

    # ptl: project tree list
    ptl = []
    
    
    build_dir_path = get_build_dir_path()
    assert os.path.isdir(build_dir_path), build_dir_path


    includes = get_includes()

    assert isinstance(includes, list), (includes, type(includes))
    assert 1 <= len(includes), (includes, len(includes))

    # ip: include path
    assert 'ip' not in locals()
    for ip in includes:

        assert isinstance(ip, str), type(ip)
        assert 0 < len(ip)
        # ipc: include path components
        ipc = ip.split('/')
        del ip

        assert isinstance(ipc, list), type(ipc)
        assert 2 == len(ipc), len(ipc)
        # cn: chapter name
        # nn: init name
        assert 'cn' not in locals()
        assert 'nn' not in locals()
        cn,nn = ipc
        del ipc

        assert isinstance(cn, str), type(cn)
        assert isinstance(nn, str), type(nn)
        assert 0 < len(cn)
        assert 0 < len(nn)
        assert INIT == nn, (INIT, nn)
        del nn
        
        # cfp: chapter file path
        assert 'cfp' not in locals()
        cfp = os.path.join(build_dir_path, cn, f'{INIT}.tex')
        assert os.path.isfile(cfp), cfp

        # cdp: chapter dir path
        assert 'cdp' not in locals()
        cdp = os.path.join(build_dir_path, cn)
        assert os.path.isdir(cdp), cdp

        # cd: chapter dict
        assert 'cd' not in locals()
        cd = \
            {
                'ch_is_leaf'  : False,
                'ch_file_path': cfp,
                'ch_dir_path' : cdp,
                'secs'        : [],
            }
        del cfp,cdp
        ptl.append((cn,cd))
        del cn,cd


    #BEGIN level-order tree traversal

    # lhs : [current-]level headings
    # nlhs: next-level      headings
    # hipp: partial heading input path
    # hd  : heading dict
    assert 'lhs'  not in locals()
    assert 'nlhs' not in locals()
    # ptl: project tree list
    lhs  = [(hipp,hd) for hipp,hd in ptl]
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
    for (sn,ln),(nsn,nln),(nnsn,nnln) in \
        zip(lsn_lln,lsn_lln[1:],lsn_lln[2:]):
#   BEGIN for each level
#   {
        # hipp: heading input path, partial
        # hd  : heading dict
        # lhs : [current-]level headings
        assert 'hipp' not in locals()
        assert 'hd'   not in locals()
        for hipp, hd in lhs:
#       BEGIN for each heading at current level
#       {
            # fpk: file path key
            assert 'fpk' not in locals()
            fpk = f'{sn}_file_path'
            assert fpk in hd, ([k for k in hd], fpk)

            # hfp: heading file path
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

                del hipp, hd

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
            assert isinstance(dp, str)     , (csn, hipp, type(dp))
            assert os.path.isdir(dp)       , (csn, hipp, dp)
            assert 2 <= len(os.listdir(dp)), (csn, hipp, dp)
            
            #   hipp :          heading input path, partial
            # onhipp : one next heading input path, partial
            #   hd   :          heading dict
            # onhd   : one next heading dict
            #  nhscl :     next headings container list       
            #  nhsclk:     next headings container list key
            assert 'nhsclk' not in locals()
            nhsclk = f'{nsn}s'
            assert nhsclk in hd, (csn, hipp, [k for k in hd], nhsclk)
            
            assert 'nhscl' not in locals()
            nhscl = hd[nhsclk]
            assert isinstance(nhscl, list), (sn, hipp, nhsclk, type(nhscl))
            assert 0 == len(nhscl)
            del nhsclk



            #BEGIN read the init file for the current heading
            #      and add each of the input macro paths to the
            #      nhscl (next headings container list)
            #      and the
            #      nlhs (next-level headings [list])


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


            # nhscl: next headings container dict
            # ips  : input paths
            assert 'ips' not in locals()
            ips = []

            STATE_SEEK_HEADING = 'state_seek_heading'
            STATE_SEEK_LABEL   = 'state_seek_label'
            STATE_SEEK_INPUT   = 'state_seek_input'

            assert 'state' not in locals()
            state = STATE_SEEK_HEADING
            assert 'fl' not in locals()
            for fl in fls:
#           BEGIN for each line in the init file
#           {
                if STATE_SEEK_HEADING == state:

                    # ln: [current level] long name 
                    if (
                        f'\\{ln}{{' == fl[:len(f'\\{ln}{{')]
                        and
                        '}\n' == fl[-2:]
                    ):
                        state = STATE_SEEK_LABEL

                elif STATE_SEEK_LABEL == state:

                    if (
                        '\\label{' == fl[:len('\\label{')]
                        and
                        '}\n' == fl[-2:]
                    ):
                        state = STATE_SEEK_INPUT

                elif STATE_SEEK_INPUT == state:

                    if (
                        '\\input{' == fl[           :len('\\input{')]
                        and
                        '}\n'      == fl[-len('}\n'):               ]
                    ):
                        # ip: input path
                        assert 'ip' not in locals(), ip
                        ip = fl[len('\\input{'):-len('}\n')]

                        ips.append(ip)
                        del ip
                else:
                    raise RuntimeError(f'unexpected state "{state}"')
                del fl
#           }
#           END for each line in the init file
            del fls
            del state
            #
            #
            # ips: input paths
            assert isinstance(ips, list), type(ips)
            assert 0 < len(ips)
            #
            assert 'ip' not in locals()
            for ip in ips:
#           BEGIN for each input path in the heading init file
#           {
                #
                # hipp: heading input path, partial
                assert len(hipp) < len(ip)
                assert hipp == ip[:len(hipp)]
                #
                # hippc: (heading input path, partial) components
                assert 'hippc' not in locals()
                hippc = hipp.split('/')
                #
                # ipc: input path components
                assert 'ipc' not in locals()
                ipc = ip.split('/')
                del ip

                assert len(hippc) < len(ipc)
                assert hippc == ipc[:len(hippc)]

                assert len(hippc)+1 <= len(ipc) and len(ipc) <= len(hippc)+2

                if len(hippc)+1 == len(ipc):

                    assert ipc[-1] != INIT     , (ipc[-1], INIT)
                    assert ipc[-2] == hippc[-1], (ipc[-2], hippc[-1])

                    assert '.tex' != ipc[-1][-4:], ipc[-1]

                    # cfp: child file path
                    assert 'cfp' not in locals()
                    cfp = os.path.join(dp, f'{ipc[-1]}.tex')
                    assert os.path.isdir(dp), dp
                    assert os.path.isfile(cfp), cfp


                    # chipp: child heading input path, partial
                    assert 'chipp' not in locals()
                    chipp = '/'.join(ipc)
                    del ipc

                    # chd: child heading dict
                    assert 'chd' not in locals()
                    chd = \
                        {
                            f'{nsn}_is_leaf'  : True,
                            f'{nsn}_file_path': cfp,
                        }
                    del cfp

                else:
                    assert len(hippc)+2 == len(ipc)

                    assert ipc[-1] == INIT
                    assert 0 < len(ipc[-2])
                    assert ipc[-3] == hippc[-1]

                    # cdp: child dir path
                    assert 'cdp' not in locals()
                    cdp = os.path.join(dp,ipc[-2])
                    assert os.path.isdir(dp), dp
                    assert os.path.isdir(cdp), cdp

                    # cfp: child file path
                    assert 'cfp' not in locals()
                    cfp = os.path.join(cdp, f'{INIT}.tex')
                    assert os.path.isfile(cfp), cfp

                    # chipp: child heading input path, partial
                    assert 'chipp' not in locals()
                    assert INIT == ipc.pop()
                    chipp = '/'.join(ipc)
                    del ipc

                    # chd: child heading dict
                    assert 'chd' not in locals()
                    chd = \
                        {
                            f'{nsn}_is_leaf'  : False,
                            f'{nsn}_file_path': cfp,
                            f'{nsn}_dir_path' : cdp,
                            f'{nnsn}s'        : [],
                        }
                    del cfp,cdp

                # nhscl: next headings container list
                nhscl.append((chipp,chd))

                # nlhs: next-level headings [list]
                nlhs.append((chipp,chd))

                del chipp,chd

                del hippc
#           }
#           END for each input path in the heading init file
            del ips


            #END read the init file for the current heading
            #    and add each of the input macro paths to the
            #    nhscl (next headings container list)
            #    and the
            #    nlhs (next-level headings [list])



            #BEGIN now that the init file has been read,
            #      confirm that the contents of the heading dir
            #      agree with what was in the init file


            assert 1 <= len(nhscl)
            assert len(nhscl) <= len(os.listdir(dp)) - 1

            assert 1 == os.listdir(dp).count(f'{INIT}.tex')


            # chn_t: child heading name to type
            assert 'chn_t' not in locals()
            chn_t = {}

            # cn: child name
            #     (the "child" may be a file or dir)
            assert 'cn' not in locals(), cn
            for cn in os.listdir(dp):
#           BEGIN for each file/dir name in the heading dir
#           {
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


                # chn: child heading name
                assert 'chn' not in locals()
                assert 't' not in locals()
                chn = None
                t = None
                if os.path.isfile(cp):
                    assert '.tex' == cp[-4:]
 

                    chn = cn[:-4]
                    t = 'isfile'
                else:
                    assert os.path.isdir(cp), cp
                    chn = cn
                    t = 'isdir'
                  
                assert chn not in chn_t
                chn_t[chn] = t
                del chn
                del t,cn,cp
#           }
#           END for each file/dir in the heading dir


            # nhscd: next headings container dict
            assert 'nhscd' not in locals()
            nhscd = {chipp:chd for chipp,chd in nhscl}
            assert len(nhscd) == len(nhscl)
            del nhscl

            # chn_t: child heading name to type
            assert len(nhscd) == len(chn_t), \
                (nhscd, chn_t, len(nhscd), len(chn_t))

            # chn: child heading name
            # t  : type
            assert 'chn' not in locals()
            assert 't'   not in locals()
            for chn,t in chn_t.items():
#           BEGIN for each sub heading in the heading dir
#           {
                # chipp: child heading input path, partial
                assert 'chipp' not in locals()
                chipp = f'{hipp}/{chn}'

                assert chipp in nhscd, chipp
                # chd: child heading dict
                assert 'chd' not in locals()
                chd = nhscd[chipp]
                del chipp

                if chd[f'{nsn}_is_leaf'] is True:
                    assert 'isfile' == t, t
                else:
                    assert chd[f'{nsn}_is_leaf'] is False
                    assert 'isdir' == t, t

                del chd
                del chn,t
#           }
#           END for each sub heading in the heading dir

            del nhscd

            del chn_t

            #END now that the init file has been read,
            #    confirm that the contents of the heading dir
            #    agree with what was in the init file


            # dp: [current heading] dir path
            del dp

            # hipp: heading input path, partial
            # hd  : [current] heading dict
            del hipp, hd
#       }
#       END for each heading at current level

        #  lhs: [current-]level headings
        # nlhs:     next- level headings
        lhs = nlhs
        nlhs = []
        
        del sn,ln,nsn,nln,nnsn,nnln
#   }
#   END for each level

    #END level-order tree traversal


    # ptl: project tree list
    assert isinstance(ptl, list), (ptl, type(ptl))
    assert 1 <= len(ptl), (ptl, len(ptl))
      
    return ptl



def main() -> int:
    pprint.pprint(get_project_tree())
    return 0



if '__main__' == __name__:
    sys.exit(main())





