import os
import util
import click
import requests
import constants
import tempfile
from toolbox.rstfile import RstFile
from pathlib import Path
from packaging import version



def get_cdragon_patch(patch):
  """
  fetches the CommunityDragon patch
  """
  data = requests.get(constants.cdragon_url + '/json').json()
  data = list(filter(lambda x: isinstance(version.parse(x['name']), version.Version), data))
  for _, cd_patch in enumerate(data):
    if patch == cd_patch['name']:
      return cd_patch['name']
  return ''



def get_ddragon_patch(patch):
  """
  fetches the DataDragon patch closest to the requested patch
  """
  data = requests.get(constants.ddragon_url + '/api/versions.json').json()
  for _, dd_patch in enumerate(data):
    if dd_patch.startswith(patch):
      return dd_patch
  return data[0]



def get_patch(patch):
  """
  fetches the CommunityDragon and DataDragon patch
  """
  data = {}
  data['cdragon'] = get_cdragon_patch(patch)
  if data['cdragon'] == '':
    click.UsageError('cdragon patch ' + patch + ' not found').show()
    exit(1)
  data['ddragon'] = get_ddragon_patch(patch)
  return data



def format_path(path, patch):
  """
  formats CommunityDragon URL path
  """
  return '{base}/{patch}/plugins/{path}'.format(
    base = constants.cdragon_url, 
    path = util.fixpath(path),
    patch = patch,
  )



lang_cache = {}
def get_languages_by_patch(patch):
  """
  fetches the languages by patch from CommunityDragon
  """
  if (len(lang_cache.keys()) > 0):
    return lang_cache

  tmp_path = tempfile.mkdtemp()
  data = requests.get('{base}/json/{patch}/{path}'.format(
    base = constants.cdragon_url, 
    patch = patch,
    path = 'game/data/menu'
  )).json()
  
  data = list(filter(lambda x: x['name'].startswith('fontconfig_'), data))
  for _, item in enumerate(data):
    if item['name'] != 'fontconfig_en_us.txt':
      continue
    export_path = os.path.join(tmp_path, item['name'])
    util.download('{base}/{patch}/{path}'.format(
      base = constants.cdragon_url, 
      patch = patch,
      path = 'game/data/menu/' + item['name'],
    ), export_path)
    country, lang = item['name'].replace('fontconfig_', '').replace('.txt', '').split('_')
    lang_cache[country + '_' + lang.upper()] = RstFile(export_path)
  return lang_cache



def get_champion_summary_by_patch(patch):
  """
  fetches a summary of champions by patch from CommunityDragon
  """
  data = requests.get('{base}/{patch}/{path}'.format(
    base = constants.cdragon_url, 
    patch = patch,
    path = 'plugins/rcp-be-lol-game-data/global/default/v1/champion-summary.json'
  )).json()
  data = list(filter(lambda x: x['id'] != -1, data))
  for i, champion in enumerate(data):
    data[i]['squarePortraitPath'] = format_path(champion['squarePortraitPath'], patch)
  return data



champion_cache = []
def get_champion_list_by_patch(patch):
  """
  fetches a list of champions by patch from CommunityDragon
  """
  summary = get_champion_summary_by_patch(patch)
  if (len(champion_cache) > 0):
    return champion_cache

  for _, champion_summary in enumerate(summary):
    champion = requests.get('{base}/{patch}/{path}'.format(
      base = constants.cdragon_url, 
      patch = patch,
      path = 'plugins/rcp-be-lol-game-data/global/default/v1/champions/{id}.json'.format(id = champion_summary['id'])
    )).json()

    champion['passive']['abilityIconExportPath'] = Path(champion['passive']['abilityIconPath']).name
    champion['passive']['abilityIconPath'] = format_path(champion['passive']['abilityIconPath'], patch)

    for i, spell in enumerate(champion['spells']):
      champion['spells'][i]['abilityIconExportPath'] = Path(spell['abilityIconPath']).name
      champion['spells'][i]['abilityIconPath'] = format_path(spell['abilityIconPath'], patch)

    for i, skin in enumerate(champion['skins']):
      champion['skins'][i]['tilePath'] = format_path(skin['tilePath'], patch)
      champion['skins'][i]['loadScreenPath'] = format_path(skin['loadScreenPath'], patch)
      champion['skins'][i]['uncenteredSplashPath'] = format_path(skin['uncenteredSplashPath'], patch)
    champion_cache.append(champion)
  return champion_cache

def get_item_summary_by_patch(patch):
  """
  fetches a list of items by patch from CommunityDragon
  """
  data = requests.get('{base}/{patch}/{path}'.format(
    base = constants.cdragon_url, 
    patch = patch,
    path = 'plugins/rcp-be-lol-game-data/global/default/v1/items.json'
  )).json()
  for i, item in enumerate(data):
    data[i]['iconPath'] = format_path(item['iconPath'], patch)
  return data



def get_item_bin_by_patch(patch):
  """
  fetches a list of bin items by patch from CommunityDragon
  """
  return requests.get('{base}/{patch}/{path}'.format(
    base = constants.cdragon_url, 
    patch = patch,
    path = 'game/global/items/items.bin.json'
  )).json()



def get_map_summary_by_patch(patch):
  """
  fetches a list of maps by patch from CommunityDragon
  """
  data = requests.get('{base}/{patch}/{path}'.format(
    base = constants.cdragon_url, 
    patch = patch,
    path = 'plugins/rcp-be-lol-game-data/global/default/v1/maps.json'
  )).json()
  data = list(filter(lambda x: x['id'] != 0, data))
  for i, mapdata in enumerate(data):
    data[i]['minimapPath'] = '{base}/{patch}/game/levels/map{id}/info/2dlevelminimap.png'.format(
      base = constants.cdragon_url, 
      patch = patch,
      id = mapdata['id']
    )
  return data



def get_mission_asset_names_by_patch(patch):
  """
  fetches a list of mission asset names by patch from CommunityDragon
  """
  data = requests.get('{base}/{patch}/{path}'.format(
    base = constants.cdragon_url, 
    patch = patch,
    path = 'plugins/rcp-be-lol-game-data/global/default/v1/mission-assets.json'
  )).json()
  data = list(filter(lambda x: x['path'].startswith('/lol-game-data/assets/ASSETS/Missions'), data))
  for i, mission in enumerate(data):
    data[i]['exportPath'] = mission['path'].replace('/lol-game-data/assets/ASSETS/Missions/', '')
    data[i]['path'] = format_path(mission['path'], patch)
  return data



def get_profile_icon_list_by_patch(patch):
  """
  fetches a list of profile icons by patch from CommunityDragon
  """
  data = requests.get('{base}/{patch}/{path}'.format(
    base = constants.cdragon_url, 
    patch = patch,
    path = 'plugins/rcp-be-lol-game-data/global/default/v1/profile-icons.json'
  )).json()
  for i, icon in enumerate(data):
    data[i]['iconPath'] = format_path(icon['iconPath'], patch)
  return data



def get_perk_list_by_patch(patch):
  """
  fetches a list of perks by patch from CommunityDragon
  """
  data = requests.get('{base}/{patch}/{path}'.format(
    base = constants.cdragon_url, 
    patch = patch,
    path = 'plugins/rcp-be-lol-game-data/global/default/v1/perks.json'
  )).json()
  for i, perk in enumerate(data):
    data[i]['iconExportPath'] = perk['iconPath'].replace('/lol-game-data/assets/v1/perk-images/', '')
    data[i]['iconPath'] = format_path(perk['iconPath'], patch)
  return data

