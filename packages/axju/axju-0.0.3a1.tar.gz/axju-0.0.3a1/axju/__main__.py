from axju.core.tools import setup_parser, setup_logger
from axju.worker.django import DjangoWorker
from axju.worker.git import GitWorker

def main():
    parser = setup_parser()
    subparsers = parser.add_subparsers(help='commands', dest='action')

    parser_git = subparsers.add_parser('git', help='coming soon')

    parser_django = subparsers.add_parser('django', help='Django deploying :)')
    parser_django.add_argument('--folder', type=str, default='.', help='The django project folder.')
    parser_django.add_argument('--setting', type=str, default='', help='Change the default the settings.')

    args = parser.parse_args()
    setup_logger(args.verbose, args.log)

    if args.action == 'django':
        worker = DjangoWorker(folder=args.folder, setting=args.setting)
    elif args.action == 'git':
        worker = GitWorker()
    else:
        return parser.print_help()

    if args.show:
        return worker.show(args.show)

    for step in args.steps:
        worker.run(step)
        

if __name__ == '__main__':
    main()
