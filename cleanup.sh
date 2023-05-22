#!/bin/bash

podman kill $(podman ps -q)
podman container prune
podman rmi -f $(podman images -q)
podman volume prune
podman network prune
