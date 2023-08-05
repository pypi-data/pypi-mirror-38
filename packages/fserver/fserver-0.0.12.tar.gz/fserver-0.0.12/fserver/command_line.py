# -*- coding: utf-8 -*-
import sys

from gevent.pywsgi import WSGIServer

from fserver import conf
from fserver import path_util
from fserver import util
from fserver.fserver_app import app as application

usage_short = 'usage: fserver [-h] [-d] [-u] [-o] [-u] [-o] [-i ADDRESS] [-w PATH] [port]'
usage = '''
Usage:
  fserver [-h] [-d] [-u] [-o] [-i ADDRESS] [port]

Positional arguments:
  port                  Specify alternate port [default: 2000]

Optional arguments:
  -h, --help            Show this help message and exit
  -d, --debug           Use debug mode of fserver
  -u, --upload          Open upload file function. This function is closed by default
  -o, --override        Set upload file with override mode, only valid when [-u] is used
  -i ADDRESS, --ip ADDRESS
                        Specify alternate bind address [default: all interfaces]
  -w PATH, --white PATH 
                        Use white_list mode. Only PATH, sub directory or file, will be share. 
                        You can use [-wi PATH], i is num from 1 to 23, to share 24 PATHs at most    
 '''


def run_fserver():
    # init conf
    CmdOption().init_conf(sys.argv[1:])

    if conf.DEBUG:
        conf.display()
    print('fserver is available at following address:')
    if conf.BIND_IP == '0.0.0.0':
        ips = util.get_ip_v4()
        for _ip in ips:
            print('  http://%s:%s' % (_ip, conf.BIND_PORT))
    else:
        print('  %s:%s' % (conf.BIND_IP, conf.BIND_PORT))

    http_server = WSGIServer((conf.BIND_IP, int(conf.BIND_PORT)), application)
    http_server.serve_forever()


class OptionError(Exception):
    def __init__(self, msg):
        self.msg = msg


def getopt(args, short_opts, long_opts=None):
    if long_opts is None:
        long_opts = []
    opts_2 = [('-' + i.replace(':', ''), True if i.endswith(':') else False) for i in short_opts]
    opts_2.extend([('--' + i.replace('=', ''), True if i.endswith('=') else False) for i in long_opts])
    options = []
    for ind, value in enumerate(args):
        if value is None:
            continue
        recognized = False
        for name, has_value in opts_2:
            if value == name:
                v = ''
                if has_value:
                    if ind == len(args) - 1:
                        raise OptionError('error: option %s requires argument' % value)
                    v = args[ind + 1]
                    args[ind + 1] = None
                options.append((value, v))
                recognized = True
                break
        if recognized:
            args[ind] = None
        elif value.startswith('-') and value != '-' and value != '--':
            raise OptionError('error: option %s not recognized' % value)

    none_count = 0
    for v in args:
        if v is None:
            none_count += 1
    for ind, value in enumerate(args):
        if value is not None and ind < none_count:
            raise OptionError(value)

    argv = [i for i in args if i is not None]
    return options, argv


class CmdOption:
    OPTIONS = {
        'help': ('h', 'help', ['--help', '-h']),
        'debug': ('d', 'debug', ['debug', '-d']),
        'upload': ('u', 'upload', ['--upload', '-u']),
        'override': ('o', 'override', ['--override', '-o']),
        'version': ('v', 'version', ['--version', '-v']),
        'ip': ('i:', 'ip=', ['--ip', '-i']),
        'white': ('w:', 'white=', ['--white', '-w']),
        'black': ('b:', 'black=', ['--black', '-b'])
    }
    for i in range(1, 24):
        OPTIONS['white%s' % i] = ('w%s:' % i, 'white%s=' % i, ['--white%s' % i, '-w%s' % i])
        OPTIONS['black%s' % i] = ('b%s:' % i, 'black%s=' % i, ['--black%s' % i, '-b%s' % i])

    def init_conf(self, string):
        short_opts = []
        long_opts = []
        for item in self.OPTIONS.items():
            short_opts.append(item[1][0])
            long_opts.append(item[1][1])

        try:
            options, args = getopt(string, short_opts, long_opts)
        except OptionError as e:
            print(usage_short)
            print(e.msg)
            sys.exit()

        if len(args) > 0:
            conf.BIND_PORT = args[0]

        conf.WHITE_LIST.clear()
        for name, value in options:
            if name in self.OPTIONS['help'][2]:
                print(usage)
                sys.exit()
            if name in ['-v', '--version']:
                print('fserver %s build at %s' % (conf.VERSION, conf.BUILD_TIME))
                print('Python %s' % sys.version)
                sys.exit()
            if name in self.OPTIONS['debug'][2]:
                conf.DEBUG = True
                continue
            if name in self.OPTIONS['upload'][2]:
                conf.UPLOAD = True
                continue
            if name in self.OPTIONS['override'][2]:
                conf.UPLOAD_OVERRIDE_MODE = True
                continue
            if name in self.OPTIONS['ip'][2]:
                conf.BIND_IP = value
                continue
            for white_opt in self.OPTIONS.keys():
                if not white_opt.startswith('white'):
                    continue
                if name in self.OPTIONS[white_opt][2]:
                    p = path_util.to_local_path(value)
                    if p.startswith('..'):
                        util.warning('not support up_level path : %s' % p)
                    else:
                        conf.WHITE_LIST.add(p)
            for black_opt in self.OPTIONS.keys():
                if not black_opt.startswith('black'):
                    continue
                if name in self.OPTIONS[black_opt][2]:
                    p = path_util.to_local_path(value)
                    if p.startswith('..'):
                        util.warning('not support up_level path : %s' % p)
                    else:
                        conf.BLACK_LIST.add(p)


if __name__ == '__main__':
    run_fserver()
