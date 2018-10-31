# You can use this arguments in code by its name casted to python var style
# '--docker-commands' ==> 'docker_commands'
#
# args = parser.parse_args()
# print(args.docker_commands)
ARGUMENTS = {
    '--docker-commands': {
        'short_name': '-d',
        'help': 'Additional docker commands',
    },
    '--config': {
        'short_name': '-c',
        'help': '',
    }
}


def parse_default_args(parser):
    parser.add_argument('-c', '--config', help='Custom dct config')
    conf_args, unknown = parser.parse_known_args()
    return conf_args


def parse_args(parser, config):
    subparsers = parser.add_subparsers()
    for name, desc in config['commands'].items():
        parser_append = subparsers.add_parser(
            name,
            help=desc.get('description', 'No description provided'))
        for arg_name, args in ARGUMENTS.items():
            parser_append.add_argument(
                args['short_name'],
                arg_name,
                help=args['help'],
            )
        parser_append.set_defaults(command=name)
    args = parser.parse_args()
    if not getattr(args, 'command', False):
        parser.print_help()
        exit(1)
    return args
