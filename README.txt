# Migration Qase to TestIT

Этот проект предоставляет инструмент для миграции тестов из Qase в TestIT. Инструмент автоматизирует процесс миграции, обеспечивая целостность данных и эффективную передачу.

## Содержание

- [Описание](#описание)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Использование](#использование)
- [Зависимости](#зависимости)

## Описание

**Migration Qase to TestIT** — это инструмент для упрощения переноса тестов из [Qase](https://qase.io) в [TestIT](https://testit.software). Он получает тесты из Qase с использованием их API и загружает их в TestIT через API TestIT.

Основные функции:
- Извлечение тестов из Qase.
- Преобразование данных в формат TestIT.
- Автоматическая загрузка тестов в TestIT.

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Angel00014/migration_qase_to_testit.git
    ```
2. Перейдите в директорию проекта:
    ```bash
    cd migration_qase_to_testit
    ```
3. Создайте и активируйте виртуальное окружение (рекомендуется):
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте: venv\Scripts\activate
    ```
4. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Конфигурация

Описанна в .env файле.

HOST_SYSTEM
PORT_SYSTEM
LOG_LEVEL
ACCESS_LOG

## Использование

#1. Перейти в директорию проекта

    ```bash
    cd migration_qase_to_testit
    ```

#2. Соберать Docker-образ проекта

    ```bash
    docker build -t migration_qase_to_testit .
    ```

#3. Запустить контейнер с использованием Docker

    ```bash
    docker run -d -p 8002:8002 migration_qase_to_testit .
    ```
#4. Перейти на localhost:8002 (или порт который вы указали при конфигурации или при запуске docker контейнера)

    #Дальнейшее описани будет приведено в файле "тут будет ссылка на файл"


## Зависимости

Полный список зависимостей указан в файле requirements.txt