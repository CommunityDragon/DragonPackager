import tempfile, requests, os, struct, zstd, io
from toolbox.patcher import PatcherManifest
import constants, util

bundle_dir = tempfile.mkdtemp()
manifest_dir = tempfile.mkdtemp()
patchlines_conf = requests.get(constants.patchlines_url).json()



def download(patchline = 'live', platform = 'mac', region = 'NA'):
  """
  downloads a manifest file
  """
  manifest_path = os.path.join(manifest_dir, '{region}.manifest'.format(region = region.lower()))
  if os.path.exists(manifest_path):
    return manifest_path
  data = patchlines_conf

  patchline_key = 'keystone.products.league_of_legends.patchlines.' + patchline
  if patchline_key not in data:
    print("patchline '{patchline}' not found".format(patchline))
    exit(1)
  data = data[patchline_key]['platforms']

  if platform not in data:
    print("platform '{platform}' not found".format(platform))
    exit(1)
  data = data[platform]['configurations']

  data = list(filter(lambda x: x['id'].lower() == region.lower(), data))
  if len(data) != 1:
    print("region '{region}' not found".format(platform))
    exit(1)
  
  data = list(filter(lambda x: x['id'].lower() == 'game_patch', data[0]['secondary_patchlines']))
  util.download(data[0]['url'], manifest_path)
  return manifest_path

# 'LeagueofLegends.app/Contents/MacOS/LeagueofLegends'

def fetch_file(filename, path, patchline = 'live', platform = 'mac', region = 'NA'):
  """
  fetches a file from the game client
  """
  rman = PatcherManifest(download(patchline, platform, region))
  file = rman.files[filename]
  bundle_ids = {}
  for chunk in file.chunks:
    bundle_ids[chunk.bundle.bundle_id] = True
  bundle_ids = list(bundle_ids.keys())
  
  for bundle_id in bundle_ids:
    name = f'{bundle_id:016X}.bundle'
    url = os.path.join(constants.riotcdn_url, 'channels', 'public', 'bundles', name)
    util.download(url, os.path.join(bundle_dir, name))

  f = open(path, 'wb')
  for chunk in file.chunks:
    bundle_id = chunk.bundle.bundle_id
    bundle = open(os.path.join(bundle_dir, f'{bundle_id:016X}.bundle'), 'rb')
    bundle.seek(chunk.offset)
    f.write(zstd.decompress(bundle.read(chunk.size)))
    bundle.close()
  f.close()
    
