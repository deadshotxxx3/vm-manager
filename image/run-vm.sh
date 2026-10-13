#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Объявление переменных
DISK_NAME="disk.qcow2"
SEED_ISO="seed.iso"
RAM_MB="1024"
CPU_CORES="2"
SSH_PORT="2222"

# Запуск VM
qemu-system-x86_64 \
  -machine q35,accel=kvm:tcg \
  -m "$RAM_MB" -smp "$CPU_CORES" \
  -drive "file=$DISK_NAME,if=virtio,format=qcow2" \
  -drive "file=$SEED_ISO,if=virtio,format=raw" \
  -netdev "user,id=net0,hostfwd=tcp::$SSH_PORT-:22" \
  -device virtio-net-pci,netdev=net0