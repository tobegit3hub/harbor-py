## Introduction

[harbor](https://github.com/vmware/harbor) is the enterprise-class registry server for docker distribution.

[harbor-py](https://github.com/tobegit3hub/harbor-py) is the native and compatible python SDK for harbor. The supported APIs are list below.

- [x] Projects APIs
  - [x] [Get projects](./examples/get_projects.py)
  - [x] [Create project](./examples/create_project.py)
  - [x] [Check project exist](./examples/check_project_exist.py)
- [x] Users APIs
  - [x] [Get users](./examples/get_users.py)
  - [x] [Create user](./examples/create_user.py)
  - [x] [Update user profile](./examples/update_user_profile.py)
  - [x] [Delete user](./examples/delete_user.py)
  - [x] [Change password](./examples/change_password.py)
  - [x] [Promote as admin](./examples/promote_as_admin.py)
- [ ] Repositories APIs
  - [x] [Get repositories](./examples/get_repositories.py)
  - [ ] Create repository
  - [ ] Delete repository
  - [x] [Get repository tags](./examples/get_repository_tags.py)
  - [x] [Get repository manifests](./examples/get_repository_manifests.py)
- [x] Others APIs
  - [x] [Search](./examples/search.py)
  - [x] [Get statistics](./examples/get_statistics.py)
  - [x] [Get top accessed repositories](./examples/get_top_accessed_repositories.py)
  - [x] [Get logs](./examples/get_logs.py)

## Installation

```
pip install -U harbor-py
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

## Contribution

If you have any suggestion, feel free to submit [issues](https://github.com/tobegit3hub/harbor-py/issues) or send [pull-requests](https://github.com/tobegit3hub/harbor-py/pulls) for `harbor-py`.

The `harbor` APIs may change occasionally, checkout the complete API list [here](https://github.com/vmware/harbor/blob/master/docs/configure_swagger.md).

Publish `harbor-py` package to [pypi](https://pypi.python.org/pypi/harbor-py/) server with the following commands.

```
python setup.py register -r pypi
python setup.py sdist upload  -r pypi
```
