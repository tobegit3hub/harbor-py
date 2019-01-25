#!/usr/bin/env python

import sys
sys.path.append("../")

from harborclient_light import harborclient

host = "127.0.0.1"
user = "admin"
password = "Harbor12345"

client = harborclient.HarborClient(host, user, password)

# Check if project exists
project_name = "test-project"
print(client.check_project_exist(project_name))
