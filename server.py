import socket
import threading
import json
import time
import logging
import queue

store = {}
expiry = {}
jobs = {}
job_queue = queue.Queue()

file_name = "data.json"

logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def save():
    with open(file_name, "w") as f:
        json.dump({"store": store, "expiry": expiry}, f)

def load():
    global store, expiry
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
            store = data.get("store", {})
            expiry = data.get("expiry", {})
    except:
        store = {}
        expiry = {}

def cleanup():
    while True:
        now = time.time()
        expired = [k for k,v in expiry.items() if v < now]
        for k in expired:
            store.pop(k,None)
            expiry.pop(k,None)
        time.sleep(2)

def worker():
    while True:
        job_id, payload = job_queue.get()
        try:
            time.sleep(3)
            jobs[job_id]["status"] = "completed"
        except:
            jobs[job_id]["status"] = "failed"
        job_queue.task_done()

def handle(conn):
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        parts = data.split()
        cmd = parts[0].upper()

        if cmd == "SET" and len(parts) >= 3:
            key = parts[1]
            value = parts[2]
            ttl = int(parts[3]) if len(parts) == 4 else None

            store[key] = value

            if ttl:
                expiry[key] = time.time() + ttl
            else:
                expiry.pop(key,None)

            save()
            conn.send(b"OK\n")

        elif cmd == "GET" and len(parts) >= 2:
            key = parts[1]

            if key in expiry and expiry[key] < time.time():
                store.pop(key,None)
                expiry.pop(key,None)
                save()
                conn.send(b"NULL\n")
            else:
                val = store.get(key,"NULL")
                conn.send((str(val)+"\n").encode())

        elif cmd == "DELETE" and len(parts) >= 2:
            key = parts[1]
            store.pop(key,None)
            expiry.pop(key,None)
            save()
            conn.send(b"DELETED\n")

        elif cmd == "SUBMIT":
            payload = parts[1:] if len(parts)>1 else []
            job_id = str(time.time())

            jobs[job_id] = {
                "status":"queued",
                "payload":payload
            }

            job_queue.put((job_id,payload))
            conn.send((job_id+"\n").encode())

        elif cmd == "STATUS" and len(parts) >= 2:
            job_id = parts[1]
            status = jobs.get(job_id,{}).get("status","NOT_FOUND")
            conn.send((status+"\n").encode())

        else:
            conn.send(b"ERROR\n")

    conn.close()

load()

threading.Thread(target=cleanup,daemon=True).start()

for _ in range(3):
    threading.Thread(target=worker,daemon=True).start()

s = socket.socket()
s.bind(("0.0.0.0",5000))
s.listen()

print("Server running on port 5000")

while True:
    conn,addr = s.accept()
    threading.Thread(target=handle,args=(conn,)).start()
