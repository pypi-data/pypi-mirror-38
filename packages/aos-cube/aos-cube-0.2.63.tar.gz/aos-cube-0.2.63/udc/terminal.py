#!/usr/bin/python

import os, sys, time, re, random, json, Queue
import curses, socket, ssl, select
import subprocess, thread, threading
import traceback
from operator import itemgetter
from os import path
import packet as pkt

MAX_MSG_LENGTH = 65536
CMD_WINDOW_HEIGHT = 2
DEV_WINDOW_WIDTH  = 36
LOG_WINDOW_HEIGHT = 30
LOG_WINDOW_WIDTH  = 80
LOG_HISTORY_LENGTH = 5000
MOUSE_SCROLL_UP = 0x80000
MOUSE_SCROLL_DOWN = 0x8000000
ENCRYPT = True
DEBUG = True

class ConnectionLost(Exception):
    pass

class Terminal:
    def __init__(self):
        self.stdscr = 0
        self.log_window = 0
        self.dev_window = 0
        self.cmd_window = 0
        self.keep_running = True
        self.connected = False
        self.device_list= {}
        self.service_socket = None
        self.cmd_excute_state = 'idle'
        self.cmd_excute_return = ''
        self.cmd_excute_event = threading.Event()
        self.output_queue = Queue.Queue(256)
        self.debug_socks = {}
        self.debug_queue = Queue.Queue(256)
        self.log_content = []
        self.log_curr_line = -1
        self.log_subscribed = []
        self.using_list = []
        self.max_log_width = 0
        self.cur_color_pair = 7
        self.alias_tuples = {}
        self.cmd_history = []
        self.last_runcmd_dev = []
        self.uuid = None

    def init(self):
        work_dir = path.join(path.expanduser('~'), '.udterminal')
        if path.exists(work_dir) == False:
            os.mkdir(work_dir)

        alias_file = path.join(path.expanduser('~'), '.udterminal', '.alias')
        if path.exists(alias_file) == True:
            try:
                file = open(alias_file, 'rb')
                self.alias_tuples = json.load(file)
                file.close()
            except:
                print 'read alias record failed'

        cmd_history_file = path.join(path.expanduser('~'), '.udterminal', '.cmd_history')
        if path.exists(cmd_history_file) == True:
            try:
                file = open(cmd_history_file, 'rb')
                self.cmd_history = json.load(file)
                file.close()
            except:
                print 'read command history failed'

        accesskey_file = path.join(path.expanduser('~'), '.udterminal', '.accesskey')
        if path.exists(accesskey_file) == True:
            try:
                file = open(accesskey_file, 'rb')
                self.uuid = json.load(file)
                file.close()
            except:
                print 'read access key failed'
        while self.uuid == None:
            try:
                uuid = raw_input('please input your access key: ')
            except:
                return 'read access key fail'
            is_valid_uuid = re.match('^[0-9a-f]{10,20}$', uuid)
            if is_valid_uuid == None:
                print 'invalid access key {0}, please enter a valid access key'.format(uuid)
                continue
            self.uuid = uuid
            try:
                accesskey_file = path.join(path.expanduser('~'), '.udterminal', '.accesskey')
                file = open(accesskey_file, 'wb')
                json.dump(self.uuid, file)
                file.close()
            except:
                print 'error: save access key to file failed'

        #initialize UI
        try:
            self.stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            curses.mousemask(-1)
            curses.mouseinterval(0)
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, -1)
            curses.init_pair(2, curses.COLOR_GREEN, -1)
            curses.init_pair(3, curses.COLOR_YELLOW, -1)
            curses.init_pair(4, curses.COLOR_BLUE, -1)
            curses.init_pair(5, curses.COLOR_MAGENTA, -1)
            curses.init_pair(6, curses.COLOR_CYAN, -1)
            curses.init_pair(7, curses.COLOR_WHITE, -1)
            self.curseslock = threading.Lock();
            self.window_redraw()
            return 'success'
        except:
            if DEBUG: traceback.print_exc()
            return 'UI failed'

    def window_redraw(self):
        global LOG_WINDOW_WIDTH
        global LOG_WINDOW_HEIGHT
        self.curseslock.acquire()
        (max_y, max_x) = self.stdscr.getmaxyx()
        for y in range(max_y):
            for x in range(max_x - 1):
                self.stdscr.addch(y, x, ' ')
        self.stdscr.refresh()
        LOG_WINDOW_HEIGHT = max_y - CMD_WINDOW_HEIGHT - 3
        LOG_WINDOW_WIDTH = max_x - DEV_WINDOW_WIDTH - 3
        width = 1 + LOG_WINDOW_WIDTH + 1 + DEV_WINDOW_WIDTH + 1
        height = 1 + LOG_WINDOW_HEIGHT + 1 + CMD_WINDOW_HEIGHT + 1
        horline = '-' * (width-2)
        self.stdscr.addstr(0, 1, horline)
        self.stdscr.addstr(LOG_WINDOW_HEIGHT + 1, 1, horline)
        self.stdscr.addstr(LOG_WINDOW_HEIGHT + CMD_WINDOW_HEIGHT + 2, 1, horline)
        for i in range(1, height-1):
            self.stdscr.addch(i, 0, '|')
        for i in range(1, height - CMD_WINDOW_HEIGHT - 2):
            self.stdscr.addch(i, LOG_WINDOW_WIDTH + 1, '|')
        for i in range(1, height-1):
            self.stdscr.addch(i, LOG_WINDOW_WIDTH + DEV_WINDOW_WIDTH + 2, '|')
        self.stdscr.refresh()
        x = 1; y = 1;
        self.log_window = curses.newwin(LOG_WINDOW_HEIGHT, LOG_WINDOW_WIDTH, y, x)
        x = 1 + LOG_WINDOW_WIDTH + 1; y = 1;
        self.dev_window = curses.newwin(LOG_WINDOW_HEIGHT, DEV_WINDOW_WIDTH, y, x)
        x = 1; y = 1 + LOG_WINDOW_HEIGHT + 1;
        self.cmd_window = curses.newwin(CMD_WINDOW_HEIGHT, LOG_WINDOW_WIDTH + 1 + DEV_WINDOW_WIDTH, y, x)
        self.cmd_window.keypad(1)
        self.log_window.addstr(0, 0, 'Logs', curses.A_BOLD)
        self.log_window.move(1, 0)
        self.log_window.refresh()
        self.dev_window.addstr(0, 0, 'Devices', curses.A_BOLD)
        self.dev_window.addstr(0, DEV_WINDOW_WIDTH-4, 'USE')
        self.dev_window.move(1, 0)
        self.dev_window.refresh()
        self.cmd_window.addstr(0, 0, 'Command:', curses.A_BOLD)
        self.cmd_window.refresh()
        self.curseslock.release()

    def process_esc_sequence(self, escape):
        colors = escape[2:-1].split(';')
        self.cur_color_pair = 7
        for color in colors:
            if color == '30':
                self.cur_color_pair = 0
            elif color == '31':
                self.cur_color_pair = 1
            elif color == '32':
                self.cur_color_pair = 2
            elif color == '33':
                self.cur_color_pair = 3
            elif color == '34':
                self.cur_color_pair = 4
            elif color == '35':
                self.cur_color_pair = 5
            elif color == '36':
                self.cur_color_pair = 6
            elif color == '37':
                self.cur_color_pair = 7

    def log_parse_oneline(self, log):
        log_buffer = []

        if ':' in log:
            log_index = log.split(':')[0] + ':'
        else:
            log_index = ''
        log = log[len(log_index):]
        log = log.replace('\t', ' ' * 8)
        line_length = len(log)
        j = 0; log_len = 0; log_str = log_index;
        while j < line_length:
            c = log[j]
            if c == '\x1B' and log[j:j+2] == '\x1B[': #ESC
                k = j + 2
                find_esc_seq = False
                while k < line_length:
                    if log[k] == 'm':
                        find_esc_seq = True
                        break
                    k += 1
                if find_esc_seq:
                    self.process_esc_sequence(log[j:k+1])
                    j = k + 1
                    continue
            if ord(c) >= 0x20 and ord(c) < 0x7F:
                log_str += c
                log_len += 1
                if log_len + len(log_index) >= LOG_WINDOW_WIDTH - 1:
                    log_buffer.append([self.cur_color_pair, log_str])
                    log_len = 0; log_str = log_index
            j += 1

        if log_len > 0:
            log_buffer.append([self.cur_color_pair, log_str])

        if len(log_buffer) == 0:
            log_buffer.append([self.cur_color_pair, log_index])

        return log_buffer

    def log_display(self, logtime, log):
        #save log
        if log != '':
            self.log_content.append((logtime, log))
            self.log_content.sort(key=itemgetter(0))
            if len(self.log_content) > LOG_HISTORY_LENGTH:
                self.log_content.pop(0)
                if self.log_curr_line > 0:
                    self.log_curr_line -= 1

        if self.log_curr_line != -1 and log != '':
            return

        #clear log screen
        self.log_window.move(1,0)
        clear = (' ' * (LOG_WINDOW_WIDTH - 1) + '\n') * (LOG_WINDOW_HEIGHT - 2)
        clear += ' ' * (LOG_WINDOW_WIDTH-1)
        self.log_window.addstr(clear)

        if self.log_curr_line >= 0:
            log_dsp_line = self.log_curr_line
        else:
            log_dsp_line = len(self.log_content) - 1

        log_dsp_buffer = []
        while log_dsp_line >= 0:
            log_line_buffer = self.log_parse_oneline(self.log_content[log_dsp_line][1])
            log_dsp_buffer = log_line_buffer + log_dsp_buffer
            log_dsp_line -= 1
            if len(log_dsp_buffer) >= (LOG_WINDOW_HEIGHT - 1):
                break
        remove_len = len(log_dsp_buffer) - (LOG_WINDOW_HEIGHT - 1)
        if remove_len > 0:
            log_dsp_buffer = log_dsp_buffer[remove_len:]

        self.curseslock.acquire()
        for i in range(len(log_dsp_buffer)):
            try:
                self.log_window.addstr(i+1, 0, log_dsp_buffer[i][1], curses.color_pair(log_dsp_buffer[i][0]))
            except:
                self.curseslock.release()
                if DEBUG:
                    print log_dsp_buffer[i]
                    print 'len:', len(log_dsp_buffer[i][1])
                    raise
                return

        self.log_window.refresh()
        self.cmd_window.refresh()
        self.curseslock.release()

    def device_list_display(self):
        self.curseslock.acquire()
        self.dev_window.move(1,0)
        clean = (' ' * (DEV_WINDOW_WIDTH-1) + '\n') * (LOG_WINDOW_HEIGHT - 2)
        clean += ' ' * (DEV_WINDOW_WIDTH-1)
        self.dev_window.addstr(clean)
        devices = list(self.device_list)
        devices.sort()
        if len(self.device_list) > 0:
            cuuid = devices[0].split(',')[0]
        linenum = 1
        for i in range(len(devices)):
            devfull = devices[i]
            dev = devfull.split(',')
            if dev[0] != cuuid:
                cuuid = dev[0]
                linenum += 1
            if dev[0] in self.alias_tuples:
                dev_str = str(i) + '.' + self.alias_tuples[dev[0]] + ':'
            else:
                dev_str = str(i) + '.' + dev[0] + ':'
            mid_len = DEV_WINDOW_WIDTH - len(dev_str) - 5
            devpath = dev[1].replace('/dev/','')
            if mid_len >= len(devpath):
                dev_str += devpath + ' '*(mid_len - len(devpath))
            else:
                dev_str += devpath[:mid_len]
            dev_str += '  ' + self.device_list[devfull]
            try:
                self.dev_window.addstr(linenum, 0, dev_str)
            except:
                pass
            linenum += 1
            if linenum >= LOG_WINDOW_HEIGHT:
                break
        self.dev_window.refresh()
        self.cmd_window.refresh()
        self.curseslock.release()

    def cmdrun_command_display(self, cmd, postion):
        self.curseslock.acquire()
        self.cmd_window.move(0, len('Command:'))
        self.cmd_window.addstr(' ' * (LOG_WINDOW_WIDTH + DEV_WINDOW_WIDTH - len('Command:')))
        self.cmd_window.move(0, len('Command:'))
        self.cmd_window.addstr(cmd)
        self.cmd_window.move(0, len('Command:') + postion)
        self.cmd_window.refresh()
        self.curseslock.release()

    def cmdrun_status_display(self, log):
        self.curseslock.acquire()
        self.cmd_window.move(1,0)
        self.cmd_window.addstr(' ' * (LOG_WINDOW_WIDTH + DEV_WINDOW_WIDTH))
        self.cmd_window.move(1,0)
        self.cmd_window.addstr(log[:(LOG_WINDOW_WIDTH + DEV_WINDOW_WIDTH)])
        self.cmd_window.refresh()
        self.curseslock.release()

    def packet_send_thread(self):
        heartbeat_timeout = time.time() + 10
        while self.keep_running:
            try:
                [type, content] = self.output_queue.get(block=True, timeout=0.1)
            except Queue.Empty:
                type = None
                pass
            if self.service_socket == None:
                continue
            if type == None:
                if time.time() < heartbeat_timeout:
                    continue
                heartbeat_timeout += 10
                data = pkt.construct(pkt.HEARTBEAT,'')
            else:
                data = pkt.construct(type, content)
            try:
                self.service_socket.send(data)
            except:
                self.connected = False
                continue

    def send_packet(self, type, content, timeout=0.1):
        if self.service_socket == None:
            return False
        try:
            self.output_queue.put([type, content], True, timeout)
            return True
        except Queue.Full:
            if DEBUG: self.log_display(time.time(), 'error: ouput buffer full, drop packet [{0] {1}]'.format(type, content))
        return False

    def get_devstr_by_index(self, index):
        devices = list(self.device_list)
        devices.sort()
        return devices[index]

    def get_index_by_devstr(self, devstr):
        devices = list(self.device_list)
        devices.sort()
        return devices.index(devstr)

    def login_and_get_server(self, controller_ip, controller_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ENCRYPT:
            cert_file = path.join(path.dirname(path.abspath(__file__)), 'controller_certificate.pem')
            sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, ca_certs = cert_file)
        try:
            sock.connect((controller_ip, controller_port))
            sock.settimeout(3)
            msg = ''
        except:
            if DEBUG: traceback.print_exc()
            return None

        content = pkt.construct(pkt.ACCESS_LOGIN, 'terminal,' + self.uuid)
        try:
            sock.send(content)
        except:
            if DEBUG: traceback.print_exc()
            sock.close()
            return None

        try:
            data = sock.recv(MAX_MSG_LENGTH)
        except KeyboardInterrupt:
            sock.close()
            raise
        except:
            sock.close()
            return None

        if data == '':
            sock.close()
            return None

        type, length, value, data = pkt.parse(data)
        #print 'controller', type, value
        rets = value.split(',')
        if type != pkt.ACCESS_LOGIN or rets[0] != 'success':
            if rets[0] == 'invalid access key':
                self.log_display(time.time(), 'login to controller failed, invalid access key')
                accesskey_file = path.join(path.expanduser('~'), '.udterminal', '.accesskey')
                if path.exists(accesskey_file):
                    os.remove(accesskey_file)
            else:
                self.log_display(time.time(), 'login to controller failed, ret={0}'.format(value))
            sock.close()
            return None

        sock.close()
        return rets[1:]

    def connect_to_server(self, server_ip, server_port, certificate):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if certificate != 'None':
            try:
                certfile = path.join(path.expanduser('~'), '.udterminal', 'certificate.pem')
                f = open(certfile, 'wt')
                f.write(certificate)
                f.close()
                sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, ca_certs=certfile)
            except:
                return 'fail'
        try:
            sock.connect((server_ip, server_port))
            while self.output_queue.empty() == False:
                self.output_queue.get()
            self.service_socket = sock
            self.connected = True
            return 'success'
        except:
            return 'fail'

    def server_interaction(self):
        self.connected = False
        self.service_socket = None
        msg = ''
        while self.keep_running:
            try:
                if self.connected == False:
                    raise ConnectionLost

                new_msg = self.service_socket.recv(MAX_MSG_LENGTH)
                if new_msg == '':
                    raise ConnectionLost
                    break

                msg += new_msg
                while msg != '':
                    type, length, value, msg = pkt.parse(msg)
                    if type == pkt.TYPE_NONE:
                        break

                    #print type, length
                    if type == pkt.FILE_BEGIN:
                        if 'file' in locals() and file.closed == False:
                            file.close()
                        filename = path.join(path.expanduser('~'), '.udterminal', value)
                        file = open(filename, 'w')
                        continue
                    if type == pkt.FILE_DATA:
                        if 'file' in locals() and file.closed == False:
                            file.write(value)
                        continue
                    if type == pkt.FILE_END:
                        if 'file' in locals():
                            file.close()
                        continue
                    if type == pkt.ALL_DEV:
                        new_list = {}
                        clients = value.split(':')
                        for c in clients:
                            if c == '':
                                continue
                            devs = c.split(',')
                            uuid = devs[0]
                            devs = devs[1:]
                            for d in devs:
                                if d == '':
                                    continue
                                [dev, using] = d.split('|')
                                new_list[uuid + ',' + dev] = using

                        for dev in list(new_list):
                            self.device_list[dev] = new_list[dev]

                        for dev in list(self.device_list):
                            if dev not in list(new_list):
                                self.device_list.pop(dev)
                        self.device_list_display()
                        continue
                    if type == pkt.DEVICE_LOG:
                        dev = value.split(':')[0]
                        logtime = value.split(':')[1]
                        log = value[len(dev) + 1 + len(logtime):]
                        try:
                            logtime = float(logtime)
                        except:
                            continue
                        if dev not in list(self.device_list):
                            continue
                        index = self.get_index_by_devstr(dev)
                        if dev in self.log_subscribed:
                            log =  str(index) + log
                            self.log_display(logtime, log)
                        continue
                    if type == pkt.DEVICE_DEBUG_DATA:
                        dev = value.split(':')[0]
                        if dev not in list(self.device_list):
                            continue
                        data = value[len(dev)+1:]
                        if dev not in self.debug_socks:
                            continue
                        try:
                            self.debug_socks[dev].sendall(data)
                        except:
                            index = self.get_index_by_devstr(dev)
                            self.log_display(time.time(), 'forwording debug data for {0} failed'.format(index))
                    if type in [pkt.DEVICE_DEBUG_START, pkt.DEVICE_DEBUG_REINIT, pkt.DEVICE_DEBUG_STOP]:
                        #self.log_display(time.time(), '{0}'.format([type, value]))
                        try:
                            [dev, result] = value.split(':')
                        except:
                            self.log_display(time.time(), 'error: wrong data {0} {1}'.format(type,value))
                            continue
                        if dev not in list(self.device_list):
                            continue
                        message = [type, dev, result]
                        if self.debug_queue.full() == True:
                            self.log_display(time.time(), 'local debug deamon busy, discard packet {0}'.format([type, value]))
                            continue
                        self.debug_queue.put(message)
                        continue
                    if type == pkt.CMD_DONE:
                        self.cmd_excute_return = value
                        self.cmd_excute_state = 'done'
                        self.cmd_excute_event.set()
                        continue
                    if type == pkt.CMD_ERROR:
                        self.cmd_excute_return = value
                        self.cmd_excute_state = 'error'
                        self.cmd_excute_event.set()
                        continue
                    if type == pkt.TERMINAL_LOGIN:
                        if value == 'success':
                            continue
                        self.cmdrun_status_display('login to server failed, retry later ...')
                        time.sleep(10)
                        continue
            except ConnectionLost:
                self.connected = False
                if self.service_socket != None:
                    self.service_socket.close()
                    self.service_socket = None
                    self.cmdrun_status_display('connection to server lost, try reconnecting...')

                result = self.login_and_get_server(self.controller_ip, self.controller_port)
                if result == None:
                    self.cmdrun_status_display('login to controller failed, retry later...')
                    time.sleep(5)
                    continue
                try:
                    [server_ip, server_port, token, certificate] = result
                    server_port = int(server_port)
                except:
                    self.log_display(time.time(), 'login to controller failed, invalid return={0}'.format(result))
                    self.cmdrun_status_display('login to controller failed, retry later...')
                    time.sleep(5)
                    continue

                result = self.connect_to_server(server_ip, server_port, certificate)
                if result == 'success':
                    self.cmdrun_status_display('connect to server succeeded')
                else:
                    self.cmdrun_status_display('connect to server failed, retry later ...')
                    time.sleep(5)
                    continue

                data = self.uuid + ',' + token
                self.send_packet(pkt.TERMINAL_LOGIN, data)
            except:
                if DEBUG:
                    raise
                break
        self.keep_running = False;

    def debug_interaction(self):
        debug_sessions = {}
        while self.keep_running:
            if debug_sessions == {} or self.debug_queue.empty() == False:
                [type, device, result] = self.debug_queue.get()
                index = self.get_index_by_devstr(device)
                if type == pkt.DEVICE_DEBUG_START:
                    if result != 'success':
                        self.log_display(time.time(), 'error: start debug device {0} failed, ret={1}'.format(index, result))
                        self.cmd_excute_return = result
                        self.cmd_excute_state = 'error'
                        self.cmd_excute_event.set()
                        continue

                    if device in debug_sessions:
                        self.cmd_excute_return = port
                        self.cmd_excute_state = 'done'
                        self.cmd_excute_event.set()
                        port = debug_sessions[device]['port']
                        self.log_display(time.time(), 'start debugging {0} succeed, serve at port {1}'.format(index, port))
                        continue
                    used_ports = []
                    for device in debug_sessions:
                        used_ports.append(debug_sessions[device]['port'])
                    port = 4120 + ord(os.urandom(1)) * ord(os.urandom(1)) / 64
                    while port in used_ports:
                        port = 4120 + ord(os.urandom(1)) * ord(os.urandom(1)) / 64
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.setblocking(False)
                    try:
                        sock.bind(('localhost', port))
                    except:
                        self.log_display(time.time(), 'start debugging {0} failed, listen at port {1} failed'.format(index, port))
                        self.cmd_excute_return = 'fail'
                        self.cmd_excute_state = 'error'
                        self.cmd_excute_event.set()
                        continue
                    sock.listen(1)
                    debug_sessions[device] = {'port': port, 'listen_sock': sock}
                    self.log_display(time.time(), 'start debugging {0} succeed, serve at port {1}'.format(index, port))
                    self.cmd_excute_return = port
                    self.cmd_excute_state = 'done'
                    self.cmd_excute_event.set()
                elif type == pkt.DEVICE_DEBUG_REINIT:
                    if result == 'success':
                        continue
                    self.log_display(time.time(), 'error: restart debugging device {0} failed, ret={1}, closing debug session'.format(index, result))
                    if device not in debug_sessions:
                        continue
                    if 'serve_sock' in debug_sessions[device]:
                        self.debug_socks.pop(device)
                        debug_sessions[device]['serve_sock'].close()
                    debug_sessions[device]['listen_sock'].close()
                    debug_sessions.pop(device)
                elif type == pkt.DEVICE_DEBUG_STOP:
                    self.cmd_excute_return = result
                    if result == 'success':
                        self.cmd_excute_state = 'done'
                    else:
                        self.cmd_excute_state = 'error'
                    self.cmd_excute_event.set()

                    if device not in debug_sessions:
                        continue
                    self.log_display(time.time(), 'stop debugging {0}: {1}'.format(index, result))
                    if 'serve_sock' in debug_sessions[device]:
                        debug_sessions[device]['serve_sock'].close()
                    debug_sessions[device]['listen_sock'].close()
                    debug_sessions.pop(device)
                else:
                    self.log_display(time.time(), "error: wrong debug msg type '{0}'".format(type))
                continue

            select_list = {}
            for device in debug_sessions:
                if 'serve_sock' in debug_sessions[device]:
                    sock = debug_sessions[device]['serve_sock']
                    operation = 'recv'
                else:
                    sock = debug_sessions[device]['listen_sock']
                    operation = 'accept'
                select_list[sock] = [operation, device]

            r, w, e = select.select(list(select_list), [], [], 0.02)
            for sock in r:
                [operation, device] = select_list[sock]
                if operation == 'accept':
                    conn, addr = sock.accept()
                    conn.setblocking(0)
                    debug_sessions[device]['serve_sock'] = conn
                    self.debug_socks[device] = conn
                else:
                    try:
                        data = sock.recv(MAX_MSG_LENGTH)
                    except:
                        data = None
                    if not data:
                        debug_sessions[device].pop('serve_sock')
                        self.debug_socks.pop(device)
                        sock.close()
                        #self.log_display(time.time(), 'debug client disconnected')
                        self.send_packet(pkt.DEVICE_DEBUG_REINIT, device)
                        continue
                    content = device + ':' + data
                    self.send_packet(pkt.DEVICE_DEBUG_DATA, content)

    def parse_device_index(self, index_str):
        max = len(self.device_list) - 1
        if '-' in index_str:
            index_split = index_str.split('-')
            if len(index_split) != 2 or index_split[0].isdigit() == False or index_split[1].isdigit() == False:
                return [];
            try:
                start = int(index_split[0])
                end   = int(index_split[1])
                if start > max and end > max:
                    return []
                if start > max:
                    start = max
                if end > max:
                    end = max
            except:
                return [];
            if start < end:
                return range(start, end + 1, 1)
            else:
                return range(start, end - 1, -1)
        else:
            if index_str.isdigit() == False:
                return []
            try:
                index = int(index_str)
            except:
                return []
            if index >= len(self.device_list):
                return []
            return [index]

    def wait_cmd_excute_done(self, timeout):
        self.cmd_excute_state = 'wait_response'
        self.cmd_excute_return = None
        self.cmd_excute_event.clear()
        if self.cmd_excute_event.wait(timeout) == False:
            self.cmd_excute_state = 'timeout'

    def send_file_to_client(self, filename, index):
        status_str = 'sending file {0} to {1}...'.format(filename, self.get_devstr_by_index(index).split(',')[0])
        self.cmdrun_status_display(status_str)
        filehash = pkt.hash_of_file(filename)
        devstr = self.get_devstr_by_index(index)

        #send file begin
        content = devstr  + ':' + filehash + ':' + filename.split('/')[-1]
        retry = 4
        while retry > 0:
            self.send_packet(pkt.FILE_BEGIN, content)
            self.wait_cmd_excute_done(0.2)
            if self.cmd_excute_state == 'timeout':
                retry -= 1;
                continue
            if self.cmd_excute_return == 'busy':
                time.sleep(5)
                continue
            elif self.cmd_excute_return == 'ok' or self.cmd_excute_return == 'exist':
                break
            else:
                status_str += 'error'
                self.cmdrun_status_display(status_str)
                return False
        if retry == 0:
            status_str += 'error'
            self.cmdrun_status_display(status_str)
            return False

        if self.cmd_excute_return == 'exist':
            status_str += 'done'
            self.cmdrun_status_display(status_str)
            return True

        #send file data
        seq = 0
        file = open(filename,'r')
        header = devstr  + ':' + filehash + ':' + str(seq) + ':'
        content = file.read(8192)
        while(content):
            retry = 4
            while retry > 0:
                self.send_packet(pkt.FILE_DATA, header + content)
                self.wait_cmd_excute_done(0.2)
                if self.cmd_excute_return == None:
                    retry -= 1;
                    continue
                elif self.cmd_excute_return != 'ok':
                    status_str += 'error'
                    self.cmdrun_status_display(status_str)
                    file.close()
                    return False
                break

            if retry == 0:
                status_str += 'error'
                self.cmdrun_status_display(status_str)
                file.close()
                return False

            seq += 1
            header = devstr  + ':' + filehash + ':' + str(seq) + ':'
            content = file.read(8192)
        file.close()

        #send file end
        content = devstr  + ':' + filehash + ':' + filename.split('/')[-1]
        retry = 4
        while retry > 0:
            self.send_packet(pkt.FILE_END, content)
            self.wait_cmd_excute_done(0.2)
            if self.cmd_excute_return == None:
                retry -= 1;
                continue
            elif self.cmd_excute_return != 'ok':
                status_str += 'error'
                self.cmdrun_status_display(status_str)
                return False
            break
        if retry == 0:
            status_str += 'error'
            self.cmdrun_status_display(status_str)
            return False

        status_str += 'done'
        self.cmdrun_status_display(status_str)
        return True

    def erase_devices(self, args):
        devs = args
        if devs == []:
            self.cmdrun_status_display('Usage error: please specify devices you want to programg')
            return False
        succeed = []; failed = []
        for dev in devs:
            indexes = self.parse_device_index(dev)
            if indexes == []:
                self.cmdrun_status_display('invalid device index {0}'.format(dev))
                continue

            for index in indexes:
                status_str = 'erasing {0}.{1}...'.format(index, self.get_devstr_by_index(index))
                self.cmdrun_status_display(status_str)
                dev_str = self.get_devstr_by_index(index)
                self.send_packet(pkt.DEVICE_ERASE, dev_str);
                self.wait_cmd_excute_done(10)
                status_str += self.cmd_excute_state
                self.cmdrun_status_display(status_str)
                if self.cmd_excute_state == 'done':
                    succeed.append(index)
                else:
                    failed.append(index)
                self.cmd_excute_state = 'idle'
                if dev_str not in self.using_list:
                    self.using_list.append(dev_str)
        status_str = ''
        if succeed != []:
            status_str += 'succeed: {0}'.format(succeed)
        if failed != []:
            if status_str != '':
                status_str += ', '
            status_str += 'failed: {0}'.format(failed)
        self.cmdrun_status_display(status_str)

    def program_devices(self, args):
        if len(args) < 3:
            self.cmdrun_status_display('Usage: programg addresse filename device0 [device1 device2 ... deviceN]')
            return False
        if args[0].startswith('0x') == False:
            self.cmdrun_status_display('Usage error: wrong address input {0}, address should start with 0x'.format(args[0]))
            return False
        address  = args[0]
        filename = args[1]
        try:
            expandname = path.expanduser(filename)
        except:
            self.cmdrun_status_display('{0} does not exist'.format(filename))
            return False
        if path.exists(expandname) == False:
            self.cmdrun_status_display('{0} does not exist'.format(filename))
            return False
        filehash = pkt.hash_of_file(expandname)

        devs = args[2:]
        file_exist_at = []
        if devs == []:
            self.cmdrun_status_display('Usage error: please specify devices you want to programg')
            return False
        succeed = []; failed = []
        for dev in devs:
            indexes = self.parse_device_index(dev)
            if indexes == []:
                self.cmdrun_status_display('invalid device index {0}'.format(dev))
                continue
            for index in indexes:
                dev_str = self.get_devstr_by_index(index)
                [uuid, port] = dev_str.split(',')
                if uuid not in file_exist_at:
                    if self.send_file_to_client(expandname, index) == False:
                        failed.append(index)
                        continue
                    file_exist_at.append(uuid)
                status_str = 'programming {0} to {1}.{2}:{3}...'.format(filename, index, uuid, port.replace('/dev/', ''))
                self.cmdrun_status_display(status_str)
                content = dev_str + ',' + address + ',' + filehash
                self.send_packet(pkt.DEVICE_PROGRAM, content);
                self.wait_cmd_excute_done(270)
                status_str += self.cmd_excute_state
                self.cmdrun_status_display(status_str)
                if self.cmd_excute_state == 'done':
                    succeed.append(index)
                else:
                    failed.append(index)
                self.cmd_excute_state = 'idle'
                if dev_str not in self.using_list:
                    self.using_list.append(dev_str)
        status_str = ''
        if succeed != []:
            status_str += 'succeed: {0}'.format(succeed)
        if failed != []:
            if status_str != '':
                status_str += ', '
            status_str += 'failed: {0}'.format(failed)
        self.cmdrun_status_display(status_str)

    def control_devices(self, operate, args):
        if len(args) < 1:
            self.cmdrun_status_display('Usage error, usage: reset devices')
            return False

        operations = {'start':pkt.DEVICE_START, 'stop':pkt.DEVICE_STOP, 'reset':pkt.DEVICE_RESET}
        operate = operations[operate]
        succeed = []; failed = []
        for dev in args:
            indexes = self.parse_device_index(dev)
            if indexes == []:
                self.cmdrun_status_display('invalid device index {0}'.format(dev))
                return False

            for index in indexes:
                dev_str = self.get_devstr_by_index(index)
                self.send_packet(operate, dev_str)
                self.wait_cmd_excute_done(1.5)
                if self.cmd_excute_state == 'done':
                    succeed.append(index)
                else:
                    failed.append(index)
                self.cmd_excute_state = 'idle'
                if dev_str not in self.using_list:
                    self.using_list.append(dev_str)
        status_str = ''
        if succeed != []:
            status_str += 'succeed: {0}'.format(succeed)
        if failed != []:
            if status_str != '':
                status_str += ', '
            status_str += 'failed: {0}'.format(failed)
        self.cmdrun_status_display(status_str)

    def log_on_off(self, args):
        if len(args) < 2:
            self.cmdrun_status_display('Usage error, usage: log on/off devices')
            return False

        if args[0] == 'on':
            type = pkt.LOG_SUB
        elif args[0] == 'off':
            type = pkt.LOG_UNSUB
        else:
            self.cmdrun_status_display('Usage error, usage: log on/off devices')
            return False

        for dev in args[1:]:
            indexes = self.parse_device_index(dev)
            if not indexes:
                self.cmdrun_status_display('invalid device index {0}'.format(dev))
                continue
            for index in indexes:
                dev_str = self.get_devstr_by_index(index)
                if type == pkt.LOG_SUB and dev_str not in self.log_subscribed:
                    self.send_packet(type, dev_str)
                    self.log_subscribed.append(dev_str)
                elif type == pkt.LOG_UNSUB and dev_str in self.log_subscribed:
                    self.send_packet(type, dev_str)
                    self.log_subscribed.remove(dev_str)

    def log_download(self, args):
        if len(args) < 1:
            self.cmdrun_status_display('Usage error, usage: logdownload device0 [device1 ... deviceN]')
            return False

        succeed = []; failed = []
        for dev in args:
            indexes = self.parse_device_index(dev)
            if indexes == []:
                self.cmdrun_status_display('invalid device index {0}'.format(dev))
                return False
            for index in indexes:
                device = self.get_devstr_by_index(index).split(',')
                status_str = 'downloading log file for {0}.{1}:{2}...'.format(index, device[0], device[1].replace('/dev/', ''))
                self.cmdrun_status_display(status_str)
                content = ','.join(device)
                self.send_packet(pkt.LOG_DOWNLOAD, content)
                self.wait_cmd_excute_done(480)
                if self.cmd_excute_state == 'done':
                    succeed.append(index)
                else:
                    failed.append(index)
                self.cmd_excute_state = 'idle'
        status_str = ''
        if succeed != []:
            status_str += 'succeed: {0}'.format(succeed)
        if failed != []:
            if status_str != '':
                status_str += ', '
            status_str += 'failed: {0}'.format(failed)
        self.cmdrun_status_display(status_str)
        return (len(failed) == 0)

    def run_command(self, args, uselast = False):
        if uselast == False:
            if len(args) < 2:
                self.cmdrun_status_display('Usage error, usage: runcmd device cmd_arg0 [cmd_arg1 cmd_arg2 ... cmd_argN]')
                return False

            indexes = self.parse_device_index(args[0])
            if indexes == []:
                self.cmdrun_status_display('invalid device index {0}'.format(args[0]))
                return False
            args = args[1:]
            self.last_runcmd_dev = self.get_devstr_by_index(indexes[-1])
        else:
            if self.last_runcmd_dev == []:
                self.cmdrun_status_display('Error: you have not excute any remote command with runcmd yet, no target remembered')
                return False

            if len(args) < 1:
                self.cmdrun_status_display('Usage error, usage: !cmd_arg0 [cmd_arg1 cmd_arg2 ... cmd_argN]')
                return False

            if self.last_runcmd_dev not in list(self.device_list):
                self.cmdrun_status_display('Error: remembered target no longer exists')
                return False
            indexes = [self.get_index_by_devstr(self.last_runcmd_dev)]

        succeed = []; failed = []
        for index in indexes:
            dev_str = self.get_devstr_by_index(index)
            content = dev_str + ':' + '|'.join(args)
            self.send_packet(pkt.DEVICE_CMD, content)
            self.wait_cmd_excute_done(1.5)
            if self.cmd_excute_state == 'done':
                succeed.append(index)
            else:
                failed.append(index)
            self.cmd_excute_state = 'idle'
            if self.cmd_excute_return == None:
                self.cmd_excute_return = 'timeout'
            status_str = '{0} run: '.format(index) + ' '.join(args) + ', ' + self.cmd_excute_return
            self.cmdrun_status_display(status_str)
            if dev_str not in self.using_list:
                self.using_list.append(dev_str)
        if len(indexes) == 1:
            return True
        status_str = ''
        if succeed != []:
            status_str += 'succeed: {0}'.format(succeed)
        if failed != []:
            if status_str != '':
                status_str += ', '
            status_str += 'failed: {0}'.format(failed)
        self.cmdrun_status_display(status_str)
        return (len(failed) == 0)

    def run_debug(self, args, uselast = False):
        if len(args) < 2 or args[0] not in ['start', 'stop']:
            self.cmdrun_status_display('Usage error, usage: debug start/stop device1 [device2 .. deviceN] ')
            return False
        operation = args[0]
        devs = args[1:]
        indexes = []; devices = {}
        for dev in devs:
            indexes += self.parse_device_index(dev)
        if indexes == []:
            self.cmdrun_status_display('invalid device index {0}'.format(' '.join(devs)))
            return False
        indexes = list(set(indexes))
        for index in indexes:
            devices[self.get_devstr_by_index(index)] = index

        if operation == 'start':
            type = pkt.DEVICE_DEBUG_START
        else:
            type = pkt.DEVICE_DEBUG_STOP

        succeed = []; failed = []
        for device in list(devices):
            if device not in self.device_list:
                continue
            self.send_packet(type, device)
            self.wait_cmd_excute_done(2)
            if self.cmd_excute_state == 'done':
                succeed.append(devices[device])
            else:
                failed.append(devices[device])
        status_str = ''
        if succeed != []:
            status_str += 'succeed: {0}'.format(succeed)
        if failed != []:
            if status_str != '':
                status_str += ', '
            status_str += 'failed: {0}'.format(failed)
        self.cmdrun_status_display(status_str)
        return (len(failed) == 0)

    def client_alias(self, args):
        if len(args) < 1:
            self.cmdrun_status_display('Usage error, usage: alias id0:name0 [id1:name1 ... idN:nameN]')
            return False

        for arg in args:
            alias = arg.split(':')
            if len(alias) != 2:
                self.cmdrun_status_display('Usage error, unrecongnized alias tuple {0}'.format(arg))
                continue
            self.alias_tuples[alias[0]] = alias[1]
        try:
            alias_file = path.join(path.expanduser('~'), '.udterminal', '.alias')
            file = open(alias_file, 'wb')
            json.dump(self.alias_tuples, file)
            file.close()
        except:
            self.cmdrun_status_display('error: save alias record failed')
        self.device_list_display()

    def print_help_info(self):
        self.log_display(time.time(), 'Supported commands and usage examples:')
        self.log_display(time.time(), ' 1.erase      [er]: erase flash of devices')
        self.log_display(time.time(), '           example: erase 0 1 2-5')
        self.log_display(time.time(), ' 2.program    [pg]: program fireware to devices')
        self.log_display(time.time(), '           example: program 0x40000 aos_esp32.bin 0 1 5-10')
        self.log_display(time.time(), ' 3.reset      [rs]: reset/restart devices')
        self.log_display(time.time(), '           example: reset 0 1 3-8')
        self.log_display(time.time(), ' 4.stop       [sp]: stop devices')
        self.log_display(time.time(), '           example: stop 0 5-7 9')
        self.log_display(time.time(), ' 5.start      [st]: start devices')
        self.log_display(time.time(), '           example: start 3-5 0 1')
        self.log_display(time.time(), ' 6.runcmd     [rc]: run command at remote device')
        self.log_display(time.time(), '           example: runcmd 0 ping fc:00:00:10:11:22:33:44')
        self.log_display(time.time(), '                    runcmd 0-10 umesh status')
        self.log_display(time.time(), ' 7.^              : run command at latest (runcmd) remote device')
        self.log_display(time.time(), '           example: ^ping fc:00:00:10:11:22:33:44')
        self.log_display(time.time(), ' 8.debug      [db]: start/stop debugging remote device')
        self.log_display(time.time(), '           example: debug start 0')
        self.log_display(time.time(), '                    debug stop 1')
        self.log_display(time.time(), ' 9.log        [lg]: turn on/off log display for devices, eg.: log on 1')
        self.log_display(time.time(), '           example: log on 1 2 5-8; log off 2-5 7')
        self.log_display(time.time(), ' 10.logdownload[ld]: download log file of device from server')
        self.log_display(time.time(), '           example: logdownload 0-2 5')
        self.log_display(time.time(), ' 11.alias     [al]: alias names to client ids')
        self.log_display(time.time(), '           example: alias 1234567890123456:Pi1@HZ')
        self.log_display(time.time(), ' 12.quit       [q]: quit this terminal')
        self.log_display(time.time(), ' 13.help       [h]: print help infomation')
        self.log_display(time.time(), ' ')
        self.log_display(time.time(), 'Supported command editing shortcuts:')
        self.log_display(time.time(), ' Ctrl + a - go to the start of the command line')
        self.log_display(time.time(), ' Ctrl + e - go to the end of the command line')
        self.log_display(time.time(), ' Ctrl + k - delete from cursor to the end of the command line')
        self.log_display(time.time(), ' Ctrl + u - delete from cursor to the start of the command line')

    def process_cmd(self, cmd):
        if self.connected == False:
            self.cmdrun_status_display("process command '{0}' failed, connection to server lost".format(cmd))
        cmd_argv = cmd.split(' ')
        self.cmdrun_status_display('')
        cmd = cmd_argv[0]; args = cmd_argv[1:]
        if cmd == 'erase' or cmd == 'er':
            self.erase_devices(args)
        elif cmd == 'program' or cmd == 'pg':
            self.program_devices(args)
        elif cmd == 'reset' or cmd == 'rs':
            self.control_devices('reset', args)
        elif cmd == 'start' or cmd == 'st':
            self.control_devices('start', args)
        elif cmd == 'stop' or cmd == 'sp':
            self.control_devices('stop', args)
        elif cmd == 'log' or cmd == 'lg':
            self.log_on_off(args)
        elif cmd == 'logdownload' or cmd == 'ld':
            self.log_download(args)
        elif cmd == 'runcmd' or cmd == 'rc':
            self.run_command(args, uselast=False)
        elif cmd == 'debug' or cmd == 'db':
            self.run_debug(args)
        elif cmd[0] == '^':
            self.run_command([cmd[1:]] + args, uselast=True)
        elif cmd == 'alias' or cmd == 'al':
            self.client_alias(args)
        elif cmd == 'help' or cmd == 'h':
            self.print_help_info()
        else:
            self.cmdrun_status_display('unknown command:' + cmd)

    def user_interaction(self):
        cmd = ''
        saved_cmd = ''
        history_index = -1
        p = 0
        while self.keep_running:
            c = self.cmd_window.getch()
            if c == ord('\n'):
                if self.log_curr_line != -1:
                    self.log_curr_line = -1
                    self.log_display(time.time(), '')
                if cmd == 'quit' or cmd == 'q' :
                    self.keep_running = False
                    time.sleep(0.2)
                    break
                elif cmd != '':
                    self.process_cmd(cmd)
                    self.cmd_history = [cmd] + self.cmd_history
                cmd = ''
                saved_cmd = ''
                history_index = -1
                p = 0
                self.cmdrun_command_display(cmd, 0)
            elif c == curses.KEY_BACKSPACE or c == 127 or c == 8: #DELETE
                if cmd[0:p] == '':
                    continue
                newcmd = cmd[0:p-1] + cmd[p:]
                cmd = newcmd
                p -= 1
                self.cmdrun_command_display(cmd, p)
            elif c == 259 and len(self.cmd_history) > 0: #KEY_UP
                if history_index == -1:
                    saved_cmd = cmd
                if history_index < (len(self.cmd_history) - 1):
                    history_index += 1
                cmd = self.cmd_history[history_index]
                p = len(cmd)
                self.cmdrun_command_display(cmd, p)
            elif c == 258 and len(self.cmd_history) > 0: #KEY_DOWN
                if history_index <= -1:
                    history_index = -1
                    continue
                history_index -= 1
                if history_index >= 0:
                    cmd = self.cmd_history[history_index]
                else:
                    cmd = saved_cmd
                p = len(cmd)
                self.cmdrun_command_display(cmd, p)
            elif c == 260: #KEY_LEFT
                if p > 0:
                    p -= 1
                    self.cmdrun_command_display(cmd, p)
                continue
            elif c == 261: #KEY_RIGHT
                if p < len(cmd):
                    p += 1
                    self.cmdrun_command_display(cmd, p)
                continue
            elif c == 1: #ctrl-a: go to the start of the command line
                p = 0
                self.cmdrun_command_display(cmd, p)
                continue
            elif c == 3: #ctrl-c: quit
                self.keep_running = False
                time.sleep(0.2)
                break
            elif c == 5: #ctrl-e: go to the end of the command line
                p = len(cmd)
                self.cmdrun_command_display(cmd, p)
                continue
            elif c == 11: #ctrl-k: delete from cursor to the end of the command line
                cmd = cmd[0:p]
                self.cmdrun_command_display(cmd, p)
                continue
            elif c == 21: #ctrl-u: delete from cursor to the start of the command line
                cmd = cmd[p:]
                p = 0
                self.cmdrun_command_display(cmd, p)
                continue
            elif c == curses.KEY_MOUSE:
                mouse_state = curses.getmouse()[4]
                if mouse_state == MOUSE_SCROLL_UP:
                    if self.log_curr_line == -1:
                        self.log_curr_line = len(self.log_content) - 2
                    elif self.log_curr_line > 0:
                        self.log_curr_line -= 1
                    self.log_display(time.time(), '')
                    continue
                elif mouse_state == MOUSE_SCROLL_DOWN:
                    if self.log_curr_line == -1:
                        continue

                    self.log_curr_line += 1
                    if self.log_curr_line >= len(self.log_content):
                        self.log_curr_line = -1
                    self.log_display(time.time(), '')
                    continue
            elif c == curses.KEY_RESIZE:
                try:
                    self.window_redraw()
                    self.device_list_display()
                    self.log_display(time.time(), '')
                    self.cmdrun_command_display(cmd, p);
                except:
                    if DEBUG:
                        raise
                    self.keep_running = False
                    break
            else:
                try:
                    c = str(unichr(c))
                    newcmd = cmd[0:p] + c + cmd[p:]
                    cmd = newcmd
                    p += 1
                except:
                    self.cmdrun_status_display('Error: unsupported unicode character {0}'.format(c))
                    continue
                self.cmdrun_command_display(cmd, p)

    def run(self, controller_ip, controller_port):
        #connect to server
        self.controller_ip = controller_ip
        self.controller_port = controller_port
        thread.start_new_thread(self.packet_send_thread, ())
        thread.start_new_thread(self.server_interaction, ())
        thread.start_new_thread(self.debug_interaction, ())
        while self.keep_running:
            try:
                self.user_interaction()
            except KeyboardInterrupt:
                self.keep_running = False
                time.sleep(0.2)
            except:
                if DEBUG:
                    raise

    def deinit(self):
        curses.nocbreak()
        self.cmd_window.keypad(0)
        curses.echo()
        curses.endwin()
        if self.service_socket:
            self.service_socket.close()
        try:
            if len(self.cmd_history) > 0:
                cmd_history_file = path.join(path.expanduser('~'), '.udterminal', '.cmd_history')
                file = open(cmd_history_file, 'wb')
                json.dump(self.cmd_history, file)
                file.close()
        except:
            self.cmdrun_status_display('error: save command history failed')

    def terminal_func(self, controller_ip, controller_port):
        ret = self.init()
        if ret == 'read access key fail':
            print ''
            return
        if ret == 'success':
            self.run(controller_ip, controller_port)
        if ret == 'UI failed':
            print 'initilize UI window failed, try increase your terminal window size first'
        self.deinit()
