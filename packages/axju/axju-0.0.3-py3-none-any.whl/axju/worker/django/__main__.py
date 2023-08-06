import logging

from axju.worker.django import ArgparseDjangoWorker, DjangoWorker

def main():
    '''worker = DjangoWorker()

    worker.logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    ch.setLevel(logging.INFO)
    worker.logger.addHandler(ch)

    worker.load_project('.', 'production')
    worker.run_step('run')'''
    worker = ArgparseDjangoWorker()
    #worker.parse()
    worker.run()

if __name__ == '__main__':
    main()
