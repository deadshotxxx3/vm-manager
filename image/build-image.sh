#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Объявления переменных
IMAGE_URL="https://cloud.debian.org/images/cloud/trixie/20261001-2618/debian-13-genericcloud-amd64-20261001-2618.qcow2"
BASE_IMAGE="base.qcow2"
DISK_SIZE="4G"

KEY_DIR="keys"
KEY_FILE="$KEY_DIR/ssh_key"

# Скачивание образа
if [ ! -f "$BASE_IMAGE" ]; then
  echo "Downloading image"
  wget "$IMAGE_URL" -O "$BASE_IMAGE"
else
  echo "Image already downloaded"
fi

# Создание ssh ключа
if [ ! -f "$KEY_FILE" ]; then
  echo "Creating SSH key"
  mkdir -p "$KEY_DIR"
  ssh-keygen -t ed25519 -N "" -f "$KEY_FILE"
else
  echo "SSH key already exists"
fi