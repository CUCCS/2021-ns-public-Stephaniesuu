from scapy.all import *
def udp_scan(ip, port, timeout=3):
	pkt = IP(dst=ip)/UDP(dport=port)
	res = sr1(pkt, timeout=timeout, verbose=False)
	if res is None:
		print("Open|Filtered")
	elif res.haslayer(UDP):
		print('open')
	elif res.haslayer(ICMP):
		if res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code == 3:
			print('closed')
		elif res.getlayer(ICMP).type == 3 and res.getlayer(ICMP).code in [1, 2, 9, 10, 13]:
			priint('filtered')
		elif resp.haslayer(IP) and res.getlayer(IP).proto == IP_PROTOS.udp:
			print("Open")
				
if __name__ == '__main__':
    udp_scan('172.16.111.111', 53)