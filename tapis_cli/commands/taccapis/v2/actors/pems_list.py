from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier

from tapis_cli.commands.taccapis.model import Permission
from tapis_cli.clients.services.mixins import ActorVerboseLevel

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatMany

__all__ = ['ActorsPemsList']


class ActorsPemsList(ActorsFormatMany, ActorIdentifier):
    """List Permissions for specific Actor
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsPemsList, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        self.update_payload(parsed_args)

        headers = self.render_headers(Permission, parsed_args)
        results = self.tapis_client.actors.getPermissions(actorId=actor_id)

        records = []
        for rec in results:
            record = []
            # Table display
            #if self.actor_verbose_level > self.VERBOSITY:
            record.append(rec.get('username'))
            record.extend(Permission.pem_to_row(rec.get('permission', {})))
            #else:
                #for key in headers:
                #    val = self.render_value(rec.get(key, None))
                #    record.append(val)
            # Deal with an API-side bug where >1 identical pems are
            # returned for the owning user when no additional pems have been
            # granted on the app
            if record not in records:
                records.append(record)

        return (tuple(headers), tuple(records))
