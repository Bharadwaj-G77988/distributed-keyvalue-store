from fastapi import FastAPI
import socket

app = FastAPI()

HOST = "127.0.0.1"
PORT = 5000

def send_command(cmd):
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send((cmd + "\n").encode())
    data = s.recv(1024).decode().strip()
    s.close()
    return data

@app.get("/")
def home():
    return {"message": "KeyValueStore API Running"}

@app.post("/set")
def set_value(key:str,value:str,ttl:int=None):
    cmd=f"SET {key} {value}"
    if ttl:
        cmd+=f" {ttl}"
    return {"response":send_command(cmd)}

@app.get("/get")
def get_value(key:str):
    return {"value":send_command(f"GET {key}")}

@app.post("/submit")
def submit(task:str):
    return {"job_id":send_command(f"SUBMIT {task}")}

@app.get("/status")
def status(job_id:str):
    return {"status":send_command(f"STATUS {job_id}")}
