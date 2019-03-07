from harborclient_light import harborclient

host = "127.0.0.1"
user = "admin"
password = "Harbor12345"

client = harborclient.HarborClient(host, user, password)

client.retag_repository_image('project/repo', 'project/repo:tag', 'new_tag')
