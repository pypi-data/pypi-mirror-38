from vgscli.api import create_api
from vgscli.config import load_config
from vgscli.routes import dump_all_routes, sync_all_routes, create_all_routes
from vgscli.utils import is_file_accessible, eprint

import sys

from vgscli.auth import logout, login


def main(args):
    if args.subparser_name == 'logout':
        logout()
        sys.exit(0)

    config_file = load_config()
    token = login(config_file)
    if args.subparser_name == 'authenticate':
        # don't need to do anything, just process the auth
        pass

    if args.subparser_name == 'route':
        if not args.tenant:
            eprint("Please specify --tenant option.")

        vgs_api = create_api(args.tenant, args.environment, token, args.tld)
        if args.dump_all:
            dump = dump_all_routes(vgs_api)
            print(dump)
        if args.sync_all:
            dump_data = sys.stdin.read()
            updated_dump = sync_all_routes(vgs_api, dump_data,
                                           lambda route_id: eprint('Route {} processed'.format(route_id)))
            print(updated_dump)
            eprint("Routes updated successfully for tenant " + args.tenant)
        if args.create_all:
            dump_data = sys.stdin.read()
            updated_dump = create_all_routes(vgs_api, dump_data,
                                             lambda route_id: eprint('Route {} processed'.format(route_id)))
            print(updated_dump)
            eprint("Routes created successfully for tenant " + args.tenant)
