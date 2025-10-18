import os



def toggle_input_macros(input_macros_config: dict) -> None:

    imc = input_macros_config; del input_macros_config


    # ct : chapter type
    # ctd: chapter type dict
    for ct, ctd in imc.items():

        # cn: chapter name
        # cd: chapter dict
        for cn, cd in ctd.items():

            cfp = cd.pop('ch_file_path')
            assert os.path.isfile(cfp), cfp
            with open(cfp, 'rt') as cf:
                # cfs : chapter file str
                cfs = cf.read()
            del cf

            assert 1 <= len(cd), len(cfp, len(cd))
            assert len(cd) == cfs.count('\\input{'), \
                (cfp, len(cd), cfs.count('\\input{'))

            # sns: section name suffix
            # sd : section dict
            for sns, sd in cd.items():

                # ip: input (do not comment out the input macro)
                ip = sd.pop('input')
                assert ip in (True, False), ip

                sfp = sd.pop('sec_file_path')
                assert os.path.isfile(sfp), sfp

                sip = sd.pop('sec_input_path')

                assert sip in cfs, sip

                # sim: section input macro
                sim = f'\\input{"{"}{sip}{"}"}\n'

                assert sim in cfs, sim

                if ip is True:
                    pass
                else:
                    assert ip is False, ip
                    cfs = cfs.replace(sim, f'%{sim}')

                
                if 'subsecs' not in sd:
                    continue
                
                
                with open(sfp, 'rt') as sf:
                    # sfs: section file str
                    sfs = sf.read()
                del sf

                subsecs = sd.pop('subsecs')
                assert 0 == len(sd), len(sd)
                del sd
                
                assert 1 <= len(subsecs), len(subsecs)
                assert len(subsecs) == sfs.count('\\input{')

                # ssns: subsection name suffix
                # ssd : subsection dict
                for ssns, ssd in subsecs.items():

                    # ipss: input subsection
                    ipss = ssd.pop('input')
                    assert ipss in (True, False), ipss

                    # subsection input path
                    ssip = ssd.pop('subsec_input_path')

                    assert ssip in sfs, ssip

                    # ssim: subsection input macro
                    ssim = f'\\input{"{"}{ssip}{"}"}\n'

                    assert ssim in sfs, ssim

                    if ipss is True:
                        pass
                    else:
                        assert ipss is False
                        sfs = sfs.replace(ssim, f'%{ssim}')


                with open(sfp, 'wt') as sf:
                    sf.write(sfs)
                del sfs, sf, sfp

            with open(cfp, 'wt') as cf:
                cf.write(cfs)
            del cfs, cf, cfp

    return None




