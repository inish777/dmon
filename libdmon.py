#!/usr/bin/env python3
from pprint import pprint

cfg = {}
for x in range(10):
  hostname = "host%s" % x
  cfg[hostname] = dict(addr=("localhost", 6600+x))
pprint("your config, bro:")
pprint(cfg)


class Host:
  addr = None # smth like (addr, port)
  status = None #

  def start(self):
    "normal start"
    raise NotImplementedError

  def stop(self):
    "graceful shutdown"
    raise NotImplementedError

  def kill(self):
    "suddenly kill node"
    raise NotImplementedError

  def get_peers(self):
    raise NotImplementedError


def main():
  raise NotImplementedError


if __name__ == '__main__':
  main()
