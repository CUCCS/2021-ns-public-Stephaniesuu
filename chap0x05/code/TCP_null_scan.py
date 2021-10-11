from scapy.all import *

def tcp_null_scan(ip, port, timeout=3):
	pkt = IP(dst=ip)/TCP(dport=port, flags='')
	res = sr1(pkt, timeout=timeout, verbose=False)
	if res is None:
		print('open|filtered')
	elif res.haslayer(TCP):
		if res.getlayer(TCP).flags == 'AR':
			print('closed')
	elif res.haslayer(ICMP):
		if res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]:
			print('filtered')

if __name__ == '__main__':
    tcp_null_scan('172.16.111.111', 80)