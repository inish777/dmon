#!/usr/bin/env python3
from pprint import pprint

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


class Host:
  addr = None # smth like (addr, port)
  status = None #

  def __init__(self, hostname, cfg):
    self.hostname = hostname
    self.cfg = cfg
    self.status = st.down

  def start(self):
    "normal start"
    self.status = st.up
    raise NotImplementedError

  def stop(self):
    "graceful shutdown"
    self.status = st.down
    raise NotImplementedError

  def kill(self):
    "suddenly kill node"
    self.status = st.down
    raise NotImplementedError

  def get_peers(self):
    "here is your super-duper algo"
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


def main():
  raise NotImplementedError


if __name__ == '__main__':
  main()
