from os import chdir as cd, mkdir
from os.path import exists, join, dirname, realpath
import argparse
import re
import urllib.request
import pip
import pkgutil
import sys


def mkdirs(*dirs):
  for dir in dirs:
    if not exists(dir):
      mkdir(dir)


def download(url, filename):
  urllib.request.urlretrieve(url, filename)


def install(package):
  if hasattr(pip, 'main'):
    pip.main(['install', package])
  else:
    pip._internal.main(['install', package])


def RMW(file, op):
  with open(join(script_dir, file), "r") as fin:
    content = fin.read()
  content = op(content)
  with open(file, "w") as fout:
    fout.write(content)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("project_name", help="The name of your project.")
  parser.add_argument("--project_type", choices=["exe", "static", "shared"], default="exe",
                      help="The type of your project, choices are exe(default), static, shared.")
  args = parser.parse_args()
  project_name = args.project_name.strip()
  project_name = re.sub(r"\s+", "_", project_name)
  project_name = ''.join(x.capitalize() for x in re.split(r"[_\-]+", project_name))
  project_type = args.project_type
  mkdirs(project_name)
  cd(project_name)
  mkdirs("bin", "cmake", "src", "third_party")
  
  script_dir = join(dirname(sys.executable), "data")
  replace = lambda content: content.replace("{project_name}", project_name)
  copy = lambda content: content
  RMW("CMakeLists.txt", replace)
  RMW("conanfile.py", replace)
  RMW(".clang-format", copy)
  RMW(".gitignore", copy)
  cd("src"), RMW("main.cpp", copy)
  cd("../cmake"), RMW("conan.cmake", copy)
  
  install("conan")
