# coding=utf-8
"""
Interface to Github release objects
"""
import logging
import typing
from pathlib import Path

import requests
import requests.exceptions
from humanize import naturalsize

from ..custom_random import random_string
from ..downloader import Downloader, download

LOGGER = logging.getLogger('elib')


class _Val:

    def __init__(self):
        self.name = None
        self.owner = None

    def __get__(self, instance, _):
        if not instance:
            return self

        if self.name == 'assets':
            return [Asset(asset, instance) for asset in getattr(instance, '_json')['assets']]

        return getattr(instance, '_json')[self.name]

    def __set_name__(self, owner, name):
        self.owner = owner
        self.name = name


class Asset:
    """
    Represents a Github asset
    """
    name: str = _Val()  # type: ignore
    browser_download_url: str = _Val()  # type: ignore
    size: int = _Val()  # type: ignore
    state: str = _Val()  # type: ignore

    def __init__(self, json: dict, release: 'Release') -> None:
        self._json = json
        self._release = release

    def __repr__(self):
        return f'Asset({self.name}), {naturalsize(self.size)}, {self.state}, {self.browser_download_url}'

    def _get_hexdigest(self) -> typing.Optional[str]:
        for asset in self._release.assets:
            if asset.name == f'{self.name}.md5':
                hexdigest = Downloader(asset.browser_download_url, random_string())
                hexdigest.download_to_memory()
                data = hexdigest.file_binary_data
                if data:
                    return data.decode('utf16').strip()

        return None

    def download(self, outfile: typing.Union[str, Path]) -> bool:
        """
        Downloads this asset

        :param outfile: target file
        :return: success of the operation
        """
        hexdigest = self._get_hexdigest()
        return download(self.browser_download_url, outfile, hexdigest=hexdigest)


class Release:
    """
    Represents a Github release
    """
    tag_name: str = _Val()  # type: ignore
    body: str = _Val()  # type: ignore
    assets: typing.List[Asset] = _Val()  # type: ignore

    def __init__(self, json: dict) -> None:
        self._json = json

    def __repr__(self) -> str:
        return f'LatestVersion({self.tag_name}), {len(self.assets)} assets'


def get_latest_release(repo: str) -> typing.Optional[Release]:
    """
    Obtains latest release from Github

    :param repo: repository in the form of "owner/repo"
    :return: Release object or None"
    """
    LOGGER.debug('obtaining latest version for "%s"', repo)
    try:
        req = requests.get(rf'https://api.github.com/repos/{repo}/releases/latest', timeout=5)
    except requests.exceptions.Timeout:
        LOGGER.exception('request timed out')
        return None

    if not req.ok:
        LOGGER.error('request failed: %s', req.reason)
        return None

    return Release(req.json())
