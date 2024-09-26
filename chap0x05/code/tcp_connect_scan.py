from scapy.all import *

def Tcp_connect_scan(target_ip, target_port, timeout=5):
	pkt = IP(dst=target_ip)/TCP(dport=target_port, flags='S')
	res = sr1(pkt, timeout=timeout, verbose=False)
	if res is None:
		print("Filtered")
	elif res.haslayer(TCP):
		if res.getlayer(TCP).flags == 'AS':
			res1 = sr1(IP(dst=target_ip)/TCP(dport=target_port, flags='A'), timeout=timeout, verbose=False)
			print("Open")
		elif res.getlayer(TCP).flags == 'AR':
			print("Closed")
        
if __name__ == '__main__':
    Tcp_connect_scan('172.16.111.111', 80)