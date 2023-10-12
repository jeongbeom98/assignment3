import socket
import dpkt
import time
import argparse

#JB Lee and Sam Stutzman

from cs3640_ping import make_icmp_socket, send_icmp_echo, recv_icmp_response

def traceroute(destination, n_hops):
    #Do a traceroute to the specified destination wtih a max num of hops.
    for ttl in range(1, n_hops + 1):
        with make_icmp_socket(ttl, 1) as sock:
            send_time = time.time()
            send_icmp_echo(sock, f"traceroute {ttl}".encode(), ttl, ttl, destination)
            
            try:
                data, addr = recv_icmp_response(sock)
                elapsed = (time.time() - send_time) * 1000
                print(f"destination = {destination}; hop {ttl} = {addr[0]}; rtt = {elapsed:.2f} ms")
            except socket.timeout:
                print(f"Request timed out for hop {ttl}")

def main():
    parser = argparse.ArgumentParser(description='Python traceroute')
    parser.add_argument('-destination', action='store', dest='destination', required=True)
    parser.add_argument('-n_hops', action='store', dest='n_hops', type=int, required=True)
    results = parser.parse_args()
    
    destination = results.destination
    n_hops = results.n_hops
    
    traceroute(destination, n_hops)

if __name__ == "__main__":
    main()
