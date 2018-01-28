import os
import argparse
from scrapy import cmdline

parser = argparse.ArgumentParser(
        prog='LearnScrapy',
        description='The operation releated to scrapy')

group_start = parser.add_argument_group('Start Scrapy')
group_start.add_argument('--run', action='store',
        dest='run_value',
        help='Start scrapy for sina spider')
args = parser.parse_args()
pid_file = os.path.join(os.getcwd(), 'scrapy.pid')


def start():
    open(pid_file, 'w').write(str(os.getpid()))
    start_cmd = 'scrapy crawl sinaPersonalInfo'
    print('Scrapy have been boot, Wait for a minute')
    cmdline.execute(start_cmd.split())


def start_all():
    open(pid_file, 'w').write(str(os.getpid()))
    start_cmd = 'scrapy crawlall'
    print('Scrapy have been boot, Wait for a minute')
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
    if args.run_value == 'start':
        start()
    if args.run_value == 'startall':
        start_all()
    if args.run_value == 'stop':
        stop()
    if args.run_value == 'restart':
        stop()
        start()
