#!/usr/bin/env python
import salt.client

def main():
    caller = salt.client.Caller()
    return caller.sminion.functions['mine.get']('*', "network.ip_addrs")

if __name__ == "__main__":
  serverList = main()
  print serverList
