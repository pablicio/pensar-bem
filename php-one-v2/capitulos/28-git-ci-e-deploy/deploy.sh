#!/usr/bin/env bash
set -euo pipefail

cd /var/www/casa-amarela

git fetch --tags
git checkout "$1"

composer install --no-dev --optimize-autoloader

php artisan down --retry=15

php artisan migrate --force

php artisan config:cache
php artisan route:cache
php artisan view:cache

php artisan queue:restart

php artisan up
