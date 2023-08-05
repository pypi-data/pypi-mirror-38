from axju.core.tools import SmartCLI
from axju.worker.django import DjangoWorker

def main():
    cli = SmartCLI(DjangoWorker)
    cli.add_argument('--folder', type=str, help='The django project folder.')
    cli.add_argument('--setting', type=str, help='Change the default the settings.')
    cli.run()

if __name__ == '__main__':
    main()
