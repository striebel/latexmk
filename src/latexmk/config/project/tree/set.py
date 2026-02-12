import os

from . import INIT


def toggle_input_macros(input_macros_config: list) -> None:

    imc = input_macros_config
    del input_macros_config

    assert isinstance(imc, list), type(imc)
    assert 3 == len(imc), len(imc)

    # fu: files to update
    fu = {}

    # tlhs: this-level headings [list]
    # hlns: heading level names [list]
    def preorder_traversal_of_imc_to_construct_fu(fu,tlhs,hlns) -> None:
        assert isinstance(fu,dict),type(fu)
        assert isinstance(tlhs,list),type(tlhs)
        assert isinstance(hlns,tuple),type(hlns)

        assert 1 <= len(hlns)
        if 1 == len(hlns):
            assert 0 == len(tlhs), len(tlhs)

        # hipp: heading input path partial
        # hd  : config heading dict
        for hipp,chd in tlhs:
            assert isinstance(hipp,str),type(hipp)
            assert isinstance(chd,dict),type(chd)

            assert 4 == len(chd),len(chd)
            it   = chd['input_toggle']
            ifp  = chd['input_file_path']
            imp  = chd['input_macro_path']
            nlhs = chd[f'{ hlns[1] }s']
            del chd

            assert it in (True,False), it
            assert isinstance(ifp,str),type(ifp)
            assert 0 < len(ifp)
            assert os.path.isfile(ifp),ifp
            assert 0 < os.path.getsize(ifp),ifp
            assert isinstance(imp,str),type(imp)
            assert 0 < len(imp)
            assert isinstance(nlhs,list),type(nlhs)

            if it is False:
                if ifp not in fu:
                    fu[ifp] = []
                assert imp not in fu[ifp]
                fu[ifp].append(imp)

            preorder_traversal_of_imc_to_construct_fu(
                fu   = fu,
                tlhs = nlhs,
                hlns = hlns[1:],
            )
             
    
    # ct: chapter type
    for ct,cts in imc:
        # cn: chapter name [short]
        for cn,cns in cts:
            preorder_traversal_of_imc_to_construct_fu(
                fu   = fu,
                tlhs = cns,
                hlns = ('sec','subsec','subsubsec','par','subpar')
            )

    # fu  : files to update
    # ifp : input file path
    # imps: input macro paths [list]
    assert 'ifp'  not in locals()
    assert 'imps' not in locals()
    for ifp,imps in fu.items():
#   BEGIN for each file to update
#   {
        assert isinstance(imps,list),type(imps)
        assert 0 < len(imps)

        assert isinstance(ifp,str),type(ifp)
        assert 0 < len(ifp)
        assert f'{INIT}.tex' == os.path.basename(ifp),ifp
        assert os.path.isfile(ifp),ifp
        assert 0 < os.path.getsize(ifp),ifp
        assert '/build/' in ifp,ifp
        #  ifo:          input file object
        #  ifs:          input file str
        # oifs: original input file str
        with open(ifp,'rt') as ifo:
            oifs = ifs = ifo.read()
        del ifo
        assert isinstance(ifs,str),type(ifs)
        assert 0 < len(ifs)
        assert 'imp' not in locals()
        for imp in imps:
#       BEGIN for each macro to comment out
#       {
            # im : input macro
            # imo: input macro [toggled] off
            im  =  f'\n\\input{{{imp}}}\n'
            imo = f'\n%\\input{{{imp}}}\n'
            del imp
            assert 1 == ifs.count(im)
            ifs = ifs.replace(im,imo)
            assert 0 == ifs.count(im)
            assert 1 == ifs.count(imo)
            del im,imo
#       }
#       END for each macro to comment out
        assert len(oifs) + len(imps) == len(ifs)
        del oifs,imps
        with open(ifp,'wt') as ifo:
            ifo.write(ifs)
        del ifo
        del ifs
        del ifp
#   }
#   END for each file to update


    return None




