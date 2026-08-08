#!/bin/sh

set -e

export PYTHONUSERBASE=/usr/local

echo "Ожидание запуска базы данных для Superset..."
sleep 10

export PATH="/usr/local/bin:$PATH"
export FLASK_APP=superset

echo "1/3 Накатываем миграции БД..."
superset db upgrade

echo "2/3 Создаем учетную запись администратора..."
superset fab create-admin \
    --username "$SUPERSET_ADMIN_USER" \
    --firstname Admin \
    --lastname Admin \
    --email admin@fab.org \
    --password "$SUPERSET_ADMIN_PASSWORD" || true

echo "3/3 Инициализируем роли..."
superset init

# импорт дашборда
#echo "4/4 Импортируем дашборд из ZIP..."

#if [ -f "/app/dashboards/dashboard_export.zip" ]; then
#    echo "✅ Файл найден, импортируем..."
#    superset import-dashboards \
#        --username "$SUPERSET_ADMIN_USER" \
#        --path /app/dashboards/dashboard_export.zip
#    echo "✅ Дашборд импортирован!"
#else
#    echo "⚠️ Файл не найден: /app/dashboards/dashboard_export.zip"
#fi

echo "✅ Инициализация Superset успешно завершена!"