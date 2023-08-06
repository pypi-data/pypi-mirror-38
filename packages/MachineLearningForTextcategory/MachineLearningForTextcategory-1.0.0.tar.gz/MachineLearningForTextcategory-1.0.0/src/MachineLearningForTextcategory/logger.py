# !/usr/bin/env python
# coding: utf-8

import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

LOG.addHandler(handler)
LOG.addHandler(console)