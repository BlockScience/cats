import sys

sys.path.append("../..")
from apps.cat0 import catFactory

# catFactory.build_cats()
catFactory.terraform()
catFactory.execute()

# 15:35:43
# 15:37:28