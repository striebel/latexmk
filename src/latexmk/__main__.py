import sys
import os
import argparse
import shutil
import types
import stat
import copy
import datetime


SRC = \
    [
        'iuphd.cls',
        'abstract.tex',
        'documentation.tex',
        'formatting.tex',
        {
            'introduction': (
                'introduction.tex',
                'introductiondomainadaptation.tex',
                'introductiontransferlearning.tex'
            )
        },
        {
            'domainclassification': (
                'domainclassification.tex',
                'domainclassificationintroduction.tex',
                'domainclassificationrelatedwork.tex',
                'domainclassificationmethods.tex',
                'domainclassificationevaluation.tex',
                'domainclassificationresults.tex',
                'domainclassificationdiscussion.tex',
                'domainclassificationprompt.tex'
            )
        },
        {
            'domainadaptation': (
                'domainadaptation.tex',
                'domainadaptationintroduction.tex',
                'domainadaptationrelatedwork.tex',
                'domainadaptationmethods.tex',
                'domainadaptationevaluation.tex',
                'domainadaptationresults.tex',
                'domainadaptationdiscussion.tex'
            )
        },
        {
            'domainembedding': (
                'domainembedding.tex',
                'domainembeddingintroduction.tex',
                'domainembeddingrelatedwork.tex',
                'domainembeddingmethods.tex',
                'domainembeddingevaluation.tex',
                'domainembeddingresults.tex',
                'domainembeddingdiscussion.tex'
            )
        },
        'troubleshooting.tex',
        'main.bib',
        'main.tex'
    ]



def get_pdflatex_file_path() -> str:

    pdflatex_file_path = \
        os.path.join(
            '/',
            'usr',
            'bin',
            'pdflatex'
        )

    return pdflatex_file_path



def get_bibtex_file_path() -> str:

    bibtex_file_path = \
        os.path.join(
            '/',
            'usr',
            'bin',
            'bibtex'
        )

    return bibtex_file_path



def get_pythontex_file_path() -> str:

    pythontex_file_path = \
        os.path.join(
            '/',
            'usr',
            'share',
            'texlive',
            'texmf-dist',
            'scripts',
            'pythontex',
            'pythontex3.py'
        )

    return pythontex_file_path



def get_project_dir_path() -> str:

    project_dir_path = \
        os.path.join(
            '/',
            'home',
            'jacob',
            'github',
            'striebel',
            'dissertation_main_writeup'
        )

    return project_dir_path



def get_build_dir_path() -> str:

    project_dir_path = get_project_dir_path()

    assert os.path.isdir(project_dir_path), project_dir_path

    build_dir_path = os.path.join(project_dir_path, 'build')

    return build_dir_path



def get_build_cache_dir_path() -> str:

    build_dir_path = get_build_dir_path()

    assert os.path.isdir(build_dir_path), build_dir_path

    build_cache_dir_path = \
        os.path.join(
            build_dir_path,
            'cache'
        )

    return build_cache_dir_path



def get_src_dir_path() -> str:

    project_dir_path = get_project_dir_path()

    assert os.path.isdir(project_dir_path), project_dir_path

    src_dir_path = os.path.join(project_dir_path, 'src')

    return src_dir_path



def get_cache_dir_path() -> str:

    project_dir_path = get_project_dir_path()

    assert os.path.isdir(project_dir_path), project_dir_path

    cache_dir_path = \
        os.path.join(
            project_dir_path,
            'cache'
        )

    return cache_dir_path



def get_cache_domainembedding_dir_path() -> str:

    cache_dir_path = get_cache_dir_path()

    assert os.path.isdir(cache_dir_path), cache_dir_path

    cache_de_dir_path = \
        os.path.join(
            cache_dir_path,
            'domainembedding'
        )

    return cache_de_dir_path



def get_cache_domainembedding_charts_dir_path() -> str:

    cache_de_dir_path = get_cache_domainembedding_dir_path()

    assert os.path.isdir(cache_de_dir_path), cache_de_dir_path

    cache_de_c_dir_path = \
        os.path.join(
            cache_de_dir_path,
            'charts'
        )

    return cache_de_c_dir_path



