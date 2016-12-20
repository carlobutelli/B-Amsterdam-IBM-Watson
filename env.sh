#!/usr/bin/env bash

export VCAP_SERVICES=$(cat local-env.json)
source .venv/bin/activate
