from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatMany
from .mixins import ActorIdentifier
from .models import Actor

__all__ = ['ActorsWorkersList']


class ActorsWorkersList(ActorsFormatMany, ActorIdentifier):
    """List the Workers for a specific Actor 
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD_VERBOSE

    def get_parser(self, prog_name):
        parser = super(ActorsWorkersList, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        #self.requests_client.setup(API_NAME, SERVICE_VERSION)

        headers = ["workers"]
        rec = self.tapis_client.actors.listWorkers(actorId=actor_id)
        # worker names are in a list
        data = []
        for key in rec:
            try:
                val = rec['result']
            except KeyError:
                val = None
            data.append(self.render_value(val))
        return(tuple(headers), tuple(data))
