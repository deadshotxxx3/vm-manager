#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Объявления переменных

# Переменные для скачивания образа
IMAGE_URL="https://cloud.debian.org/images/cloud/trixie/20261001-2618/debian-13-genericcloud-amd64-20261001-2618.qcow2"
BASE_IMAGE="base.qcow2"

# Переменные для создания ключа
KEY_DIR="keys"
KEY_FILE="$KEY_DIR/ssh_key"

# Переменные для cloud-init
CLOUD_INIT_DIR="cloud-init"
USER_DATA_TEMPLATE="$CLOUD_INIT_DIR/user-data.template"
USER_DATA="$CLOUD_INIT_DIR/user-data"
META_DATA="$CLOUD_INIT_DIR/meta-data"

# Переменные для создания seed.iso
SEED_ISO="seed.iso"

# Переменные для создание диска
DISK_NAME="disk.qcow2"
DISK_SIZE="4G"

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

# Генерация user-data
echo "Generating user-data"
PUB_KEY="$(cat "$KEY_FILE.pub")"
sed "s|__SSH_PUBLIC_KEY__|$PUB_KEY|" "$USER_DATA_TEMPLATE" > "$USER_DATA"

# Создание iso
echo "Generating seed.iso"
cloud-localds "$SEED_ISO" "$USER_DATA" "$META_DATA"

# Создания диска
if [ ! -f "$DISK_NAME" ]; then
  echo "Creating disk"
  qemu-img create -f qcow2 -F qcow2 -b "$BASE_IMAGE" "$DISK_NAME" "$DISK_SIZE"
else
  echo "Disk already create"
fi

echo "Done. run run-vm.sh"
