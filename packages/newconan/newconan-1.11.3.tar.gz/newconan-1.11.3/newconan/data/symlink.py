import os, sys, platform

try:
  if platform.system() == 'Windows':
    import _winapi
    _winapi.CreateJunction(sys.argv[1], sys.argv[2])
  else:
    os.symlink(sys.argv[1], sys.argv[2])
except FileExistsError:
  print(f"Symlink already exists: {sys.argv[2]}")
except Exception as e:
  print(f"{sys.argv},{e}")