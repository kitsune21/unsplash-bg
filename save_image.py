import os
import sys

def get_user_home_directory():
  return os.path.expanduser('~')

def get_pictures_directory():
  home_dir = get_user_home_directory()

  if sys.platform == 'win32':
    pictures_path = os.path.join(home_dir, 'Pictures')
    if os.path.exists(pictures_path):
      return pictures_path
    return os.path.join(home_dir, 'My Documents', 'My Pictures')

  elif sys.platform == 'darwin':
    pictures_path = os.path.join(home_dir, 'Pictures')
    if os.path.exists(pictures_path):
      return pictures_path
    return os.path.join(home_dir, 'Photos')

  elif sys.platform.startswith('linux'):
    pictures_path = os.path.join(home_dir, 'Pictures')
    if os.path.exists(pictures_path):
      return pictures_path
    xdg_pictures_dir = os.path.join(os.environ.get('XDG_PICTURES_DIR', ''), '')
    if xdg_pictures_dir and os.path.exists(xdg_pictures_dir):
      return xdg_pictures_dir.rstrip(os.path.sep)
    return home_dir if os.path.exists(home_dir) else os.getcwd()

  else:
    print(f"Warning: Unsure how to find standard pictures directory on {sys.platform}. Using home directory.")
    return home_dir if os.path.exists(home_dir) else os.getcwd()


def get_default_backgrounds_directory():
  pictures_dir = get_pictures_directory()
  return os.path.join(pictures_dir, 'backgrounds')