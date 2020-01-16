"""Abaco commands
"""
# from .. import SERVICE_VERSION
API_NAME = 'actors'
SERVICE_VERSION = 'v2'

from .models import Actor
from .list import ActorsList
from .show import ActorsShow
from .delete import ActorsDelete
from .pems_list import ActorsPemsList
