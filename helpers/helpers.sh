#!/bin/bash

ft() {
  cat helpers/fast-setup.cfg > setup.cfg
  python setup.py test
}

st() {
  cat helpers/strict-setup.cfg > setup.cfg
  python setup.py test
}

cov() {
  ft && firefox htmlcov/index.html
}
