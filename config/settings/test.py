"""
テスト開発環境用の設定ファイル

"""
from .base import *
import environ

DEBUG = True

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


# TODO:　環境変数から読み込む
ALLOWED_HOSTS = ['*']

# HTTPアクセスを自動的にHTTPSのURLにリダイレクトする
# SECURE_SSL_REDIRECT = True

########
# APPS #
########
INSTALLED_APPS = [
    'analysis.apps.AnalysisConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    'storages',
]

############
# Database #
############

"""
ATMIC_REQUESTS: True
　トランザクションの有効範囲をリクエストの開始から終了までにする
"""
# TODO: データベース設定の変更
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'startlens',
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO',
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
STATIC_STORAGE: 
"""
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = '/var/www/{}/static'.format(PROJECT_NAME)

################
# AWS settings #
################
"""
AWSのアクセスキーにつき環境変数に組み込む
"""
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# 任意の非公開バケット
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_CUSTOM_DOMAIN = 'https//%s.s3-apnortheast-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

###############
# Media files #
###############
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# バケットのACLに準ずる
AWS_DEFAULT_ACL = None

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
        # 開発用
        'develop': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d %(message)s'
        },
    },
    # ハンドラ
    'handlers': {
        # コンソール出力用ハンドラ
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'develop',
        },
    },
    # ロガー
    'loggers': {
        # 自作アプリケーション全般のログを拾うロガー
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Django本体が出すログ全般を拾うロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # 発行されるSQL文を出力するための設定
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
