# flake8: noqa
from .api import APIClient
from .client import DockerClient, from_env
from .version import version, version_info

__version__ = version
__title__ = 'docker'
