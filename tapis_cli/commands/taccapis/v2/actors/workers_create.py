from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatOne

__all__ = ['ActorsPemsGrant']


class ActorsWorkersCreate(ActorsFormatOne, ActorIdentifier):
    """Create Workers for a specific Actor
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsWorkersCreate, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        parser.add_argument('num',
                            metavar='<num>',
                            type=int,
                            help='Number of Workers to create',
                            default=1)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        num = parsed_args.num
        body = {
            'num': num
        }
        create_result = self.tapis_client.actors.addWorker(
            actorId=actor_id, body=body)
        rec = self.tapis_client.actors.listWorkers(actorId=actor_id)
        headers = ["workers"]
        # worker names are in a list
        data = []
        for key in rec:
            try:
                val = rec['result']
            except KeyError:
                val = None
            data.append(self.render_value(val))
        return(tuple(headers), tuple(data))
