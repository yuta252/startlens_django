"""
本番開発環境用の設定ファイル

"""
from .base import *

DEBUG = False

#TODO: 設定変更
ALLOWED_HOSTS = ['*']

# HTTPアクセスをz自動的にHTTPSのURLにリダイレクトする
# SECURE_SSL_REDIRECT = True

############
# Database #
############

"""
ATMIC_REQUESTS: True
　トランザクションの有効範囲をリクエストの開始から終了までにする
"""
#TODO: データベース設定の変更
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'startlens',
        'USER': 'startlensuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'sql_mode': 'TRADITIONAL, NO_AUTO_VALUE_ON_ZERO',
        }
    }
}

################
# Static Files #
################

"""
STATICFILES_DIRS:アプリケーションに紐づかない静的ファイルの配置ディレクトリ
STATIC_ROOT: 静的ファイルの配信元（本番環境での配信元）
             DEBUG=Falseの場合runserverは動作しないためSTATIC_ROOTを参照する
             python manage.py collectstaticコマンドで静的ファイルを集約する
"""
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = '/var/www/{}/static'.format(PROJECT_NAME)

###########
# Logging #
###########
LOGGING = {
    # バージョンは1固定
    'version': 1,
    # 既存ログの設定を無効化しない
    'disable_existing_loggers': False,
    # ログフォーマット
    'formatters': {
        # 本番用
        'production': {
            'format': '%(asctime)s [%(levelname)s] %(process)s %(thread)s %(pathname)s:%(lineno)d %(message)s'
        },
    },
    # ハンドラ
    'handlers': {
        # コンソール出力用ハンドラ
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/{}/app.log'.format(PROJECT_NAME),
            'formatter': 'production',
        },
    },
    # ロガー
    'loggers': {
        # 自作アプリケーション全般のログを拾うロガー
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Django本体が出すログ全般を拾うロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
