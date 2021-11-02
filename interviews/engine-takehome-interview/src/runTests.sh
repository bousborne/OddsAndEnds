#!/bin/bash
pushd /app
make tests
popd
/app/build/match_engine_tests -s
