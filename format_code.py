#!/bin/bash

set -x

sudo yapf -i ./harborclient/*.py
sudo yapf -i ./examples/*.py
