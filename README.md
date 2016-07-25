## Introduction

[harbor](https://github.com/vmware/harbor) is the enterprise-class registry server for docker distributions.

[harbor-py](https://github.com/tobegit3hub/harbor-py) is the native and compatible python SDK for harbor. The supported APIs are list below.

- [ ] Projects APIs
  - [x] [Get projects](./examples/get_projects.py)
  - [x] [Check project exist](./examples/check_project_exist.py)
  - [ ] Create project
- [ ] Users APIs
  - [x] Get users
  - [ ] [Create user](./examples/get_users.py)
  - [x] [Delete user](./examples/delete_user.py)
  - [ ] Change password
  - [x] [Promote as admin](./examples/promote_as_admin.py)
- [ ] Repositories APIs
  - [x] [Get repositories](./examples/get_repositories.py)
  - [ ] Create repository
  - [ ] Delete repository
  - [x] [Get repository tags](./examples/get_repository_tags.py)
- [ ] Others APIs
  - [x] [Search](./examples/search.py)
  - [x] [Get statistics](./examples/get_statistics.py)

## Installation

```
git clone https://github.com/tobegit3hub/harbor-py
python ./setup.py install
```

## Usage

```
import harborclient

host = "127.0.0.1"
user = "admin"
password = "Harbor12345"

client = harborclient.HarborClient(host, user, password)

client.search("library")
client.get_projects()
client.check_project_exist("test-project")
```

For more usage, please refer to the [examples](./examples/).

## Contribution

If you have any suggestion for this project, feel free to subbmit [issues](https://github.com/tobegit3hub/harbor-py/issues) or send [pull-requests](https://github.com/tobegit3hub/harbor-py/pulls) to `harbor-py`.

The `harbor` APIs may change, checkout the complete API list [here](https://github.com/vmware/harbor/blob/master/docs/configure_swagger.md).
