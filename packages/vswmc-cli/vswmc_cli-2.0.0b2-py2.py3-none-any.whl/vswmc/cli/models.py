from __future__ import print_function

from vswmc.cli import utils


def list_(args):
    client = utils.create_client(args)

    rows = [['ID', 'DESCRIPTION']]
    for model in client.list_models():
        rows.append([
            model['id'],
            model['description'] or '',
        ])
    utils.print_table(rows)


def describe(args):
    client = utils.create_client(args)
    model = client.get_model(args.model)
    print('Id:', model['id'])
    print('Name:', model['name'])
    print('Description:', model['description'] or '')

    if model['properties']:
        print('Parameters:')
        for parameter in model['properties']:
            req = 'required' if parameter['required'] else 'optional'
            print(' - {} ({})'.format(parameter['key'], req))
    else:
        print('Parameters: None')


def configure_parser(parser):
    subparsers = parser.add_subparsers(title='Commands', metavar='COMMAND')

    subparser = subparsers.add_parser('list', help='List models')
    subparser.set_defaults(func=list_)

    subparser = subparsers.add_parser('describe', help='Describe a model')
    subparser.add_argument('model', metavar='MODEL', help='ID of the model to describe')
    subparser.set_defaults(func=describe)
