#!/bin/bash

java $(jq -r '.jar | "\(.options) -jar \(.jarFilePath) \(.args)"' config.json) &
python $(jq -r '.py | "\(.pyFilePath) \(.args)"' config.json) &