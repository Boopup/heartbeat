import os, time, re, requests, signal, sys

url = os.getenv("HEARTBEAT_URL").rstrip("/")
interval = os.getenv("INTERVAL", "5m")

m = re.fullmatch(r"(\d+)([smh])", interval)
v = int(m.group(1))
u = m.group(2)

sec = v * (1 if u == "s" else 60 if u == "m" else 3600)

fail = False

def send(f=False):
    try:
        requests.get(url + ("/fail" if f else ""), timeout=10)
    except:
        pass

def stop(*_):
    send(True)
    sys.exit(0)

signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

while True:
    send(fail)
    time.sleep(sec)
