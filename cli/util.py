import urllib.request, struct
from tqdm import tqdm
import os, shutil



class DownloadProgressBar(tqdm):
  """
  download progressbar class
  """
  def update_to(self, b=1, bsize=1, tsize=10):
    if tsize is not None:
      self.total = tsize
    self.update(b * bsize - self.n)



def download(url, filename):
  """
  downloads a file
  """
  with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1],
                           bar_format='downloading {l_bar}{bar:20}| {n_fmt}/{total_fmt}') as t:
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    try:
      urllib.request.urlretrieve(url, filename, reporthook=t.update_to)
    except:
      download(url, filename)



def create_clean_dir(dir_path):
  """
  creates a directory and makes sure its empty
  """
  if os.path.exists(dir_path):
    shutil.rmtree(dir_path)
  os.makedirs(dir_path, exist_ok=True)



def copytree(src, dst, symlinks=False, ignore=None):
  """
  copies a directory
  """
  for item in os.listdir(src):
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if os.path.isdir(s):
      shutil.copytree(s, d, symlinks, ignore)
    else:
      shutil.copy2(s, d)



def fixpath(val):
  """
  fixes cdragon paths
  """
  return val.replace('/lol-game-data/assets', 'rcp-be-lol-game-data/global/default').lower()



def unpack(f, fmt):
  """
  unpacks a binary
  """
  length = struct.calcsize(fmt)
  return struct.unpack(fmt, f.read(length))



def capitalize(str):
  """
  capitalizer text
  """
  return str[0].upper() + str[1:]