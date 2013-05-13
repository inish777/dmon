#!/usr/bin/env python3

from libdmon import Host, cfg, hosts

for hostname, params in cfg.items():
  Host(hostname=hostname, cfg=cfg)

def test_peerselection():
  host = hosts["host1"]
  host.start()
  host.join()


if __name__ == '__main__':
  test_peerselection()
