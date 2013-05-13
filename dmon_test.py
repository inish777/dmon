#!/usr/bin/env python3

from libdmon import Host, cfg

hosts = {}
for hostname, params in cfg.items():
  hosts[hostname] = Host(hostname=hostname, cfg=cfg)

def test_peerselection():
  host = hosts["host1"]
  print(host.get_peers())
