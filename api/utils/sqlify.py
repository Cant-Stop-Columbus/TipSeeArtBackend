#! NB: Don't mess with this file unless you know what you're doing!

import os

def sqlify():
  path = os.environ["DATABASE_URL"].split(":")
  path[0]+="ql"
  return ":".join(path)
