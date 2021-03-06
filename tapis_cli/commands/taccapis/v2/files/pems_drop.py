from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import AgaveURI
from tapis_cli.commands.taccapis.model import Permission

from . import API_NAME, SERVICE_VERSION
from .formatters import FilesFormatMany
from .helpers.pems_list import pems_list

__all__ = ['FilesPemsDrop']


class FilesPemsDrop(FilesFormatMany, AgaveURI):
    """Drop all granted permissions from a Files path
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(FilesPemsDrop, self).get_parser(prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)

        (storage_system, file_path) = self.parse_url(parsed_args.agave_uri)
        headers = self.render_headers(Permission, parsed_args)
        drop_result = self.tapis_client.files.deletePermissions(
            systemId=storage_system, filePath=file_path)
        # List now that the drop is complete
        results = pems_list(file_path,
                            system_id=storage_system,
                            agave=self.tapis_client)

        records = []
        for rec in results:
            record = []
            # Table display
            if self.app_verbose_level > self.VERBOSITY:
                record.append(rec.get('username'))
                record.extend(Permission.pem_to_row(rec.get('permission', {})))
            else:
                for key in headers:
                    val = self.render_value(rec.get(key, None))
                    record.append(val)
            # Deal with an API-side bug where >1 identical pems are
            # returned for the owning user when no additional pems have been
            # granted on the app
            if record not in records:
                records.append(record)

        return (tuple(headers), tuple(records))
