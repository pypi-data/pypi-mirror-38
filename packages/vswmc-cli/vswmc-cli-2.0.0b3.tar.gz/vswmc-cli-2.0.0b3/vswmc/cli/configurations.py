from __future__ import print_function

from vswmc.cli import utils


def list_(args):
    client = utils.create_client(args)

    rows = [['ID', 'NAME', 'MODELS']]
    for configuration in client.list_configurations():
        model_ids = [m['id'] for m in configuration['models']]
        rows.append([
            configuration['_id'],
            configuration['name'],
            ', '.join(model_ids),
        ])
    utils.print_table(rows)


def delete(args):
    client = utils.create_client(args)
    for id_ in args.configuration:
        configuration = client.get_configuration(id_)
        runs = client.list_runs(configuration=configuration['_id'])
        if runs:
            print('There are still {} "{}" runs. You must delete them first.'.format(
                len(runs), configuration.name))
        else:
            client.delete_configuration(id_)
            print('Deleted', id_)


def configure_parser(parser):
    subparsers = parser.add_subparsers(title='Commands', metavar='COMMAND')

    subparser = subparsers.add_parser('list', help='List configurations')
    subparser.set_defaults(func=list_)

    subparser = subparsers.add_parser('delete', help='Delete configuration')
    subparser.set_defaults(func=delete)
    subparser.add_argument('configuration', metavar='CONFIGURATION', nargs='+', help='Configuration to delete')
