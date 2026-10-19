# VM Manager

Веб-приложение для управления виртуальной машиной Debian 13 через QEMU и QMP.

Что умеет:
- включить, перезагрузить и остановить ВМ;
- показать статус ВМ;
- открыть терминал ВМ в браузере через serial-консоль или SSH.

## Структура

```
vm-manager/
├── image/               # скрипт сборки образа ВМ
├── backend/             # Python, FastAPI, QMP
├── frontend/            # React, xterm.js, nginx
└── docker-compose.yml
```

## Требования

- Linux с поддержкой KVM (должен быть `/dev/kvm`)
- Docker и Docker Compose
- Для сборки образа: `wget`, `qemu-utils`, `cloud-image-utils`, `openssh-client`

## Запуск

1. Склонировать репозиторий:

```bash
git clone https://github.com/deadshotxxx3/vm-manager.git
cd vm-manager
```

2. Собрать образ ВМ:

```bash
./image/build-image.sh
```

Скрипт скачивает Debian 13, создаёт SSH-ключ в `image/keys/` и готовит диск и настройки cloud-init в `image/cloud-init/`.

3. Запустить проект:

```bash
docker compose up --build
```

4. Открыть в браузере http://localhost

Остановить проект: `docker compose down`

## Использование

- **Включить** запускает ВМ.
- **Перезагрузить** перезагружает ВМ.
- **Остановить** выключает ВМ.
- **Serial** открывает serial-консоль ВМ. Логин `debian`, пароль `debian`.
- **SSH** подключается к ВМ по SSH с ключом из `image/keys/`. Пароль не нужен.
- **Переподключить** заново открывает соединение в терминале.

## API

| Метод | Путь | Что делает |
|-------|------|------------|
| GET | `/api/vm/status` | статус ВМ |
| POST | `/api/vm/start` | включить |
| POST | `/api/vm/reboot` | перезагрузить |
| POST | `/api/vm/stop` | выключить |
| WebSocket | `/ws/serial` | serial-консоль |
| WebSocket | `/ws/ssh` | SSH-терминал |
