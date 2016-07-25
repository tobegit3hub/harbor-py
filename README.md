# harbor-py

## Introduction

[harbor](https://github.com/vmware/harbor) is the enterprise-class registry server for docker distributions. It's written in golang and you can use it with the Web UI.

[harbor-py](https://github.com/tobegit3hub/harbor-py) provides the native and compatible python SDK for harbor. The supported APIs are list below.

- [ ] Projects APIs
  - [x] [Get projects](./examples/get_projects.py)
  - [ ] Create project
- [ ] Users APIs
  - [ ] Create user
- [ ] Repositories APIs
  - [ ] Create repository
- [ ] Others APIs
  - [x] [Search](./examples/search.py)

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
print(client.search("library"))
```

## Contribution

If you have any suggestion for this project, feel free to subbmit [issues](https://github.com/tobegit3hub/harbor-py/issues) or send [pull-requests](https://github.com/tobegit3hub/harbor-py/pulls) to `harbor-py`.

The `harbor` APIs may change, checkout the complete API list [here](https://github.com/vmware/harbor/blob/master/docs/configure_swagger.md).
