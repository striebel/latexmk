import os


def copytree_as_symlinks(src, dst) -> None:
    assert os.path.isdir(src), src
    assert not os.path.isdir(dst), dst

    os.mkdir(dst, mode=0o700)

    new_suffixes = [name for name in os.listdir(src)]
    while 0 < len(new_suffixes):

        cur_suffixes = new_suffixes
        new_suffixes = []

        while 0 < len(cur_suffixes):
             
            suffix = cur_suffixes.pop()

            src_suffix_path = os.path.join(src, suffix)
            dst_suffix_path = os.path.join(dst, suffix)

            assert not os.path.isdir (dst_suffix_path), dst_suffix_path
            assert not os.path.isfile(dst_suffix_path), dst_suffix_path
            
            if os.path.isdir(src_suffix_path):
                assert not os.path.isdir(dst_suffix_path), dst_suffix_path
                os.mkdir(dst_suffix_path, mode=0o700)

                for new_suffix in os.listdir(src_suffix_path):
                    ns = os.path.join(suffix, new_suffix)
                    new_suffixes.append(ns)

            else:
                assert os.path.isfile(src_suffix_path), src_suffix_path

                assert not os.path.isfile(dst_suffix_path), dst_suffix_path

                os.symlink(src_suffix_path, dst_suffix_path)
                
    return None