def execute(argv : tuple) -> int:

    assert isinstance(argv, tuple), (type(argv), argv)

    assert 2 <= len(argv), (len(argv), argv)

    for i, arg in enumerate(argv):
        assert isinstance(argv[i], str), (i, type(argv[i]), argv[i])

    assert os.path.isfile(argv[0]), argv[0]


    # Confirm that the file is executable

    assert bool(0o100 & os.stat(argv[0]).st_mode)


    build_dir_path = get_build_dir_path()

    assert os.path.isdir(build_dir_path), build_dir_path


    pid = os.fork()

    assert isinstance(pid, int)

    if 0 == pid: # child branch

        assert os.getcwd() != build_dir_path
        assert os.getcwd() == os.environ['PWD']

        os.chdir(build_dir_path)

        assert os.getcwd() == build_dir_path
        assert os.getcwd() != os.environ['PWD']

        os.environ['PWD'] = os.getcwd()

        os.execve(
            path = argv[0],
            argv = argv,
            env  = os.environ
        )

        sys.stderr.write('error: unexpected behavior: execve returned\n')
        sys.exit(3)

    child_pid, raw_wait_status = os.wait()

    assert isinstance(child_pid, int)
    assert pid == child_pid
    assert isinstance(raw_wait_status, int)
    assert 0 <= raw_wait_status

    wait_status = os.waitstatus_to_exitcode(raw_wait_status)

    assert isinstance(wait_status, int)

    return wait_status



def execute_pdflatex() -> int:

    pdflatex_file_path = get_pdflatex_file_path()

    assert os.path.isfile(pdflatex_file_path), pdflatex_file_path

    argv = \
        (
            pdflatex_file_path,
            '-interaction=nonstopmode', # do not stop for user input
                                        # at any point; if an error occurs,
                                        # keep processing.
            '-halt-on-error',           # if an error occurs, exit immediately
            'main'
        )

    wait_status = execute(argv)

    assert isinstance(wait_status, int)

    return wait_status



def execute_bibtex() -> int:

    bibtex_file_path = get_bibtex_file_path()

    assert os.path.isfile(bibtex_file_path), bibtex_file_path

    argv = (bibtex_file_path, 'main')

    wait_status = execute(argv)

    assert isinstance(wait_status, int)

    return wait_status



def execute_pythontex() -> int:

    pythontex_file_path = get_pythontex_file_path()

    assert os.path.isfile(pythontex_file_path), pythontex_file_path

    argv = (pythontex_file_path, 'main')

    wait_status = execute(argv)

    assert isinstance(wait_status, int)

    return wait_status




def clean() -> int:

    build_dir_path = get_build_dir_path()

    if not os.path.isdir(build_dir_path):

        sys.stderr.write('error: project already clean: no build dir present\n')

        return 2

    shutil.rmtree(build_dir_path)

    return 0



