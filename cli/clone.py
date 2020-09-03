import os, shutil



def clone_ddragon_assets(dd_patch, cd_patch, path):
  cd_path = os.path.join(path, 'cdragon', cd_patch)
  dd_path = os.path.join(path, 'ddragon', dd_patch)
  dd_patch_short = dd_patch.rsplit('.', 1)[0]

  shutil.copyfile(os.path.join(dd_path, 'dragonhead.js'),
                  os.path.join(cd_path, 'dragonhead.js'))
  shutil.copyfile(os.path.join(dd_path, 'languages.js'),
                  os.path.join(cd_path, 'languages.js'))
  shutil.copyfile(os.path.join(dd_path, 'languages.json'),
                  os.path.join(cd_path, 'languages.json'))
  shutil.copytree(os.path.join(dd_path, 'lolpatch_' + dd_patch_short),
                  os.path.join(cd_path, 'lolpatch_' + cd_patch))
  shutil.copytree(os.path.join(dd_path, 'img', 'bg'),
                  os.path.join(cd_path, 'img', 'bg'))
  shutil.copytree(os.path.join(dd_path, 'img', 'global'),
                  os.path.join(cd_path, 'img', 'global'))
  shutil.copytree(os.path.join(dd_path, dd_patch, 'css'),
                  os.path.join(cd_path, cd_patch, 'css'))
  shutil.copytree(os.path.join(dd_path, dd_patch, 'js'),
                  os.path.join(cd_path, cd_patch, 'js'))
  shutil.copyfile(os.path.join(dd_path, dd_patch, 'manifest.js'),
                  os.path.join(cd_path, cd_patch, 'manifest.js'))
  shutil.copyfile(os.path.join(dd_path, dd_patch, 'manifest.json'),
                  os.path.join(cd_path, cd_patch, 'manifest.json'))
