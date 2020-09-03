import os, util, click, urllib, shutil, tarfile, pathlib, version, tempfile, clone, manifest, json
from pprint import pprint



def download(patch, path):
  """
  downloads all files of a patch
  """
  # resolving patch
  click.echo('resolving current patch...')
  data = version.get_patch(patch)
  click.echo('cdragon patch to be used: ' + data['cdragon'])
  click.echo('ddragon patch to be used: ' + data['ddragon'])
  util.create_clean_dir(os.path.join(path, 'ddragon', data['ddragon']))
  util.create_clean_dir(os.path.join(path, 'cdragon', data['cdragon']))

  # downloading assets
  click.echo('downloading ddragon dragontail and extracting assets...')
  download_ddragon_assets(data['ddragon'], data['cdragon'], path)
  click.echo('downloading cdragon versioned assets...')
  download_cdragon_assets(data['cdragon'], path)



def download_ddragon_assets(dd_patch, cd_patch, path):
  """
  downloads the DataDragon tarball and extracts it
  """
  tar_url = 'https://ddragon.leagueoflegends.com/cdn/dragontail-' + dd_patch + '.tgz'
  dir_path = os.path.join(path, 'ddragon', dd_patch)
  tmp_path = tempfile.mkdtemp()

  # download tarball into 
  os.makedirs(tmp_path, exist_ok=True)
  util.download(tar_url, os.path.join(tmp_path, 'data.tgz'))
  util.create_clean_dir(dir_path)

  tar = tarfile.open(os.path.join(tmp_path, 'data.tgz'))
  tar.extractall(dir_path)
  tar.close()
  clone.clone_ddragon_assets(dd_patch, cd_patch, path)



def download_cdragon_assets(patch, path):
  """
  downloads assets from CommunityDragon
  """
  download_cdragon_versioned_champion_squares(patch, path)
  download_cdragon_versioned_item_icons(patch, path)
  download_cdragon_versioned_minimaps(patch, path)
  download_cdragon_versioned_missions(patch, path)
  download_cdragon_versioned_profile_icons(patch, path)
  download_cdragon_versioned_champion_passives(patch, path)
  download_cdragon_versioned_champion_spells(patch, path)
  download_cdragon_champion_loading_portraits(patch, path)
  download_cdragon_champion_splash_arts(patch, path)
  download_cdragon_champion_tiles(patch, path)
  download_cdragon_perks(patch, path)
  download_cdragon_data(patch, path)
  


def download_cdragon_versioned_champion_squares(patch, path):
  """
  downloads versioned champion squares
  """
  champions = version.get_champion_summary_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, patch, 'img', 'champion')
  util.create_clean_dir(dir_path)

  for _, champion in enumerate(champions):
    util.download(champion['squarePortraitPath'], os.path.join(dir_path, champion['alias'] + '.png'))



def download_cdragon_versioned_item_icons(patch, path):
  """
  downloads versioned item icons
  """
  items = version.get_item_summary_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, patch, 'img', 'item')
  util.create_clean_dir(dir_path)

  for _, item in enumerate(items):
    util.download(item['iconPath'], os.path.join(dir_path, '{id}.png'.format(id = item['id'])))



def download_cdragon_versioned_minimaps(patch, path):
  """
  downloads versioned minimaps
  """
  maps = version.get_map_summary_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, patch, 'img', 'map')
  util.create_clean_dir(dir_path)

  for _, mapdata in enumerate(maps):
    util.download(mapdata['minimapPath'], os.path.join(dir_path, '{id}.png'.format(id = mapdata['id'])))



def download_cdragon_versioned_missions(patch, path):
  """
  downloads versioned missions
  """
  missions = version.get_mission_asset_names_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, patch, 'img', 'mission')
  util.create_clean_dir(dir_path)

  for _, mission in enumerate(missions):
    os.makedirs(os.path.join(dir_path, os.path.dirname(mission['exportPath'])), exist_ok=True)
    util.download(mission['path'], os.path.join(dir_path, mission['exportPath']))



def download_cdragon_versioned_profile_icons(patch, path):
  """
  downloads versioned profile icons
  """
  icons = version.get_profile_icon_list_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, patch, 'img', 'profileicon')
  util.create_clean_dir(dir_path)

  for _, icon in enumerate(icons):
    util.download(icon['iconPath'], os.path.join(dir_path, '{id}.png'.format(id = icon['id'])))



def download_cdragon_versioned_champion_passives(patch, path):
  """
  downloads versioned champion passives
  """
  champions = version.get_champion_list_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, patch, 'img', 'passive')
  util.create_clean_dir(dir_path)

  for _, champion in enumerate(champions):
    util.download(champion['passive']['abilityIconPath'], os.path.join(dir_path, champion['passive']['abilityIconExportPath']))



