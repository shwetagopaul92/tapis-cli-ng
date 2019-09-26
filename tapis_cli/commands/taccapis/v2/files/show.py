import os
from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier, AgaveURI
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import File
from .formatters import FilesFormatOne
from .mixins import FileOptions

__all__ = ['FilesShow']


class FilesShow(FilesFormatOne, AgaveURI, FileOptions):
    """Show a single Files record
    """
    VERBOSITY = Verbosity.RECORD
    EXTRA_VERBOSITY = Verbosity.RECORD

    # TODO - add formatting and sorting options
    def get_parser(self, prog_name):
        parser = FilesFormatOne.get_parser(self, prog_name)
        parser = AgaveURI.extend_parser(self, parser)
        parser = FileOptions.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = FilesFormatOne.before_take_action(self, parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        headers = SearchableCommand.headers(self, File, parsed_args)
        (storage_system, file_path) = AgaveURI.parse_url(parsed_args.agave_uri)
        rec = self.tapis_client.files.list(systemId=storage_system,
                                           filePath=file_path,
                                           limit=1,
                                           offset=0)
        if isinstance(rec, list):
            rec = rec[0]
        else:
            raise ValueError('No files listing was returned')

        # Fixes issue where the name of the listed file/directory is not
        # returned by the files service
        if rec['name'] == '.':
            rec['name'] = os.path.basename(rec['path'])

        data = []
        for key in headers:
            try:
                val = rec[key]
            except KeyError:
                val = None
            data.append(self.render_value(val))

        return (tuple(headers), tuple(data))
