import socket
import dpkt
import time
import argparse

#JB Lee and Sam Stutzman

def make_icmp_socket(ttl, timeout):
    """Creates and returns a raw socket with a specific TTL and timeout for ICMP protocol."""
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    s.settimeout(timeout)
    return s

def send_icmp_echo(sock, payload, id, seq, destination):
    """Sends an ICMP echo message using provided socket and details."""
    icmp = dpkt.icmp.ICMP.Echo(id=id, seq=seq, data=payload)
    packet = dpkt.icmp.ICMP(type=8, data=icmp)
    sock.sendto(bytes(packet), (destination, 1))

def recv_icmp_response(sock):
    """Waits and receives ICMP response. Returns received data and address."""
    data, addr = sock.recvfrom(1024)
    return data, addr

def main():
    """Main function to parse command line arguments, send ICMP echo requests and print results."""
    parser = argparse.ArgumentParser(description='Python ping')
    parser.add_argument('-destination', action='store', dest='destination', required=True)
    parser.add_argument('-n', action='store', dest='n', type=int, required=True)
    parser.add_argument('-ttl', action='store', dest='ttl', type=int, required=True)
    results = parser.parse_args()

    destination = results.destination
    n = results.n
    ttl = results.ttl
    
    total_rtt = 0
    successful_pings = 0
    
    for i in range(n):
        with make_icmp_socket(ttl, 1) as sock:
            send_time = time.time()
            send_icmp_echo(sock, b'Ping', i, i, destination)
            try:
                data, addr = recv_icmp_response(sock)
                elapsed = (time.time() - send_time) * 1000
                total_rtt += elapsed
                successful_pings += 1
                print(f"destination = {destination}; icmp_seq = {i}; icmp_id = {i}; ttl = {ttl}; rtt = {elapsed:.2f} ms")
            except socket.timeout:
                print(f"Request timed out for icmp_seq {i}")

    if successful_pings > 0:
        average_rtt = total_rtt / successful_pings
        print(f"Average rtt: {average_rtt:.2f} ms; {successful_pings}/{n} successful pings.")
    else:
        print("No successful pings.")

if __name__ == "__main__":
    main()
