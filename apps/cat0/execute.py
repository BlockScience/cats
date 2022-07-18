import pytest, json
from apps.cat0 import catFactory
from pycats.function.process.ipfs import ProcessClient

catFactory.build_cats()
catFactory.terraform()
catFactory.execute()