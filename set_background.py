import sys
import subprocess
import os
import ctypes # Import ctypes for Windows

def get_os():
  return sys.platform

def set_macos_wallpaper(image_path):
  if not os.path.exists(image_path):
    print(f"Error: Image file not found at {image_path}")
    return
  script = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
  try:
    subprocess.run(['osascript', '-e', script], check=True)
    print(f"Desktop wallpaper set to: {image_path} (macOS)")
  except subprocess.CalledProcessError as e:
    print(f"Error setting wallpaper: {e}")
  except FileNotFoundError:
    print("Error: osascript command not found. Is macOS installed correctly?")

def set_windows_wallpaper(image_path):
  if not os.path.exists(image_path):
    print(f"Error: Image file not found at {image_path}")
    return
  SPI_SETDESKWALLPAPER = 20
  SPIF_UPDATEINIFILE = 1
  SPIF_SENDCHANGE = 2
  try:
    success = ctypes.windll.user32.SystemParametersInfoW(
      SPI_SETDESKWALLPAPER,
      0,
      image_path,
      SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )
    if success:
      print(f"Desktop wallpaper set to: {image_path} (Windows)")
    else:
      error_code = ctypes.GetLastError()
      print(f"Error setting wallpaper (Windows), error code: {error_code}")
  except AttributeError:
    print("Error: ctypes.windll.user32 not found. Are you running on Windows?")
  except Exception as e:
    print(f"An unexpected error occurred on Windows: {e}")

def set_linux_wallpaper_gnome(image_path):
  if not os.path.exists(image_path):
    print(f"Error: Image file not found at {image_path}")
    return
  try:
    subprocess.run([
      'gsettings',
      'set',
      'org.gnome.desktop.background',
      'picture-uri',
      f'file://{image_path}'
    ], check=True)
    print(f"Desktop wallpaper set to: {image_path} (Linux - GNOME)")
  except FileNotFoundError:
    print("Error: gsettings command not found. Is GNOME installed?")
  except subprocess.CalledProcessError as e:
    print(f"Error setting wallpaper (Linux - GNOME): {e}")

def set_desktop_wallpaper(image_path):
  os_name = get_os()
  absolute_image_path = os.path.abspath(image_path)
  if os_name == 'darwin':
    set_macos_wallpaper(absolute_image_path)
  elif os_name == 'win32':
    set_windows_wallpaper(absolute_image_path)
  elif os_name == 'linux':
    set_linux_wallpaper_gnome(absolute_image_path)
  else:
    print(f"Unsupported operating system: {os_name}")