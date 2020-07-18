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
EC2インスタンス環境
:Ubuntu: 18.04
:インスタンスタイプ: t2.micro

1. sudo apt -y update
2. sudo apt -y upgrade
3. sudo apt -y install build-essential python3-dev libsqlite3-dev libreadline6-dev libgdbm-dev zlib1g-dev libbz2-dev sqlite3 tk-dev zip libssl-dev
4. wget https://www.python.org/ftp/python/3.6.10/Python-3.6.10.tgz
5. tar xf Python-3.6.10.tgz
6. cd Python-3.6.10
7. ./configure —prefix=/opt/python3.6.10
8. make
9. sudo make install
10. sudo ln -s /opt/python3.6.10/bin/python3.6 /usr/local/bin/python3.6
11. sudo ln -s /opt/python3.6.10/bin/pip3.6 /usr/local/bin/pip

