#!/usr/bin/env python

import sys
sys.path.append("../harborclient/")

import harborclient

host = "127.0.0.1"
user = "admin"
password = "Harbor12345"

client = harborclient.HarborClient(host, user, password)

# Get all projects
print(client.get_projects())

# Get projects with project_name
print("TODO")

# Get project iwth is_public
print("TODO")
