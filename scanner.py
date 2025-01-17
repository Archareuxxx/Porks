import socket
import threading
from queue import Queue
from signature import create_signature
queue = Queue()
results = []
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            results.append(f"Port {port} [OPEN]")
        sock.close()
    except Exception as e:
        results.append(f"Port {port} [ERROR]: {e}")
def worker(ip):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()
def main():
    print(create_signature("PORT SCANNER"))
    ip = input("Enter target IP: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    thread_count = int(input("Enter number of threads: "))
    for port in range(start_port, end_port + 1):
        queue.put(port)
    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(ip,))
        threads.append(t)
        t.start()
    queue.join()
    print("\nScan Results:")
    for result in results:
        print(result)
    save = input("\nDo you want to save the results? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter filename to save results: ")
        with open(filename, "w") as f:
            f.write("\n".join(results))
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    main()
  
