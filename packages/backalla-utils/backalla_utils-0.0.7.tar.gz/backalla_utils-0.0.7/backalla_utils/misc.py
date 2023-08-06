import sys
from itertools import chain
import os
from glob import glob
import tarfile
import os


def create_checkpoint_tar(save_path):
    """
    Create a tar archive of all checkpoint files for a particular checkpoint
    :param save_path: Path to the checkpoints
    :return: Path to the created tar file
    """
    checkpoint_suffixes = [".data-00000-of-00001", ".index", ".meta"]

    tar_path = save_path + ".tar"

    with tarfile.open(tar_path, 'w') as tar:
        for suffix in checkpoint_suffixes:
            checkpoint_file = save_path+suffix
            tar.add(checkpoint_file, arcname=os.path.basename(checkpoint_file))

    return tar_path

def untar(tar_path,extract_path):
    """
    Extract tar file to a destination
    :param tar_path: Path to the tar file
    :param extract_path: Path to extract the tar
    :return: Nothing
    """
    with tarfile.open(tar_path) as tar_file:
        tar_file.extractall(path=extract_path)



def recursive_ls(path, get_generator=False, filter="*.*"):
    """Recursively list the files in a given target path.
    
    Arguments:
        path {str} -- Path of root folder to recursively list files
    
    Keyword Arguments:
        get_generator {bool} -- Flag to decide whether to return a generator or a list (default: {False})
        filter {str} -- Regex to filter filenames  (default: {"*.*"})
    
    Returns:
        [list/generator] -- Depending on the get_generator flag return the list
        of files or a generator
    """

    if get_generator:
        result = (chain.from_iterable(glob(os.path.join(x[0], filter)) for x in os.walk(path)))
    else:
        result = [y for x in os.walk(path) for y in glob(os.path.join(x[0], filter))]
    
    return result



def rprint(*args):
    """Print a string in one line by overwriting the current line.
    Used to print training and testing progress. Can accept multiple
    arguments which will be printed with spaces in between.
    """

    
    sys.stdout.write("\r{}".format(" ".join([str(arg) for arg in args])))
    sys.stdout.flush()