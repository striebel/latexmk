# Confirm that the project trees returned by v0 and v1
# are logically equivalent

import sys
import os

from .v0 import get_project_tree as get_pt_v0
from .v1 import get_project_tree as get_pt_v1


def v1test() -> None:
    
    # ptd: project tree dict
    # ptl: project tree list
    ptd = get_pt_v0()
    ptl = get_pt_v1()
    
    assert isinstance(ptd, dict), type(ptd)
    assert isinstance(ptl, list), type(ptl)
    
    assert len(ptd) == len(ptl)
    
    #BEGIN level-order tree traversal
    
    # tld: this level dict 
    # tll: this level list
    # nld: next level dict
    # nll: next level list
    tld = ptd
    tll = ptl
    nld = {}
    nll = []
    del ptd,ptl
    
    # lns: level names
    lns = \
        (
            'ch'       ,
            'sec'      ,
            'subsec'   ,
            'subsubsec',
            'par'      ,
            'subpar'   ,
            ''         ,
        )
    
    max_ln_width = max(len(ln) for ln in lns)
    
    #  ln: [this] level name
    # nln:  next  level name
    assert  'ln' not in locals()
    assert 'nln' not in locals()
    for ln,nln in zip(lns,lns[1:]):
#   BEGIN for each level
#   {
        assert {} == nld
        assert [] == nll
        
        assert isinstance(tld, dict), (ln, type(tld))
        assert isinstance(tll, list), (ln, type(tll))
        
        assert len(tld) == len(tll)
        
        # tls: this level set
        assert 'tls' not in locals()
        tls = set(hipp for hipp,hd in tll)
        assert len(tls) == len(tll)
        del tls
        
        _ln = ln.ljust(max_ln_width)
        print(f'level={_ln}  width={len(tll)}')
        del _ln
        
        # hipp: heading input path, partial [str]
        # hdv1: heading dict version 1
        assert 'hipp' not in locals()
        assert 'hdv1' not in locals()
        for hipp,hdv1 in tll:
#       BEGIN for each heading in this level list
#       {
            assert hipp in tld, (ln, hipp)
            # hdv0: heading dict version 0
            assert 'hdv0' not in locals()
            hdv0 = tld[hipp]

            assert 'is_leaf'   not in locals()
            assert 'file_path' not in locals()
            is_leaf   = hdv1[f'{ln}_is_leaf'  ]
            file_path = hdv1[f'{ln}_file_path']

            assert is_leaf   == hdv0[f'{ln}_is_leaf'  ]
            assert file_path == hdv0[f'{ln}_file_path']
            
            assert os.path.isfile(file_path), file_path
            del file_path

            if is_leaf is True:
                del is_leaf

                assert 2 == len(hdv0)
                assert 2 == len(hdv1)

                del hdv0
                del hipp,hdv1
                continue

            assert is_leaf is False
            del is_leaf

            assert 4 == len(hdv0)
            assert 4 == len(hdv1)

            assert 'dir_path' not in locals()
            dir_path = hdv1[f'{ln}_dir_path']
            assert dir_path == hdv0[f'{ln}_dir_path']
            assert os.path.isdir(dir_path), dir_path
            del dir_path

            # chsv1: child headers version 1
            # chsv0: child headers version 0
            assert 'chsv1' not in locals()
            chsv1 = hdv1[f'{nln}s']
            chsv0 = hdv0[f'{nln}s']
            del hdv1,hdv0

            assert isinstance(chsv1, list), type(chsv1)
            assert isinstance(chsv0, dict), type(chsv0)

            assert len(chsv1) == len(chsv0)

            # _chsv1: child headers version 1 [set]
            assert '_chsv1' not in locals()
            _chsv1 = set(chipp for chipp,_ in chsv1)
            assert len(chsv1) == len(_chsv1)
            del _chsv1

            # chipp: child heading input path, partial
            # chd  : child heading dict
            assert 'chipp' not in locals()
            assert 'chd'   not in locals()
            for chipp,chd in chsv1:

                assert hipp == chipp[:len(hipp)]

                # chipb: child heading input path basename
                assert 'chipb' not in locals()
                chipb = os.path.basename(chipp)
                assert f'{hipp}/{chipb}' == chipp

                # nll: next-level list
                nll.append((chipp,chd))

                # nld: next-level dict
                assert chipb in chsv0, ([k for k in chsv0], hipp, chipb, chipp)
                assert chipp not in nld
                nld[chipp] = chsv0[chipb]

                del chipb
                del chipp,chd
            
            del chsv1,chsv0 
            del hipp
#       }
#       END for each heading in this level list

        tll = nll
        tld = nld
        nll = []
        nld = {}
        
        del ln,nln
#   }
#   END for each level

    assert {} == tld
    assert [] == tll
    assert {} == nld
    assert [] == nll

    #END level-order tree traversal
 
    return None


def main() -> int:
    assert v1test() is None
    return 0


if '__main__' == __name__:
    sys.exit(main())




