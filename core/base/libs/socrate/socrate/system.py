import hmac
import logging as log
import os
import signal
import sys
import re
from pwd import getpwnam
import socket
import tenacity
import subprocess
import threading

@tenacity.retry(stop=tenacity.stop_after_attempt(100),
                wait=tenacity.wait_random(min=2, max=5))
def resolve_hostname(hostname):
    """ This function uses system DNS to resolve a hostname.
    It is capable of retrying in case the host is not immediately available
    """
    try:
        return sorted(socket.getaddrinfo(hostname, None, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE), key=lambda s:s[0])[0][4][0]
    except Exception as e:
        log.warning("Unable to lookup '%s': %s",hostname,e)
        raise e

def _coerce_value(value):
    if isinstance(value, str) and value.lower() in ('true','yes'):
        return True
    elif isinstance(value, str) and value.lower() in ('false', 'no'):
        return False
    return value

class LogFilter(object):
    def __init__(self, stream, re_patterns):
        self.stream  = stream
        self.pattern = re.compile(b'|'.join([b''.join([b'(?:', pattern, b')']) for pattern in re_patterns]))
        self.buffer  = b''

    def __getattr__(self, attr_name):
        return getattr(self.stream, attr_name)

    def write(self, data):
        if type(data) is str:
            data = data.encode('utf-8')
        self.buffer += data
        while b'\n' in self.buffer:
            line, cr, rest = self.buffer.partition(b'\n')
            if not self.pattern.search(line):
                self.stream.buffer.write(line)
                self.stream.buffer.write(cr)
                self.stream.flush()
            self.buffer = rest

    def flush(self):
        # write out buffer on flush even if it's not a complete line
        if self.buffer and not self.pattern.search(self.buffer):
            self.stream.buffer.write(self.buffer)
        self.stream.flush()

def _is_compatible_with_hardened_malloc():
    with open('/proc/version', 'r') as f:
        major, minor = f.readline().split()[2].split('.')[:2]
        if int(major) < 6 or int(major) == 6 and int(minor) < 1:
            return False

    with open('/proc/cpuinfo', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # See #2764, we need vmovdqu
            # See #2959, we need vpunpckldq
            if line.startswith('flags') and ' avx2 ' not in line:
                return False
            # See #2541
            if line.startswith('Features') and ' lrcpc ' not in line:
                return False
    return True


def sigterm_handler(_signo, _stack_frame):
    log.critical("Received SIGTERM, terminating.")
    sys.exit(143)

def set_env(required_secrets=[], log_filters=[]):
    if log_filters:
        sys.stdout = LogFilter(sys.stdout, log_filters)
        sys.stderr = LogFilter(sys.stderr, log_filters)
    log.basicConfig(stream=sys.stderr, level=os.environ.get("LOG_LEVEL", 'WARNING'))
    signal.signal(signal.SIGTERM, sigterm_handler)

    if _is_compatible_with_hardened_malloc():
        if not 'LD_PRELOAD' in os.environ and _is_compatible_with_hardened_malloc():
            log.warning('Your CPU has Advanced Vector Extensions available, we recommend you enable hardened-malloc earlier in the boot process by adding LD_PRELOAD=/usr/lib/libhardened_malloc.so to your mailu.env')
            os.environ['LD_PRELOAD'] = '/usr/lib/libhardened_malloc.so'
        with open('/proc/sys/vm/max_map_count', 'r') as f:
            if int(f.readline()) < 1048576:
                log.warning('Please consider increasing vm.max_map_count to 1048576 as per https://github.com/GrapheneOS/hardened_malloc?tab=readme-ov-file#traditional-linux-based-operating-systems')

    """ This will set all the environment variables and retains only the secrets we need """
    if 'SECRET_KEY_FILE' in os.environ:
        try:
            secret_key = open(os.environ.get("SECRET_KEY_FILE"), "r").read().strip()
        except Exception as exc:
            log.error(f"Can't read SECRET_KEY from file: {exc}")
            raise exc
    else:
        secret_key = os.environ.get('SECRET_KEY')
    clean_env()
    # derive the keys we need
    for secret in required_secrets:
        os.environ[f'{secret}_KEY'] = hmac.new(bytearray(secret_key, 'utf-8'), bytearray(secret, 'utf-8'), 'sha256').hexdigest()

    os.system(r'find /run -xdev -type f -name \*.pid -print -delete')

    return {
            key: _coerce_value(os.environ.get(key, value))
            for key, value in os.environ.items()
           }

def clean_env():
    """ remove all secret keys, normalize PROXY_PROTOCOL """
    [os.environ.pop(key, None) for key in os.environ.keys() if key.endswith("_KEY")]
    # Configure PROXY_PROTOCOL
    PROTO_MAIL=['25', '110', '995', '143', '993', '587', '465', '4190']
    PROTO_ALL_BUT_HTTP=PROTO_MAIL.copy()
    PROTO_ALL_BUT_HTTP.extend(['443'])
    PROTO_ALL=PROTO_ALL_BUT_HTTP.copy()
    PROTO_ALL.extend(['80'])
    for item in os.environ.get('PROXY_PROTOCOL', '').split(','):
        if item.isdigit():
            os.environ[f'PROXY_PROTOCOL_{item}']='True'
        elif item == 'mail':
            for p in PROTO_MAIL: os.environ[f'PROXY_PROTOCOL_{p}']='True'
        elif item == 'all-but-http':
            for p in PROTO_ALL_BUT_HTTP: os.environ[f'PROXY_PROTOCOL_{p}']='True'
        elif item == 'all':
            for p in PROTO_ALL: os.environ[f'PROXY_PROTOCOL_{p}']='True'
        elif item == '':
            pass
        else:
            log.error(f'Not sure what to do with {item} in PROXY_PROTOCOL ({args.get("PROXY_PROTOCOL")})')

    PORTS_REQUIRING_TLS=['443', '465', '993', '995']
    ALL_PORTS='25,80,443,465,993,995,4190'
    for item in os.environ.get('PORTS', ALL_PORTS).split(','):
        if item in PORTS_REQUIRING_TLS and os.environ.get('TLS_FLAVOR','') == 'notls':
            continue
        os.environ[f'PORT_{item}']='True'

    if os.environ.get('TLS_FLAVOR', '') != 'notls':
        for item in os.environ.get('TLS', ALL_PORTS).split(','):
            if item in PORTS_REQUIRING_TLS:
                os.environ[f'TLS_{item}']='True'
    if 'CPU_COUNT' not in os.environ:
        os.environ['CPU_COUNT'] = str(os.cpu_count())

def drop_privs_to(username='mailu'):
    pwnam = getpwnam(username)
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)
    os.environ['HOME'] = pwnam.pw_dir

# forwards text lines from src to dst in an infinite loop
def forward_text_lines(src, dst):
    while True:
        current_line = src.readline()
        dst.write(current_line)


# runs a process and passes its standard/error output to the standard/error output of the current python script
def run_process_and_forward_output(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout_thread = threading.Thread(target=forward_text_lines, args=(process.stdout, sys.stdout))
    stdout_thread.daemon = True
    stdout_thread.start()

    stderr_thread = threading.Thread(target=forward_text_lines, args=(process.stderr, sys.stderr))
    stderr_thread.daemon = True
    stderr_thread.start()

    rc = process.wait()
    sys.stdout.flush()
    sys.stderr.flush()
    return rc
