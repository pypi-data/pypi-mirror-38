from axju.core.tools import SmartCLI
from axju.worker.git import GitWorker

def main():
    cli = SmartCLI(GitWorker)
    cli.run()

if __name__ == '__main__':
    main()
