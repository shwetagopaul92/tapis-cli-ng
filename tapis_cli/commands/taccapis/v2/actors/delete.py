
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne
from .mixins import ActorIdentifier
from .models import Actor, HTTP_METHODS

__all__ = ['ActorsDelete']


class ActorsDelete(ActorsFormatOne, ActorIdentifier):
    """Deletes the Actor corresponding to the given actor ID
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsDelete, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)

        headers = ['deleted', 'messages']
        deleted = []
        messages = []
        try:
            self.requests_client.delete(actor_id)
            deleted.append(self.requests_client.build_url(actor_id))
        except Exception as err:
            messages.append(str(err))
        data = [deleted, messages]
        return (tuple(headers), tuple(data))