def download_cdragon_versioned_champion_spells(patch, path):
  """
  downloads versioned champion spells
  """
  champions = version.get_champion_list_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, patch, 'img', 'spell')
  util.create_clean_dir(dir_path)

  for _, champion in enumerate(champions):
    for _, spell in enumerate(champion['spells']):
      util.download(spell['abilityIconPath'], os.path.join(dir_path, spell['abilityIconExportPath']))



def download_cdragon_champion_loading_portraits(patch, path):
  """
  downloads champion loading portraits
  """
  champions = version.get_champion_list_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, 'img', 'champion', 'loading')
  util.create_clean_dir(dir_path)

  for _, champion in enumerate(champions):
    for _, skin in enumerate(champion['skins']):
      util.download(skin['loadScreenPath'], os.path.join(dir_path, '{name}_{id}.jpg'.format(
        name = champion['alias'],
        id = skin['id'] - (1000 * champion['id']),
      )))



def download_cdragon_champion_splash_arts(patch, path):
  """
  downloads champion splash arts
  """
  champions = version.get_champion_list_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, 'img', 'champion', 'splash')
  util.create_clean_dir(dir_path)

  for _, champion in enumerate(champions):
    for _, skin in enumerate(champion['skins']):
      util.download(skin['uncenteredSplashPath'], os.path.join(dir_path, '{name}_{id}.jpg'.format(
        name = champion['alias'],
        id = skin['id'] - (1000 * champion['id']),
      )))



def download_cdragon_champion_tiles(patch, path):
  """
  downloads champion tiles
  """
  champions = version.get_champion_list_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, 'img', 'champion', 'tiles')
  util.create_clean_dir(dir_path)

  for _, champion in enumerate(champions):
    for _, skin in enumerate(champion['skins']):
      util.download(skin['tilePath'], os.path.join(dir_path, '{name}_{id}.jpg'.format(
        name = champion['alias'],
        id = skin['id'] - (1000 * champion['id']),
      )))



def download_cdragon_perks(patch, path):
  """
  downloads perks 
  """
  perks = version.get_perk_list_by_patch(patch)
  dir_path = os.path.join(path, 'cdragon', patch, 'img', 'perk-images')
  util.create_clean_dir(dir_path)

  for _, perk in enumerate(perks):
    os.makedirs(os.path.join(dir_path, os.path.dirname(perk['iconExportPath'])), exist_ok=True)
    util.download(perk['iconPath'], os.path.join(dir_path, perk['iconExportPath']))



def download_cdragon_data(patch, path):
  """
  downloads all json data
  """
  download_cdragon_item_data(patch, path)



def download_cdragon_item_data(patch, path):
  """
  downloads item json data
  """
  langs = version.get_languages_by_patch(patch)
  maps = version.get_map_summary_by_patch(patch)
  items = version.get_item_summary_by_patch(patch)
  bin_items = version.get_item_bin_by_patch(patch)

  item = items[0]
  bin_item = bin_items['Items/{id}'.format(id = item['id'])]
  result = {'data': {}}

  for item in items:
    item_id = '{id}'.format(id = item['id'])
    bin_item = bin_items['Items/' + item_id] if ('Items/' + item_id) in bin_items else next(filter(lambda x: 'itemID' in bin_items[x] and bin_items[x]['itemID'] == item['id'], bin_items.keys()))
    try:
      result['data'][item_id] = {
        'name': item['name'],
        'description': item['description'],
        'colloq': langs['en_US'].__getitem__('game_item_colloquialism_' + item_id),
        'plaintext': langs['en_US'].__getitem__('game_item_plaintext_' + item_id),
        'into': list(map(lambda x: '{x}'.format(x = x), item['to'])),
        'image': {},
        'gold': {
          'base': item['price'],
          'purchasable': item['inStore'],
          'total': item['priceTotal'],
          'sell': round(item['priceTotal'] * (bin_item['sellBackModifier'] if 'sellBackModifier' in bin_item else 0.7)),
        },
        'tags': item['categories'],
        'maps': dict(map(lambda x: ['{id}'.format(id = x['id']), x['mapStringId'] in item['mapStringIdInclusions']], maps)),
        'stats': dict(map(lambda x: [util.capitalize(x[1:] if x[0].startswith('m') and x[1].upper() == x[1] else x), bin_item[x]], list(filter(lambda x: x.endswith("Mod"), bin_item))))
      }
    except:
      continue

  dir_path = os.path.join(path, 'cdragon', patch, 'en_US')
  util.create_clean_dir(dir_path)
  f = open(os.path.join(dir_path, 'items.json'), 'w')
  f.write(json.dumps(result, indent=2))
  f.close()
  
