#!/usr/bin/env sh


if [ "$1" = "tests" ]
then
  echo "run tests"
  python -m unittest tests
fi

if [ "$1" = "server" ]
then
  echo "run tcp server"
  python app.py
fi
