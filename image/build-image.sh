#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

DISK_SIZE='4G'
IMAGE_URL="https://cloud.debian.org/images/cloud/trixie/20261001-2618/debian-13-genericcloud-amd64-20261001-2618.qcow2"

if [ ! -f base.qcow2 ]; then
  echo "Download image"
  wget "$IMAGE_URL" -O base.qcow2
else
  echo "Already downloaded"

fi

