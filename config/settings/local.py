"""
ローカル開発環境用の設定ファイル

"""
from .base import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

################
# Static Files #
################
"""
STATICFILES_DIRS:アプリケーションに紐づかない静的ファイルの配置ディレクトリ
"""
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
