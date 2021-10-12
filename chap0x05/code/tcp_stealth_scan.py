from scapy.all import *

def tcp_stealth_scan(ip, port, timeout=3):
	pkt = IP(dst=ip)/TCP(dport=port, flags='S')
	res = sr1(pkt, timeout=timeout, verbose=False)
	if res is None:
		print("Filtered")
	elif res.haslayer(TCP):
		if res.getlayer(TCP).flags == 'AS':
			res1 = sr1(IP(dst=ip)/TCP(dport=port, flags='R'), timeout=timeout, verbose=False)
			print("Open")
		elif res.getlayer(TCP).flags == 'AR':
			print("Close")
		elif res.haslayer(ICMP) and res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]:
			print("Filtered")

if __name__ == '__main__':
    tcp_stealth_scan('172.16.111.111', 80)