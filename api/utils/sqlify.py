import os

def sqlify():
  path = os.environ["DATABASE_URL"].split(":")
  path[0]+="ql"
  return ":".join(path)