#!/usr/bin/env python

import sys
sys.path.append("../harborclient/")

import harborclient

host = "10.69.1.246"
user = "admin"
password = "Harbor12345"

client = harborclient.HarborClient(host, user, password)
