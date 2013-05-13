#!/usr/bin/env python3
from pprint import pprint
from threading import Thread
from queue import Queue, Empty

cfg = {}
for x in range(8):
  hostname = "host%s" % x
  cfg[hostname] = dict(addr=("localhost", 6600+x), id=x)
MINID = 0
MAXID = x
pprint("your config, bro:")
pprint(cfg)

class st:
  up = 1
  down = 2


class Host(Thread):
  addr = None # smth like (addr, port)
  status = None #

  def __init__(self, hostname, cfg):
    self.hostname = hostname
    self.cfg = cfg
    self.status = st.down
    self.queue = Queue()
    super().__init__()

  def do_start(self):
    "normal start"
    self.status = st.up
    raise NotImplementedError

  def do_stop(self):
    "graceful shutdown"
    self.status = st.down
    "flush queue"
    try:
      while True: self.queue.get_nowait()
    except Empty:
      pass
    raise NotImplementedError

  def do_kill(self):
    "suddenly kill node"
    self.status = st.down
    raise NotImplementedError

  def send_msg(self, msg):
    if self.status == st.down:
      return
    self.queue.put_nowait(msg)

  def get_peers(self):
    "here is your super-duper peer selection algo"
    id = self.cfg[self.hostname]['id']
    peers_ids = [id-1, id+1]
    peers = []
    for p_id in peers_ids:
      if p_id < 0:
        p_id = MAXID
      elif p_id > MAXID:
        p_id = 0
      peers += [ cfg["host%s"%p_id] ]
    return peers

  def run(self):
    while True:
      msg = self.queue.get()


def main():
  raise NotImplementedError


if __name__ == '__main__':
  main()
