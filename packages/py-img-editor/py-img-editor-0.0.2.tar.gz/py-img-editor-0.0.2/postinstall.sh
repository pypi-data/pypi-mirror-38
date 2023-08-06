#!/usr/bin/env bash

curl http://uwsgi.it/install | bash -s cgi /tmp/uwsgi
cd uwsgi_latest_from_installer
python uwsgiconfig.py --plugin plugins/cgi
cd ../
rm -rf uwsgi_latest_from_installer
rm uwsgi_latest_from_installer.tar.gz