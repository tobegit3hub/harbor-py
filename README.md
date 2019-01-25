# [Harbor](https://github.com/goharbor/harbor) client light.

## Introduction

[Harbor](https://github.com/goharbor/harbor) is the enterprise-class registry server for docker distribution.

[harbor-py-light](https://github.com/fedor-chemashkin/harbor-py-light) is lightweight Harbor client. The supported APIs are list below.

- [x] Projects APIs
  - [x] [Get projects](./examples/get_projects.py)
  - [x] [Create project](./examples/create_project.py)
  - [x] [Check project exist](./examples/check_project_exist.py)
  - [x] [Get project id from name](./examples/get_project_id_from_name.py)
  - [ ] [Set project publicity](./examples/set_project_publicity.py)
  - [ ] Get project access logs
  - [ ] Get project member
  - [ ] Get project and user member
- [x] Repositories APIs
  - [x] [Get repositories](./examples/get_repositories.py)
  - [x] [Delete repository](./examples/delete_repository.py)
  - [x] [Get repository tags](./examples/get_repository_tags.py)
  - [x] [Get repository manifests](./examples/get_repository_manifests.py)
- [x] Others APIs
  - [x] [Search](./examples/search.py)
  - [x] [Get statistics](./examples/get_statistics.py)
  - [x] [Get top accessed repositories](./examples/get_top_accessed_repositories.py)
  - [x] [Get logs](./examples/get_logs.py)
  - [x] Get systeminfo
  - [x] Get systeminfo volumes
  - [x] Get configurations

## Installation

```
pip install harbor-py-light
```

## Usage

```
from harborclient import harborclient

host = "127.0.0.1"
user = "admin"
password = "Harbor12345"

client = harborclient.HarborClient(host, user, password)

client.get_projects()
client.get_users()
client.get_statistics()
client.get_top_accessed_repositories()
client.search("library")
```

For more usage, please refer to the [examples](./examples/).