def build_project(chapter: str=None) -> int:

    assert chapter in (None, 'domainclassification'), chapter


    build_dir_path = get_build_dir_path()

    if os.path.isdir(build_dir_path):

        sys.stderr.write('error: build dir already exists\n')

        return 2

    os.mkdir(build_dir_path, mode=0o700)


    cache_dir_path = get_cache_dir_path()

    assert os.path.isdir(cache_dir_path), cache_dir_path

    build_cache_dir_path = get_build_cache_dir_path()

    assert not os.path.isdir(build_cache_dir_path)

    os.symlink(cache_dir_path, build_cache_dir_path)

    assert os.path.isdir(build_cache_dir_path)


    src_dir_path = get_src_dir_path()

    assert os.path.isdir(src_dir_path), src_dir_path

    src_dir_file_names = os.listdir(src_dir_path)

    assert isinstance(src_dir_file_names, list)



    for i in range(len(src_dir_file_names)-1, -1, -1):

        fn = src_dir_file_names[i]

        if isinstance(fn, dict):

            pass

        else:
            assert isinstance(fn, str)

            if '.' == fn[0] and '.swp' == fn[-4:]:

                src_dir_file_names.pop(i)

        
    assert len(SRC) == len(src_dir_file_names)



    main_tex_old_to_new = []
    main_aux_old_to_new = []

    _src = copy.deepcopy( SRC )
    if chapter is None:

        pass

    elif 'domainclassification' == chapter:

        assert isinstance(_src, list)
        _src_len = len(_src)
        for i in range(_src_len - 1, -1, -1):
            if isinstance(_src[i], str):
                if _src[i] not in ('iuphd.cls', 'main.tex', 'main.bib'):
                    _src.pop(i)
            else:
                assert isinstance(_src[i], dict)
                assert 1 == len(_src[i])
                if 'domainclassification' != [k for k in _src[i].keys()][0]:
                    _src.pop(i)

        assert 4 == len(_src), (len(_src), _src)

        main_tex_old_to_new.append((
            '\\title{Dissertation Title}',
            '\\title{Domain Classification Dissertation Chapter}'
        ))

        now = \
            datetime.datetime.now(
                tz = datetime.timezone(
                    offset = datetime.timedelta(
                        hours = 0
                    )
                )
            )
        ye = now.year
        mo = now.month
        da = now.day
        ho = now.hour
        mi = now.minute
        se = now.second
        mo = f'0{mo}'[-2:]
        da = f'0{da}'[-2:]
        ho = f'0{ho}'[-2:]
        mi = f'0{mi}'[-2:]
        se = f'0{se}'[-2:]

        main_tex_old_to_new.append((
            '\\date{Month Year}',
            f'\\date{"{"}Draft Version \\texttt{"{"}{ye}-{mo}-{da}T{ho}:{mi}:{se}+00:00{"}"}{"}"}'
        ))

        main_tex_old_to_new.append((
            f'{" "*4}documentation,%\n',
           f'%{" "*4}documentation,%\n'
        ))
        main_aux_old_to_new.append((
            '\\@input{documentation.aux}\n',
            '%\\@input{documentation.aux}\n'
        ))

        main_tex_old_to_new.append((
            f'{" "*4}formatting,%\n',
            f'%{" "*4}formatting,%\n'
        ))
        main_aux_old_to_new.append((
            '\\@input{formatting.aux}\n',
            '%\\@input{formatting.aux}\n'
        ))

        a = 'introduction/introduction'
        main_tex_old_to_new.append((
            f'{" "*4}introduction/introduction,%\n',
            f'%{" "*4}introduction/introduction,%\n'
        ))
        b = f'\\@input{"{"}{a}.aux{"}"}\n'
        main_aux_old_to_new.append((f'{b}', f'%{b}'))
        del b
        del a

        a = 'domainadaptation/domainadaptation'
        b = f'{" "*4}{a},%\n'
        main_tex_old_to_new.append((f'{b}', f'%{b}'))
        c = f'\\@input{"{"}{a}.aux{"}"}\n'
        main_aux_old_to_new.append((f'{c}', f'%{c}'))
        del c
        del b
        del a

        a = 'domainembedding/domainembedding'
        b = f'{" "*4}{a},%\n'
        c = f'\\@input{"{"}{a}.aux{"}"}\n'
        main_tex_old_to_new.append((f'{b}', f'%{b}'))
        main_aux_old_to_new.append((f'{c}', f'%{c}'))
        del c
        del b
        del a

        main_tex_old_to_new.append((
            '\\input{abstract.tex}',
            '%\\input{abstract.tex}'
        ))

    else:
        raise RuntimeError(f'unexpected chapter "{chapter}"')




    # build_file_name to time of last access / modification
    bfn_to_am_to_time = \
        {
            'cache': {
                'accessed': os.stat(build_cache_dir_path).st_atime,
                'modified': os.stat(build_cache_dir_path).st_mtime
            }
        }


    # invocation number to names of created and modified build files 
    #     invono=0 is the original build files
    invono_to_acm_to_bfns = \
        [
            {
                'accessed': [],
                'created' : ['cache'],
                'modified': []
            }
        ]


    for src_file_name in _src:

        if isinstance(src_file_name, str):

            src_file_path = os.path.join(src_dir_path, src_file_name)

            assert os.path.isfile(src_file_path), src_file_path

            dst_dir_path = build_dir_path

            assert os.path.isdir(dst_dir_path), dst_dir_path

            dst_file_path = shutil.copy(src_file_path, f'{dst_dir_path}/')

            assert os.path.isfile(dst_file_path)

             
            if 'main.tex' == os.path.basename(dst_file_path):
                with open(dst_file_path, 'rt') as main_file:
                    main_file_str = main_file.read()
                del main_file
                for old_str, new_str in main_tex_old_to_new:
                    c = main_file_str.count(old_str)
                    assert 1 == c, (c, type(old_str), old_str, new_str)
                    main_file_str = main_file_str.replace(old_str, new_str)
                with open(dst_file_path, 'wt') as main_file:
                    main_file.write(main_file_str)
                del main_file
                    



            assert src_file_name not in bfn_to_am_to_time

            bfn_to_am_to_time[src_file_name] = \
                {
                    'accessed': os.stat(dst_file_path).st_atime,
                    'modified': os.stat(dst_file_path).st_mtime
                }



            assert invono_to_acm_to_bfns[0] == invono_to_acm_to_bfns[-1]

            invono_to_acm_to_bfns[0]['created'].append(src_file_name)

        else:
            assert isinstance(src_file_name, dict)

            for src_subdir_name, src_subfile_names in src_file_name.items():

                for src_subfile_name in src_subfile_names:

                    src_file_path = \
                        os.path.join(
                            src_dir_path,
                            src_subdir_name,
                            src_subfile_name
                        )

                    assert os.path.isfile(src_file_path), src_file_path

                    dst_dir_path = os.path.join(build_dir_path, src_subdir_name)

                    if not os.path.isdir(dst_dir_path):

                        os.mkdir(dst_dir_path, mode=0o700)

                    assert os.path.isdir(dst_dir_path), dst_dir_path

                    dst_file_path = shutil.copy(src_file_path, f'{dst_dir_path}/')

                    assert os.path.isfile(dst_file_path)



                    _src_file_name = f'{src_subdir_name}/{src_subfile_name}'



                    assert _src_file_name not in bfn_to_am_to_time

                    bfn_to_am_to_time[_src_file_name] = \
                        {
                            'accessed': os.stat(dst_file_path).st_atime,
                            'modified': os.stat(dst_file_path).st_mtime
                        }



                    assert invono_to_acm_to_bfns[0] == invono_to_acm_to_bfns[-1]

                    invono_to_acm_to_bfns[0]['created'].append(_src_file_name)








    build_sequence = \
        (
            ('before first invocation of pdflatex', None             ),
            ('first invocation of pdflatex'       , execute_pdflatex ),
            ('invocation of bibtex'               , execute_bibtex   ),
            ('invocation of pythontex'            , execute_pythontex),
            ('second invocation of pdflatex'      , execute_pdflatex ),
            ('third invocation of pdflatex'       , execute_pdflatex ),
        )




    exit_message = None


    assert 1 == len(invono_to_acm_to_bfns)

    # invocation number, (invocation description, function)
    for invono, (invodesc, func) in enumerate(build_sequence):

        assert isinstance(invono, int)
        assert isinstance(invodesc, str)

        if 0 == invono:
            assert func is None
            continue

        assert callable(func)
        assert isinstance(func, types.FunctionType)

        exit_status = func()


        invono_to_acm_to_bfns.append({'accessed': [], 'created': [], 'modified': []})

        assert invono_to_acm_to_bfns[invono] == invono_to_acm_to_bfns[-1]

        # build_file_name
        for bfn in os.listdir(build_dir_path):

            # build_file_path
            bfp = os.path.join(build_dir_path, bfn)

            if bfn not in bfn_to_am_to_time:

                bfn_to_am_to_time[bfn] = \
                    {
                        'accessed': os.stat(bfp).st_atime,
                        'modified': os.stat(bfp).st_mtime
                    }

                invono_to_acm_to_bfns[invono]['created'].append(bfn)

            else:
                assert bfn in bfn_to_am_to_time

                epsilon = 1e-6 # one microsecond

                for am in ('accessed', 'modified'):

                    prev_amtime = bfn_to_am_to_time[bfn][am]

                    curr_amtime = {
                        'accessed': os.stat(bfp).st_atime,
                        'modified': os.stat(bfp).st_mtime
                    }[am]

                    assert isinstance(prev_amtime, float)
                    assert isinstance(curr_amtime, float)

                    if epsilon < abs(prev_amtime - curr_amtime):

                        bfn_to_am_to_time[bfn][am] = curr_amtime

                        invono_to_acm_to_bfns[invono][am].append(bfn)


        if 1 == invono:
            build_dir_path = get_build_dir_path()
            assert os.path.isdir(build_dir_path), build_dir_path
            main_aux_file_path = os.path.join(build_dir_path, 'main.aux')
            assert os.path.isfile(main_aux_file_path), main_aux_file_path
            with open(main_aux_file_path, 'rt') as main_aux_file:
                main_aux_str = main_aux_file.read()
            del main_aux_file
            for old_str, new_str in main_aux_old_to_new:
                c = main_aux_str.count(old_str)
                if 0 == c:
                    continue
                assert 1 == c, (c, old_str)
                main_aux_str = main_aux_str.replace(old_str, new_str)
            with open(main_aux_file_path, 'wt') as main_aux_file:
                main_aux_file.write(main_aux_str)
            del main_aux_str
            del main_aux_file
            del main_aux_file_path
        
                
        if 0 != exit_status:

            exit_message = f'error: the {invodesc} returned exit status {exit_status}\n'

            break



    sys.stderr.write('info: log of file creations and modifications per step, below\n') 


    if len(invono_to_acm_to_bfns) != len(build_sequence):

        assert len(invono_to_acm_to_bfns) < len(build_sequence)

        pass
        

    for invono, (cm_to_bfns, (invodesc, func)) in enumerate(
        zip(invono_to_acm_to_bfns, build_sequence[:len(invono_to_acm_to_bfns)])
    ):

        sys.stderr.write(f'{" "*4}{invodesc}\n')

        for cm, bfns in cm_to_bfns.items():

            sys.stderr.write(f'{" "*8}{cm}\n')

            if 0 == len(bfns):

                sys.stderr.write(f'{" "*12}None\n')
            
            else:

                for bfn in sorted(bfns):

                    sys.stderr.write(f'{" "*12}{bfn}\n')

       
    if exit_message is None:

        assert 0 == exit_status, exit_status

        exit_message = f'info: build complete with no errors detected\n'

        
        assert os.path.isdir(build_dir_path), build_dir_path

        build_main_file_path = os.path.join(build_dir_path, 'main.pdf')

        assert os.path.isfile(build_main_file_path), build_main_file_path


        project_dir_path = get_project_dir_path()

        assert os.path.isdir(project_dir_path), project_dir_path

        evince_main_file_path = os.path.join(project_dir_path, 'main.pdf')


        shutil.copy(build_main_file_path, evince_main_file_path)


    sys.stderr.write(exit_message)
    
    return exit_status




def main() -> int:

    root_parser = argparse.ArgumentParser()

    subparsers = \
        root_parser.add_subparsers(
            required = False
        )

    # dc : domain classification
    # dcp: domain classification parser
    dcp = subparsers.add_parser('dc')
    dcp.set_defaults(
        func    = build_project,
        chapter = 'domainclassification'
    )
    del dcp

    # cp: clean_parser
    cp = subparsers.add_parser('clean')
    cp.set_defaults(func=clean)
    del cp

    root_parser.set_defaults(func=build_project)

    args = vars(root_parser.parse_args())
    func = args.pop('func')
    
    
    return func(**args)



if '__main__' == __name__:
    sys.exit(main())







