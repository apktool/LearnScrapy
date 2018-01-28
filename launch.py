import os
import argparse
from scrapy import cmdline

parser = argparse.ArgumentParser(
        prog='LearnScrapy',
        description='The operation releated to scrapy')

group_start = parser.add_argument_group('Start Scrapy')
group_start.add_argument('--start', action='store',
        dest='start_spider',
        help='sinaPersonalInfo')

group_start.add_argument('--stop', action='store',
        dest='stop_spider',
        help='Stop scrapy specified for sina spider')

group_start.add_argument('--restart', action='store',
        dest='restart_spider',
        help='Restart scrapy specified for sina spider')

args = parser.parse_args()
pid_file = os.path.join(os.getcwd(), 'scrapy.pid')


def start(spider):
    open(pid_file, 'w').write(str(os.getpid()))
    start_cmd = 'scrapy crawl ' + spider
    print('Scrapy->[{}]have been boot, Wait for a minute'.format(spider))
    cmdline.execute(start_cmd.split())


def start_all():
    open(pid_file, 'w').write(str(os.getpid()))
    start_cmd = 'scrapy crawlall'
    print('All Scrapy have been boot, Wait for a minute')
    cmdline.execute(start_cmd.split())


def stop():
    with open(pid_file, 'r') as f:
        pid = f.read()
    try:
        os.kill(int(pid), 9)
    except OSError:
        print('Scrapy is not processed')
    else:
        print('Scrapy is exited')


if __name__ == '__main__':
    if args.start_spider == 'all':
        start_all()
    elif args.start_spider is not None:
        start(args.start_spider)

    if args.stop_spider is not None:
        stop()

    if args.restart_spider == 'all':
        stop()
        start_all()
    elif args.restart_spider is not None:
        stop()
        start(args.restart_spider)
