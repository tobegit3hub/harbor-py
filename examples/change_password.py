#!/usr/bin/env python
from harborclient_light import harborclient
import sys
sys.path.append("../")

host = "127.0.0.1"
user = "admin"
password = "Harbor12345"

client = harborclient.HarborClient(host, user, password)

# Change password
user_id = 2
old_password = "test-password"
new_password = "new-password"
client.change_password(user_id, old_password, new_password)
