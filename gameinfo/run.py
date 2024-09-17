import xml.etree.ElementTree as ET
import requests
import json
# import xml.dom.minidom as DOM

my_games = [
'5 minute dungeon',
'5 minute mystery',
'7-Wonders',
'azul',
'bears vs babies',
'blokus',
'chomp',
'Clank!: A Deck-Building Adventure', # found and hardcoded
'codenames',
'couture',
'dark dealings',
'dixit',
'exploding kittens',
'forbidden island',
'fuzzy mage fight',
'here to slay',
'hnefatafl',
'in a pickle',
'jaipur',
'king of tokyo',
'kiri-ai the duel',
'love letter: batman',
'mare nostrum',
'merchants of the dark road',
'migration mars',
'mind space',
'monopoly deal',
'mountain goats',
'munchkin adventure time',
'munchkin deluxe',
'otto game over',
'Overboss: A Boss Monster Adventure', # found and hardcoded
'pit',
'potato pirates: enter the spudnet',
'potato pirates',
'radlands',
'ravine',
'regular show flux',
'rick and morty total rickall',
'sail',
'secret hitler',
'sequoia',
'skipbo',
# 'skull 2011',
'solarquest',
# 'space base 2018',
'spaceteam',
# 'spots 2022',
'star trek fluxx',
'sushi go!',
'taco cat goat cheese pizza',
'takenoko',
'terraforming mars',
'The Binding of Isaac: Four Souls', # found and hardcoded
'the fox and the forest',
'the princess bride i hate to kill you',
'the royal game of ur',
'ticket to ride',
'trash pandas',
# 'treasure hunter 2015',
'tsuro of the seas',
'unstable unicorns'
]


known_ids = [
  92415, # skull 2011
  242302, # space base 2018
  372559, # spots 2022
  182189 # treasure hunter
]


output = []
try_again = []

for game_name in my_games:
    print(f'game name - {game_name}')
    exact_res = requests.get(f'https://boardgamegeek.com/xmlapi/search?search={game_name}&exact=1')
    exact = ET.fromstring(exact_res.text)
    boardgame_xml = exact.find('boardgame')

    if boardgame_xml == None:
        print('could not find exact match, trying fuzzy search')
        fuzzy_res = requests.get(f'https://boardgamegeek.com/xmlapi/search?search={game_name}')

        # dom = DOM.parseString(fuzzy_res.text)
        # print(dom.toprettyxml())
        fuzzy = ET.fromstring(fuzzy_res.text)
        boardgame_xml = fuzzy.find('boardgame')

        if boardgame_xml == None:
            try_again.append(game_name)
            continue

    bggid = boardgame_xml.attrib['objectid']
    game_res = requests.get(f'https://boardgamegeek.com/xmlapi/game/{bggid}')
    # dom = DOM.parseString(game_res.text)
    # print(dom.toprettyxml())
    game_xml = ET.fromstring(game_res.text)
    bgg = game_xml.find('boardgame')

    name = bgg.find('.//name[@primary="true"]')

    thumb = bgg.find('thumbnail')
    if thumb == None:
        thumb = ''
    else:
      thumb = thumb.text

    output.append({"bgg_id": bggid,"name": name.text, "url": f'https://boardgamegeek.com/boardgame/{bggid}', "image_url": thumb })


for known_id in known_ids:
    print(f'working through known ids that are dupes in bgg api: {known_id}')
    known_res = requests.get(f'https://boardgamegeek.com/xmlapi/game/{known_id}')
    # dom = DOM.parseString(known_res.text)
    # print(dom.toprettyxml())
    known_xml = ET.fromstring(known_res.text)
    bgg = known_xml.find('boardgame')

    name = bgg.find('.//name[@primary="true"]')

    thumb = bgg.find('thumbnail')
    if thumb == None:
        thumb = ''
    else:
      thumb = thumb.text

    output.append({"bgg_id": known_id, "name": name.text, "url": f'https://boardgamegeek.com/boardgame/{known_id}', "image_url": thumb })

with open('games.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'The following games were not found by exact or fuzzy match: {try_again}')
