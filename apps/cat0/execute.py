import sys
from pathlib import Path
apps_dir = str(Path(__file__).resolve().parents[1])
sys.path.append(apps_dir)
# print(sys.path)
# exit()
from apps.cat0 import catFactory

# catFactory.build_cats()
catFactory.terraform()
catFactory.execute()

# 15:35:43
# 15:37:28