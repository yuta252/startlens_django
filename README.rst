===================================
Startlensの管理画面及び分析ダッシュボード
===================================

目的
=====
Startlensプロジェクトにおける開発環境の構築

ツールのバージョン
==============
:Python:    3.6.10
:pip:       20.1.1


インストールと起動方法
==================
リポジトリーからコードを取得し、venv環境に依存ライブラリをインストールする

    #. $ git clone https://github.com/
    #. $ cd startlens
    #. $ python3.6 -m venv venv
    #. $ source venv/bin/activate
    #. (venv) $ pip install -r requirements/text.txt
    #. (venv) $ python3.6 manage.py runserver


AWSでの環境設定と起動方法
======================
:Ubuntu:    18.04
:インスタンスタイプ:    t2.micro

EC2インスタンス内での実行手順
    #. sudo apt -y update
    #. sudo apt -y upgrade
    #. sudo apt -y install build-essential python3-dev libsqlite3-dev libreadline6-dev libgdbm-dev zlib1g-dev libbz2-dev sqlite3 tk-dev zip libssl-dev
    #. wget https://www.python.org/ftp/python/3.6.10/Python-3.6.10.tgz
    #. tar xf Python-3.6.10.tgz
    #. cd Python-3.6.10
    #. ./configure —prefix=/opt/python3.6.10
    #. make
    #. sudo make install
    #. sudo ln -s /opt/python3.6.10/bin/python3.6 /usr/local/bin/python3.6
    #. sudo ln -s /opt/python3.6.10/bin/pip3.6 /usr/local/bin/pip

