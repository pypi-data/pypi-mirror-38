from os.path import join, isdir
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
    logger.info(f'Saving indexer [{class_name}] to {output_dir}')
    _save_name(class_name, _gen_name_path(output_dir))

    # save indexer
    indexer.save(output_dir)  # save indexer
    del indexer


def load_indexer(
        output_dir: str,
        logger: logging.Logger = LOGGER,
    ) -> Indexer:

    _validate_dir(output_dir)
    logger.info(f'Loading indexer from {output_dir}')

    # load indexer
    indexer_name = _load_name(_gen_name_path(output_dir))
    indexer_module = _get_indexer_module(indexer_name)
    indexer = indexer_module.load(output_dir)

    return indexer


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


def _gen_name_path(directory: str) -> str:
    return join(directory, 'name')


def _get_indexer_module(indexer_name: str) -> Indexer:
    return INDEXERS[indexer_name]
