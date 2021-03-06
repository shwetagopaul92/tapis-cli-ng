from tapis_cli.clients.http import HTTPFormatMany
from tapis_cli.settings import TAPIS_CLI_PAGE_SIZE
from .bearer import TaccApisBearer
from ...mixins import (AppVerboseLevel, JsonVerbose, UploadJsonFile,
                       ServiceIdentifier)

__all__ = ['TaccApisFormatManyUnlimited', 'TaccApisFormatMany']


class TaccApisFormatManyUnlimited(JsonVerbose, HTTPFormatMany, TaccApisBearer):
    def get_parser(self, prog_name):
        parser = HTTPFormatMany.get_parser(self, prog_name)
        parser = HTTPFormatMany.add_common_parser_arguments(self, parser)
        parser = TaccApisBearer.add_common_parser_arguments(self, parser)
        return parser

    def preprocess_args(self, parsed_args):
        self.init_clients(parsed_args)
        parsed_args = super(TaccApisFormatManyUnlimited,
                            self).preprocess_args(parsed_args)
        self.update_payload(parsed_args)
        return parsed_args


class TaccApisFormatMany(TaccApisFormatManyUnlimited):
    """TACC APIs HTTP+Token Records Listing
    """
    def get_parser(self, prog_name):
        # Because this class is composed of multiple parents with get_parser
        # and add_common_parser_arguments methods, we call them in preferred
        # order because relying Python MRO will fail

        # print('TaccApisFormatMany.get_parser')
        parser = TaccApisFormatManyUnlimited.get_parser(self, prog_name)
        parser.add_argument('-l',
                            '--limit',
                            dest='limit',
                            metavar='<int>',
                            default=TAPIS_CLI_PAGE_SIZE,
                            type=int,
                            help='Limit to L records')
        parser.add_argument('-o',
                            '--offset',
                            default=0,
                            metavar='<int>',
                            dest='offset',
                            type=int,
                            help='Skip first O records')
        return parser

    def update_payload(self, parsed_args):
        self.post_payload['limit'] = parsed_args.limit
        self.post_payload['offset'] = parsed_args.offset
        return self

    def preprocess_args(self, parsed_args):
        parsed_args = super(TaccApisFormatMany,
                            self).preprocess_args(parsed_args)
        self.update_payload(parsed_args)
        return parsed_args
