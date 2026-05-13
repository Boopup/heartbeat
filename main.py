import os, time, re, signal, sys
from urllib.request import urlopen, Request

url = os.getenv("HEARTBEAT_URL").rstrip("/")
interval = os.getenv("INTERVAL", "5m")

m = re.fullmatch(r"(\d+)([smh])", interval)
v = int(m.group(1))
u = m.group(2)

sec = v * (1 if u == "s" else 60 if u == "m" else 3600)

fail = False

def send(f=False):
    try:
        req = Request(url + ("/fail" if f else ""))
        urlopen(req, timeout=10).read()
        print("sent:", "fail" if f else "ok")
    except:
        print("send failed")

def stop(*_):
    send(True)
    sys.exit(0)

signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

print("heartbeat started")
print("interval:", interval)

while True:
    send(fail)
    time.sleep(sec)
