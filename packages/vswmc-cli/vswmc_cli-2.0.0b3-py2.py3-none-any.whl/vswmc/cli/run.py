from __future__ import print_function

import os

from vswmc.cli import utils


def add_parameter(run_parameters, param):
    if '=' not in param:
        raise Exception(
            'Invalid parameter \'{}\'. Use format \'key=value\''.format(param))

    k, value = param.split('=')

    if '.' not in k:
        raise Exception('Parameter \'{}\' does not include a model prefix'.format(k))

    model, key = k.split('.')

    if model in run_parameters:
        model_parameters = run_parameters[model]
    else:
        model_parameters = {}
        run_parameters[model] = model_parameters

    model_parameters[key] = value


def do_run(args):
    parameters = {}

    if args.param_file:
        with open(args.param_file, 'rb') as f:
            for param in f.readlines():
                param = param.strip()
                if param and not param.startswith('#'):
                    add_parameter(parameters, param)

    for param_arg in (args.param or []):
        for param in param_arg:
            add_parameter(parameters, param)

    client = utils.create_client(args)

    for model in parameters:
        model_parameters = parameters[model]
        if model == 'euhforia_corona':
            if 'magnetogram' in model_parameters:
                path = os.path.expanduser(model_parameters['magnetogram'])
                with open(path, 'rb') as f:
                    name = os.path.basename(path)
                    upload_reference = client.upload_magnetogram(f, name)
                    model_parameters['magnetogram'] = upload_reference

    run = client.start_run(args.configuration, parameters=parameters)

    def on_data(msg, sess):  # source, generated, msg
        if not msg['debug']:
            print('{} [{}] {}'.format(msg['generated'], msg['source'], msg['msg']))
            if 'Stopping run' in msg['msg']:
                sess.disconnect()

    if args.follow:
        content = client.download_logs(run['_id']).strip()
        if content:
            print(content)
        subscription = client.follow_logs(args.user, run['_id'], on_data=on_data)
        subscription.result()
    else:
        print(run['_id'])


def configure_parser(parser):
    parser.set_defaults(func=do_run)
    parser.add_argument('--param-file', help='Read parameters from a file')
    parser.add_argument('--param', metavar='PARAM=VALUE', action='append', nargs='+', help='Set parameters')
    parser.add_argument('-f', '--follow', action='store_true', help='Follow log output')
    parser.add_argument('configuration', metavar='CONFIGURATION', help='The configuration to run')
