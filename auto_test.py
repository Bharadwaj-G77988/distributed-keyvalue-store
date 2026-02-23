import socket,time

def send(cmd):
    s.send((cmd+"\n").encode())
    return s.recv(1024).decode().strip()

s=socket.socket()
s.connect(("127.0.0.1",5000))

print("TEST STARTED\n")

print("1?? SET name")
print(send("SET name Bharadwaj"))

print("2?? GET name")
print(send("GET name"))

print("3?? SET city with TTL=5")
print(send("SET city Hyderabad 5"))

print("4?? GET city")
print(send("GET city"))

print("Waiting 6 seconds for TTL expire...")
time.sleep(6)

print("5?? GET city after expiry")
print(send("GET city"))

print("6?? SUBMIT job")
jobid = send("SUBMIT task1")
print("JobID:",jobid)

print("7?? STATUS immediately")
print(send(f"STATUS {jobid}"))

time.sleep(4)

print("8?? STATUS after processing")
print(send(f"STATUS {jobid}"))

print("\n? ALL TESTS COMPLETED")

s.close()
