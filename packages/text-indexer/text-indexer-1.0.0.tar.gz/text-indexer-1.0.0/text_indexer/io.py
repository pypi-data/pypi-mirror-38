from os.path import join, dirname, basename, isdir, isfile
import tarfile
import shutil
import logging

from .indexers import (
    Indexer,
    CharIndexer,
)


LOGGER = logging.getLogger('__file__')
INDEXERS = {
    indexer_cls.__class__.__name__: indexer_cls for indexer_cls in [
        CharIndexer,
    ]
}


def save_indexer(
        indexer: Indexer,
        output_dir: str,
        logger: logging.Logger = LOGGER,
    ) -> str:

    _validate_dir(output_dir)

    # save indexer class name
    class_name = indexer.__class__.__name__
    _save_name(class_name, _gen_name_path(output_dir))

    # save indexer
    indexer.save(output_dir)  # save indexer
    del indexer

    # compress
    compressed_filepath = _compress_to_tar(output_dir)  # compressed
    shutil.rmtree(output_dir)  # remove output_dir
    logger.info(f'Export to {compressed_filepath}')

    return compressed_filepath


def load_indexer(
        path: str,
        logger: logging.Logger = LOGGER,
    ) -> Indexer:

    _validate_file(path)

    # extract
    output_dir = _extract_from_tar(path)
    logger.info(f'Extract to {output_dir}')

    # load indexer
    indexer_name = _load_name(_gen_name_path(output_dir))
    indexer_module = _get_indexer_module(indexer_name)
    indexer = indexer_module.load(output_dir)

    return indexer


def _validate_file(path: str):
    if not isfile(path):
        raise ValueError(f'[{path}] is not a file path.')


def _validate_dir(directory: str):
    if not isdir(directory):
        raise ValueError(f'[{directory}] is not a directory.')


def _save_name(name: str, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as text_file:
        text_file.write(name)


def _load_name(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as text_file:
        name = text_file.read()
    return name


def _compress_to_tar(output_dir: str) -> str:
    tar_path = _gen_compression_path(output_dir)
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(output_dir, arcname=basename(output_dir))
    return tar_path


def _extract_from_tar(path: str) -> str:
    output_dir = _gen_extraction_dir(path)
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(path=output_dir)
    return output_dir


def _gen_name_path(directory: str) -> str:
    return join(directory, 'name')


def _gen_compression_path(directory: str) -> str:
    parent_dir = dirname(dirname(directory))
    dir_name = basename(dirname(directory))
    path = join(parent_dir, f'{dir_name}-all.tar.gz')
    return path


def _gen_extraction_dir(path: str) -> str:
    parent_dir = dirname(path)
    filename = basename(path)
    output_dirname = '{}/'.format(filename.split('-')[0])
    return join(parent_dir, output_dirname)


def _get_indexer_module(indexer_name: str) -> Indexer:
    return INDEXERS[indexer_name]
