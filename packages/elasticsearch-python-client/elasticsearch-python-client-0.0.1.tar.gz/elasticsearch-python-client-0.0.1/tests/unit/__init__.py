import sys
import os

path = os.path.dirname(format(os.path.realpath(__file__)))
parent_path = "/".join(path.split("/")[0:-1])
grand_parent = "/".join(path.split("/")[0:-2])

sys.path.append("{}/lib".format(parent_path))
sys.path.append(grand_parent)

