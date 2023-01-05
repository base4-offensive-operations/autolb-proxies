# c0ded by jctommasi - 2022 - base4sec offensive operations
import requests
import random
import time
import json
import urllib3
import threading
import subprocess
from argparse import ArgumentParser
from termcolor import colored
from threading import Thread


'''
MISC
'''

#disable warnings for certificate issues in requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#logic for conditional args: type=str2bool
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean Value Expected')

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

'''
BANNER FUNCS
'''

def pprint(string,color):
    print(colored(string, color, attrs=["bold"]))


'''
PROGRAM LOGIC
'''

def get_proxys_count(proxytype):
    try:
        url = "https://proxylist.geonode.com:443/api/proxy-list?limit=1&page=1&sort_by=lastChecked&sort_type=desc&protocols={}".format(proxytype)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; x64; rv:105.0esr) Gecko/20010101 Firefox/105.0esr", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = json.loads(r.text)
            return data["total"]
    except Exception as e:
        print("Error getting proxy count: {}".format(e))
        exit()

def check_proxy(proxyline,webtest):
    aux = proxyline.split(" ")
    proxytype = aux[0]
    ip = aux[1]
    port = aux[2]
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; x64; rv:105.0esr) Gecko/20010101 Firefox/105.0esr", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Te": "trailers", "Connection": "close"}
        # pprint('[*] Checking {}:{}'.format(ip,port), "cyan")
        pxy = '{}://{}:{}'.format(proxytype,ip,port)
        r = requests.get(webtest, headers=headers,proxies={"http":pxy,"https":pxy}, timeout=10,allow_redirects=True)
        if r.status_code == 200:
            pprint("[!] Proxy {}:{} it's alive (̿▀̿ ̿Ĺ̯̿̿▀̿ ̿)̄".format(ip,port), "green")
            #pprint("[*] Response: {}".format(r.text),"blue")
            return proxyline
    except Exception:
        pass
        # pprint("[!] Proxy {}:{} is down ..".format(ip,port), "red")

def parse_proxy_response(r,proxytype,latency):
    db = []
    data = json.loads(r)
    proxies = data["data"]
    for proxy in proxies:
        if proxy["latency"] < latency:
            ip = proxy["ip"]
            port = proxy["port"]
            string_pxy = "{} {} {}".format(proxytype,ip,port)
            db.append(string_pxy)
    return db

def get_proxy_list(proxytype,latency):
    proxy_list = []
    pprint("[*] Total proxies fetched: {}".format(get_proxys_count(proxytype)),"blue")
    total = get_proxys_count(proxytype)
    totalaux = total
    max = int(total/500)+1
    for proxypage in range(1,max+1):
        try:
            if 500 < total:
                pprint("[*] Parsing 500 proxies of page {}/{}".format(proxypage,max),"yellow")
            else:
                pprint("[*] Parsing {} proxies of page {}/{}".format(totalaux-500*(proxypage-1),proxypage,max),"yellow")
            url = "https://proxylist.geonode.com:443/api/proxy-list?limit=500&page={}&sort_by=lastChecked&sort_type=desc&protocols={}".format(proxypage,proxytype)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; x64; rv:105.0esr) Gecko/20010101 Firefox/105.0esr", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close"}
            r = requests.get(url, headers=headers)
            db = parse_proxy_response(r.text,proxytype,latency)
            for proxy in db:
                proxy_list.append(proxy)
            total = total-500
        except Exception as e:
            pprint("[!] Couldn't fetch proxy lists .. ERR: {}".format(e),"red")
            exit()
    return proxy_list

def do_multi_thread_check(proxies,webtest):
    good_ones = []
    while len(proxies) > 0:
        try:
            time.sleep(1)
            # creating threads
            t1 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t2 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t3 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t4 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t5 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t6 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t7 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t8 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t9 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t10 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t11 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))
            t12 = ThreadWithReturnValue(target=check_proxy, args=(proxies.pop(0),webtest,))

            # starting threads
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t5.start()
            t6.start()
            t7.start()
            t8.start()
            t9.start()
            t10.start()
            t11.start()
            t12.start()

            # wait until thread 1 is completely executed
            threads = [t1.join(),t2.join(),t3.join(),t4.join(),t5.join(),t6.join(),t7.join(),t8.join(),t9.join(),t10.join(),t11.join(),t12.join()]
            for result in threads:
                if result != None:
                    good_ones.append(result)
        except KeyboardInterrupt:
            exit()
        except:
            pass
    return good_ones

def print_proxy_chains_file(good_ones,chainlen):
    file = '''round_robin_chain
chain_len = {}
quiet_mode
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]'''.format(chainlen)
    print(file)
    for proxy in good_ones:
        print(proxy)
    return file

def loadbalance_proxies(good_ones):
    cmd = "./loadbalancer -lhost 10.0.3.15 -tunnel"
    for proxy in good_ones:
        aux = proxy.split(" ")
        host = aux[1]
        ip = aux[2]
        cmd += " {}:{}@1".format(host,ip)
    pprint("\n[!] Starting Load Balancer ..","yellow")
    pprint("[*] Executing command: \n{}".format(cmd),"blue")
    subprocess.run(cmd.split(" "),capture_output=False)

def main():
    parser = ArgumentParser(description='description')
    parser.add_argument('-c', '--chainlength', type=int, default=1, required=False, metavar='', help='how many proxyies to chain, default 1 for rotative proxy')
    parser.add_argument('-w', '--webtest', type=str, required=True, metavar='', help='web to test the proxyes, can be your vps to check proxies connections')
    parser.add_argument('-l', '--latency', type=int, default=100, required=False, metavar='', help='max proxy latency to fetch')
    parser.add_argument('-t', '--type', type=str, required=True, metavar='', help='types supported: http / https / socks4 / socks5')
    parser.add_argument('--proxychains', type=str2bool, required=False, nargs='?', const=True, default=False, help='Generate and print proxychains file')
    parser.add_argument('--lbproxies', type=str2bool, required=False, nargs='?', const=True, default=False, help='Create a load balancer with good proxies')
    parser.add_argument('--onlyip', type=str2bool, required=False, nargs='?', const=True, default=False, help='Print only IP addresses')
    args = parser.parse_args()

    if args.type in "http https socks4 socks5":
        if args.lbproxies and args.type != "socks5":
            pprint("[*] Load balancer is incompatible with {}, please use socks5 proxies ..".format(args.type))
            exit()

        proxies = get_proxy_list(args.type,args.latency)
        proxies_len = len(proxies)

        pprint("\n[*] {} Total proxies with latency less than {} ms".format(proxies_len,args.latency),"blue")
        pprint("[!] Start testing {} proxies, this may take a while ..\n".format(proxies_len),"yellow")

        good_ones = do_multi_thread_check(proxies,args.webtest)
        pprint("\n[*] Tasks finished, total {} good proxies of {}".format(len(good_ones),proxies_len),"blue")
        if args.proxychains:
            pprint("[!] Printing /etc/proxychains4.conf file\n","yellow")
            print_proxy_chains_file(good_ones,args.chainlength)
        if args.lbproxies and args.type == "socks5":
            loadbalance_proxies(good_ones)
        if args.proxychains != True and args.lbproxies != True:
            for proxy in good_ones:
                aux = proxy.split(" ")
                proto = aux[0]
                host = aux[1]
                ip = aux[2]
                if args.onlyip:
                    print("{}:{}".format(host,ip))
                else:
                    print("{}://{}:{}".format(proto,host,ip))

    else:
        pprint("[!] Proxy type not supported", "red")

if __name__ == '__main__':
    main()
