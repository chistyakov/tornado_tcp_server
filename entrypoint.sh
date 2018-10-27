#!/usr/bin/env sh


if [ "$1" = "tests" ]
then
  echo "run tests"
  python -m doctest -v ./core/*.py
  python -m tornado.testing tests
fi

if [ "$1" = "server" ]
then
  echo "run tcp server"
  python app.py
fi
