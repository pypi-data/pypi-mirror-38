import argparse
import sys
from axju.tools import WorkLoader
from axju.worker.django import ArgparseDjangoWorker
from axju.worker.git import GitWorker

def run_one(loader, show):
    name = list(loader.worker.keys())[0]
    if show:
        return loader.worker[name].show()

    return loader.run(name, sys.argv[3:])


def main():
    parser = argparse.ArgumentParser(description='Manage custom worker')

    parser.add_argument('--directory', type=str, help='...')
    parser.add_argument('--file', type=str, help='...')
    parser.add_argument('--cls', type=str, help='...')
    parser.add_argument('--show', action='store_true', help='...')
    parser.add_argument('--setup', action='store_true', help='...')
    parser.add_argument('worker', nargs='?', help='...')

    args, unknown = parser.parse_known_args()
    loader = WorkLoader()

    # No worker name requirt only one worker load
    if args.file:
        loader.load_file(args.file)
        return run_one(loader, args.show)

    if args.cls:
        loader.load_class(args.cls)
        return run_one(loader, args.show)


    # multible worker load
    if args.directory:
        loader.load_directory(args.directory)
    else:
        loader.load_class(ArgparseDjangoWorker, 'django')
        loader.load_class(GitWorker, 'git')

    if args.worker:
        if args.show:
            return loader.worker[args.worker].show()

        n = 4 if args.directory else 2
        return loader.run(args.worker, sys.argv[n:])

    elif args.show:
        return loader.show()

    parser.print_help()

if __name__ == '__main__':
    main()
