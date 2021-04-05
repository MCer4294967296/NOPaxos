#!/bin/bash
sudo apt update && sudo apt install -y protobuf-compiler pkg-config libunwind-dev libssl-dev libprotobuf-dev libevent-dev libgtest-dev
make
mkdir logoutput