#!/usr/bin/env python3
from queue import Queue, Empty
from threading import Thread
from pprint import pprint
import logging
import time


#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

cfg = {}
for x in range(8):
  hostname = "host%s" % x
  cfg[hostname] = dict(addr=("localhost", 6600+x), id=x)
MINID = 0
MAXID = x
print("your config, bro:")
pprint(cfg)

class st:
  up = 1
  down = 2


hosts = {}
class Host(Thread):
  addr     = None       # smth like (addr, port)
  status   = st.down    # is host up?
  interval = 1          # peers poke interval
  timeout  = 10         # host ping timeout

  def __init__(self, hostname, cfg):
    self.hostname = hostname
    self.cfg = cfg
    self.status = st.down
    self.queue = Queue()
    self.log = logging.getLogger(hostname)
    self.log.setLevel(logging.DEBUG)
    self.last_seen = {}  # when did we see our peers last time?
    super().__init__(daemon=True)
    hosts[hostname] = self

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
      peers += [ hosts["host%s"%p_id] ]
    assert self not in peers, "TODO: why I'm monitoring myself??"  # check that in small nets nodes do not monitor theirselves
    return peers

  def notify_peers(self):
    peers = self.get_peers()
    self.log.debug("it's time to poke our peers %s!" % peers)
    for peer in peers:
      self.log.debug("tackling %s" % peer)
      peer.send_msg(self.hostname)
      if peer not in self.last_seen:
        self.last_seen[peer.hostname] = None
    now = time.time()
    #TODO: here we can process peers and send notifications
    #  naive example:
    for peer, last_seen in self.last_seen.items():
      self.log.debug("checking peer %s that was last seen %s" % (peer, last_seen))
      if not last_seen or now - last_seen > self.timeout:
        self.log.critical("host is unreachable")

  def run(self):
    next_check = self.interval
    while True:
      delta = -time.time()
      try:
        self.log.debug("waiting for a message for %ss" % next_check)
        msg = self.queue.get(timeout=next_check)
        self.last_seen[msg] = time.time()
      except Empty:
        pass
      delta += time.time()
      next_check -= delta
      if next_check < 0:
        next_check = self.interval
        self.notify_peers()


def main():
  raise NotImplementedError


if __name__ == '__main__':
  main()
