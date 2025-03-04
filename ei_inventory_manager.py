import requests
import datetime
import humanize
import ei_pb2
import base64
import time
import json
import os
import re

base_dir = 'C://Desktop//Discord Bot//bot_data//egg_inc_data//'

stone_types = ["PROPHECY", "CLARITY", "LIFE", "QUANTUM", "DILITHIUM", "SOUL", "TERRA", "TACHYON", "SHELL", "LUNAR"]
ingredient_types = ["GOLD METEORITE", "SOLAR TITANIUM", "TAU CETI GEODE"]
artifact_types = ["LIGHT OF EGGENDIL", "BOOK OF BASAN", "TACHYON DEFLECTOR", "SHIP IN A BOTTLE", "TITANIUM ACTUATOR", "DILITHIUM MONOCLE", "QUANTUM METRONOME", 
                  "PHOENIX FEATHER", "THE CHALICE", "INTERSTELLAR COMPASS", "CARVED RAINSTICK", "BEAK OF MIDAS", "MERCURYS LENS", "NEODYMIUM MEDALLION", "ORNATE GUSSET", 
                  "TUNGSTEN ANKH", "AURELIAN BROOCH", "VIAL MARTIAN DUST", "DEMETERS NECKLACE", "LUNAR TOTEM", "PUZZLE CUBE"]
legendary_types = ["T4L LIGHT OF EGGENDIL", "T4L BOOK OF BASAN", "T4L TACHYON DEFLECTOR", "T4L SHIP IN A BOTTLE", "T4L TITANIUM ACTUATOR", "T4L DILITHIUM MONOCLE", 
                   "T4L QUANTUM METRONOME", "T4L PHOENIX FEATHER", "T4L THE CHALICE", "T4L INTERSTELLAR COMPASS", "T4L CARVED RAINSTICK", "T4L BEAK OF MIDAS", 
                   "T4L MERCURYS LENS", "T4L NEODYMIUM MEDALLION", "T4L ORNATE GUSSET", "T3L TUNGSTEN ANKH", "T4L TUNGSTEN ANKH", "T4L AURELIAN BROOCH",
                   "T4L VIAL MARTIAN DUST", "T4L DEMETERS NECKLACE", "T4L LUNAR TOTEM", "T4L PUZZLE CUBE"]

legendary_base = {"T4L LIGHT OF EGGENDIL": 1000., "T4L BOOK OF BASAN": 1000., "T4L TACHYON DEFLECTOR": 1200., "T4L SHIP IN A BOTTLE": 1200., 
                   "T4L TITANIUM ACTUATOR": 1000., "T4L DILITHIUM MONOCLE": 1000., "T4L QUANTUM METRONOME": 1000., "T4L PHOENIX FEATHER": 1000., 
                   "T4L THE CHALICE": 1000., "T4L INTERSTELLAR COMPASS": 1000., "T4L CARVED RAINSTICK": 1000., "T4L BEAK OF MIDAS": 1500., 
                   "T4L MERCURYS LENS": 1000., "T4L NEODYMIUM MEDALLION": 1000., "T4L ORNATE GUSSET": 1000., "T3L TUNGSTEN ANKH": 1000., 
                   "T4L TUNGSTEN ANKH": 1000., "T4L AURELIAN BROOCH": 1000., "T4L VIAL MARTIAN DUST": 1000., "T4L DEMETERS NECKLACE": 1000., 
                   "T4L LUNAR TOTEM": 1500., "T4L PUZZLE CUBE": 1000.}

##### FUNCTIONS CALLED BY OTHER FUNCTIONS #####

def get_artifact_key_indices(data):
    artifact_key_indices = []
    index = 0
    for item in data:
        if 'artifact' in item:
            artifact_key_indices.append(index)
        index += 1
    return artifact_key_indices

def sort_neatly(data, artifact_key_indices):
    number_of_indices = len(artifact_key_indices)
    cleaned_list = {}

    for i in range(number_of_indices):
        if i < number_of_indices - 1:
            section = data[artifact_key_indices[i]:artifact_key_indices[i+1]]
        else:
            section = data[artifact_key_indices[i]:]

        name = (str(section[2]).split('name: ')[-1]).split('\n')[0]
        if 'STONE' in name:
            stones = []
            if 'FRAGMENT' in name:
                name = make_name(name, section, True, False)
                type = 'fragment'
            else:
                name = make_name(name, section, False, False)
                type = 'stone'
        elif 'SOLAR_' in name or 'GOLD_' in name or 'TAU_' in name:
            name = make_name(name, section, False, False)
            type = 'ingredient'
            stones = []
        else:
            name = make_name(name, section, False, False)
            type = 'artifact'
            if 'stones' not in section[7]:
                stones = []
            else:
                stones = find_stones(section)

        if name in cleaned_list:
            extension = 2
            while name + f' #{extension}' in cleaned_list:
                extension += 1
            name = name + f' #{extension}'

        quantity = int((str(section[-3]).split('quantity: ')[-1]).split('\n')[0])
        
        cleaned_list[name] = [type, quantity, stones]
    return cleaned_list

def make_name(base_name, section, fragment = False, slotted = False, slot_number = 0):
    raw_levels = ['INFERIOR', 'LESSER', 'NORMAL', 'GREATER']
    raw_rarities = ['COMMON', 'RARE', 'EPIC', 'LEGENDARY']
    rarities = ['', 'R', 'E', 'L']
    if not slotted:
        if not fragment:
            level = str(raw_levels.index((str(section[3]).split('level: ')[-1]).split('\n')[0]) + 1)
        else:
            level = 0
        rarity = rarities[raw_rarities.index((str(section[4]).split('rarity: ')[-1]).split('\n')[0])]
        name = f'T{level}{rarity} {" ".join(str(base_name).split("_"))}'
        return name
    else:
        level = str(raw_levels.index((str(section[3+6*slot_number]).split('level: ')[-1]).split('\n')[0]) + 1)
        name = f'T{level} {" ".join(str(base_name).split("_"))}'
        return name

def find_stones(section):
    if len(section) == 17:
        base_name1 = (str(section[8]).split('name: ')[-1]).split('\n')[0]
        name1 = make_name(base_name1, section, False, True, 1)
        stones = [name1]
    elif len(section) == 23:
        base_name1 = (str(section[8]).split('name: ')[-1]).split('\n')[0]
        name1 = make_name(base_name1, section, False, True, 1)
        base_name2 = (str(section[14]).split('name: ')[-1]).split('\n')[0]
        name2 = make_name(base_name2, section, False, True, 2)
        stones = [name1, name2]
    elif len(section) == 29:
        base_name1 = (str(section[8]).split('name: ')[-1]).split('\n')[0]
        name1 = make_name(base_name1, section, False, True, 1)
        base_name2 = (str(section[14]).split('name: ')[-1]).split('\n')[0]
        name2 = make_name(base_name2, section, False, True, 2)
        base_name3 = (str(section[20]).split('name: ')[-1]).split('\n')[0]
        name3 = make_name(base_name3, section, False, True, 3)
        stones = [name1, name2, name3]
    else:
        stones = ['failed to identify stones']
    return stones

def get_current_missions(mission_data):
    mission_times = []

    mission_blocks = re.split(r'status:', mission_data)

    for block in mission_blocks:
        item = [0,0]
        attributes = re.findall(r'(\w+):\s*(\w+)', block)
        for key, value in attributes:
            if key.lower() == 'start_time_derived':
                item[0] = int(value)
            if key.lower() == 'duration_seconds':
                item[1] = int(value)
        mission_times.append(item)

    return mission_times[1:]

def get_stats(game_backup, stats_backup):
    raw_se = game_backup.soul_eggs_d
    se = humanize.intword(raw_se, format="%.3f")
    pe = game_backup.eggs_of_prophecy
    mult = int(((str(game_backup.epic_research).split('\n'))[1::2][-3]).split(' ')[1]) # get the PROPHECY BONUS level
    eb = humanize.intword(100 * (((105 + mult) / 100) ** pe) * (1.5 * raw_se), format="%.3f")
    ge = "{:,}".format(game_backup.golden_eggs_earned - game_backup.golden_eggs_spent)
    pb = game_backup.piggy_bank
    pb_mult = 1 + stats_backup.num_piggy_breaks
    scaled_pb = "{:,}".format(round(pb * (1 + (10 * pb_mult + 10)/100)))
    return se, pe, eb, ge, scaled_pb

def parse_api_response(response: str):
    items = {}
    
    # Regex to find all spec blocks
    spec_blocks = re.split(r',\s*spec\s*{', response)  # Split into chunks

    for block in spec_blocks:
        item = {}

        # Extract other key-value pairs
        attributes = re.findall(r'(\w+):\s*(\w+)', block)
        for key, value in attributes:
            # Convert boolean-like strings and numbers
            if value.lower() in {"true", "false"}:
                item[key] = value.lower() == "true"
            elif key.lower() == "name":
                name = ' '.join((value).split('_'))
            elif value.isdigit():
                item[key] = int(value)
            elif value.lower() in ["inferior", "lesser", "normal", "greater"]:
                if 'STONE' not in name:
                    extension = ["T1", "T2", "T3", "T4"][["inferior", "lesser", "normal", "greater"].index(value.lower())]
                else:
                    if 'FRAGMENT' in name:
                        extension = "T0"
                    else:
                        extension = ["T1", "T2", "T3"][["inferior", "lesser", "normal"].index(value.lower())]

        items[f"{extension} {name}"] = item

    return items

def get_multiplier(craft_xp: int):
    match craft_xp:
        case _ if craft_xp < 500:
            multip = 1.00
        case _ if craft_xp < 3000:
            multip = 1.05
        case _ if craft_xp < 8000:
            multip = 1.10
        case _ if craft_xp < 18000:
            multip = 1.15
        case _ if craft_xp < 43000:
            multip = 1.20
        case _ if craft_xp < 93000:
            multip = 1.25
        case _ if craft_xp < 193000:
            multip = 1.30
        case _ if craft_xp < 443000:
            multip = 1.35
        case _ if craft_xp < 943000:
            multip = 1.40
        case _ if craft_xp < 1943000:
            multip = 1.45
        case _ if craft_xp < 3943000:
            multip = 1.50
        case _ if craft_xp < 7943000:
            multip = 1.55
        case _ if craft_xp < 15943000:
            multip = 1.60
        case _ if craft_xp < 30943000:
            multip = 1.65
        case _ if craft_xp < 50943000:
            multip = 1.70
        case _ if craft_xp < 85943000:
            multip = 1.75
        case _ if craft_xp < 145943000:
            multip = 1.85
        case _ if craft_xp < 245943000:
            multip = 2.00
        case _ if craft_xp < 395943000:
            multip = 2.25
        case _ if craft_xp < 595943000:
            multip = 2.50
        case _ if craft_xp < 845943000:
            multip = 3.00
        case _ if craft_xp < 1145943000:
            multip = 3.50
        case _ if craft_xp < 1470943000:
            multip = 4.00
        case _ if craft_xp < 1820943000:
            multip = 4.50
        case _ if craft_xp < 2220943000:
            multip = 5.00
        case _ if craft_xp < 2720943000:
            multip = 6.00
        case _ if craft_xp < 3320943000:
            multip = 7.00
        case _ if craft_xp < 4070943000:
            multip = 8.00
        case _ if craft_xp < 5070943000:
            multip = 9.00
        case _:
            multip = 10.00
    return multip

def save(dict, name):
    json_object = json.dumps(dict, indent=4)
    with open(name, 'w') as writer:
        writer.write(json_object)

##### FUNCTIONS CALLED FROM OUTSIDE #####

def get_full_inventory(user: str, user_id: str) -> None:
    first_contact_request = ei_pb2.EggIncFirstContactRequest()
    first_contact_request.ei_user_id = user_id
    first_contact_request.client_version = 42

    url = 'https://www.auxbrain.com/ei/bot_first_contact'
    data = { 'data' : base64.b64encode(first_contact_request.SerializeToString()).decode('utf-8') }
    response = requests.post(url, data = data)

    first_contact_response = ei_pb2.EggIncFirstContactResponse()
    first_contact_response.ParseFromString(base64.b64decode(response.text))

    raw_inventory = first_contact_response.backup.artifacts_db.inventory_items
    raw_artifact_stats = first_contact_response.backup.artifacts_db.artifact_status
    formatted_artifact_stats = parse_api_response(str(raw_artifact_stats))

    # print(str(first_contact_response.backup.contracts.current_coop_statuses)) # this is neat! implement in future!
    raw_inventory = str(raw_inventory).split('\n')

    artifact_key_indices = get_artifact_key_indices(raw_inventory)
    full_inventory = sort_neatly(raw_inventory, artifact_key_indices)
    save(full_inventory, f'{base_dir}{user}_all artifacts.json')

    game_backup = first_contact_response.backup.game
    stats_backup = first_contact_response.backup.stats
    se, pe, eb, ge, scaled_pb = get_stats(game_backup, stats_backup)

    craft_xp = int(first_contact_response.backup.artifacts.crafting_xp)
    multip = get_multiplier(craft_xp)

    last_api_time = int(first_contact_response.backup.approx_time)

    player_info = {"SOUL EGGS": se, "EGGS OF PROPHECY": pe, "RAW EB %": eb,
                   "GOLDEN EGGS": ge, "PIGGY": scaled_pb, "CRAFTING XP": craft_xp, "ODDS MULTTIPLIER": multip}

    mission_times = get_current_missions(str(first_contact_response.backup.artifacts_db.mission_infos))

    for i in range(len(mission_times)):
        player_info[f"Mission {i+1} return"] = mission_times[i]
    
    save(player_info, f'{base_dir}{user}_player info.json')
    return formatted_artifact_stats

def sort_by_name(user: str, formatted_artifact_stats) -> None:

    # format: {"stones": {"T0 PROPHECY STONE FRAGMENT": [qty, value], ...}, "ingredients": {"T1 GOLD METEORITE": [qty, value], ...}, "artifacts": {T1 LIGHT OF EGGENDIL: qty, ...}}

    f = open(f'{base_dir}{user}_all artifacts.json')
    aft_dict = json.load(f)

    g = open(f'{base_dir}prices.json')
    pce_dict = json.load(g)

    quantity_dict = {"stones": {}, "ingredients": {}, "artifacts": {}} # create dictionary with above format

    for stone in stone_types: # fill all stones with defaults
        for i in [0, 1, 2, 3]:
            fragment = ' FRAGMENT' if i == 0 else ''
            stone_name = f'T{i} {stone} STONE{fragment}'
            quantity_dict["stones"][stone_name] = [0, 0, 0]

    for ingredient in ingredient_types: # fill all ingredients with defaults
        for i in [1, 2, 3]:
            ingredient_name = f'T{i} {ingredient}'
            quantity_dict["ingredients"][ingredient_name] = [0, 0, 0]

    for artifact in artifact_types: # fill all artifacts with defaults
        for i in [1, 2, 3, 4]:
            artifact_name = f'T{i} {artifact}'
            quantity_dict["artifacts"][artifact_name] = [0, 0]
        
    for item in aft_dict: # update quantities
        if aft_dict[item][0] == 'stone' or aft_dict[item][0] == 'fragment': # standalone stones
            quantity_dict["stones"][item][0] += aft_dict[item][1]

        if len(aft_dict[item][2]) != 0: # slotted stones
            for slotted_stone in aft_dict[item][2]:
                quantity_dict["stones"][slotted_stone][0] += 1

        if aft_dict[item][0] == 'ingredient': # standalone ingredients
            quantity_dict["ingredients"][item][0] += aft_dict[item][1]

        if aft_dict[item][0] == 'artifact': # artifacts (just quantities, no sort by rarity)
            if item[2] not in ['R', 'E', 'L']: # common
                quantity_dict["artifacts"][item][0] += aft_dict[item][1]
            else: # anything else
                quantity_dict["artifacts"][(item[0:2] + item[3:]).split(' #')[0]][0] += 1
    
    for type in ["stones", "ingredients"]: # update values
        for item in quantity_dict[type]:
            quantity_dict[type][item][1] = quantity_dict[type][item][0] * pce_dict[type][item]
        
    for type in ["stones", "ingredients", "artifacts"]: # fill in craft count
        for item in quantity_dict[type]:
            quantity_dict[type][item][-1] = formatted_artifact_stats[item]["count"]
    
    f.close()
    g.close()
    save(quantity_dict, f'{base_dir}{user}_quantity data.json')

def stat_list(user: str):
    try:
        g = open(f'{base_dir}{user}_player info.json')
        stat_dict = json.load(g)
    except:
        return None

    stats = ''
    for stat in stat_dict:
        if type(stat_dict[stat]) is not list:
            stats = stats + f'{stat:<17}: {stat_dict[stat]}\n'
        else:
            seconds_remaining = stat_dict[stat][0] + stat_dict[stat][1] - int(time.time()) # seconds remaining = (launch + duration) - current
            if seconds_remaining > 0:
                time_string = str(datetime.timedelta(seconds=seconds_remaining))
            else:
                time_string = 'COLLECT ME'
            stats = stats + f'{stat:<17}: {time_string}\n'

    g.close()

    return stats

def make_stone_list(user: str) -> list[tuple[str, str]]:
    try:
        g = open(f'{base_dir}{user}_quantity data.json')
        stones = json.load(g)["stones"]
    except:
        return None

    stone_list = []
    total_items = 0
    total_value = 0
    gold_value = 0
    piggy_value = 0

    for stone in stone_types:
        q_t0 = stones[f'T0 {stone} STONE FRAGMENT'][0]
        q_t1 = stones[f'T1 {stone} STONE'][0]
        q_t2 = stones[f'T2 {stone} STONE'][0]
        q_t3 = stones[f'T3 {stone} STONE'][0]
        q_tot = q_t0 + q_t1 + q_t2 + q_t3

        v_t0 = stones[f'T0 {stone} STONE FRAGMENT'][1]
        v_t1 = stones[f'T1 {stone} STONE'][1]
        v_t2 = stones[f'T2 {stone} STONE'][1]
        v_t3 = stones[f'T3 {stone} STONE'][1]
        v_tot = v_t0 + v_t1 + v_t2 + v_t3

        val_line_1 = f'tier 0 -- Qty: {q_t0} -- Value: {v_t0}\n'
        val_line_2 = f'tier 1 -- Qty: {q_t1} -- Value: {v_t1}\n'
        val_line_3 = f'tier 2 -- Qty: {q_t2} -- Value: {v_t2}\n'
        val_line_4 = f'tier 3 -- Qty: {q_t3} -- Value: {v_t3}'

        stone_list.append((f'{stone} -- Qty: {q_tot} -- Value: {v_tot}', val_line_1 + val_line_2 + val_line_3 + val_line_4))
        total_items += q_tot
        total_value += v_tot
        gold_value += v_tot - v_t0
        piggy_value += v_t0

    stone_list.append((f'TOTAL -- Qty: {total_items} -- Value: {total_value}', f'Gold Value: {gold_value} \n Piggy Value: {piggy_value}'))
    g.close()
    return stone_list

def make_ingredient_list(user: str) -> list[tuple[str, str]]:
    try:
        g = open(f'{base_dir}{user}_quantity data.json')
        ingredients = json.load(g)["ingredients"]
    except:
        return None
    
    ingredient_list = []
    total_items = 0
    total_value = 0

    for ingredient in ingredient_types:
        q_t1 = ingredients[f'T1 {ingredient}'][0]
        q_t2 = ingredients[f'T2 {ingredient}'][0]
        q_t3 = ingredients[f'T3 {ingredient}'][0]
        q_tot = q_t1 + q_t2 + q_t3

        v_t1 = ingredients[f'T1 {ingredient}'][1]
        v_t2 = ingredients[f'T2 {ingredient}'][1]
        v_t3 = ingredients[f'T3 {ingredient}'][1]
        v_tot = v_t1 + v_t2 + v_t3

        val_line_1 = f'tier 1 -- Qty: {q_t1} -- Value: {v_t1}\n'
        val_line_2 = f'tier 2 -- Qty: {q_t2} -- Value: {v_t2}\n'
        val_line_3 = f'tier 3 -- Qty: {q_t3} -- Value: {v_t3}'

        ingredient_list.append((f'{ingredient} -- Qty: {q_tot} -- Value: {v_tot}', val_line_1 + val_line_2 + val_line_3))
        total_items += q_tot
        total_value += v_tot
    
    ingredient_list.append((f'TOTAL -- Qty: {total_items} -- Value: {total_value}', ''))
    g.close()
    return ingredient_list

def make_artifact_list(user: str) -> list[tuple[str, str]]:
    try:
        g = open(f'{base_dir}{user}_quantity data.json')
        artifacts = json.load(g)["artifacts"]
    except:
        return None

    artifact_list = []
    total_items = 0

    for artifact in artifact_types:
        q_t1 = artifacts[f'T1 {artifact}'][0]
        q_t2 = artifacts[f'T2 {artifact}'][0]
        q_t3 = artifacts[f'T3 {artifact}'][0]
        q_t4 = artifacts[f'T4 {artifact}'][0]
        q_tot = q_t1 + q_t2 + q_t3 + q_t4

        val_line_1 = f'tier 1 -- Qty: {q_t1}\n'
        val_line_2 = f'tier 2 -- Qty: {q_t2}\n'
        val_line_3 = f'tier 3 -- Qty: {q_t3}\n'
        val_line_4 = f'tier 4 -- Qty: {q_t4}'

        artifact_list.append((f'{artifact} -- Qty: {q_tot}', val_line_1 + val_line_2 + val_line_3 + val_line_4))
        total_items += q_tot

    artifact_list.append((f'TOTAL -- Qty: {total_items}', ''))
    g.close()
    return artifact_list

def create_archive_entry(user: str, time_index: str) -> int:
    entry = {}
    if os.path.isfile(f'{base_dir}archives//{user}_history.json'):
        g = open(f'{base_dir}archives//{user}_history.json')
        history = json.load(g)
    else:
        save({}, f'{base_dir}archives//{user}_history.json')
        g = open(f'{base_dir}archives//{user}_history.json')
        history = json.load(g)

    if not os.path.isfile(f'{base_dir}{user}_quantity data.json'):
        return 1

    ##### build artifact entry (do later)
    
    ##### build stone entry
    s = open(f'{base_dir}{user}_quantity data.json')
    stuff = json.load(s)

    for stone_type in stone_types:
        for tier in [0, 1, 2, 3]:
            index = f'T{tier} {stone_type} STONE FRAGMENT' if tier == 0 else f'T{tier} {stone_type} STONE'
            entry[index] = stuff["stones"][index][0]

    ##### build ingredient entry
    for ingredient_type in ingredient_types:
        for tier in [1, 2, 3]:
            index = f'T{tier} {ingredient_type}'
            entry[index] = stuff["ingredients"][index][0]

    s.close()

    history[time_index] = entry
    g.close()
    save(history, f'{base_dir}archives//{user}_history.json')
    return 0

def legendary_list(user: str):
    try:
        g = open(f'{base_dir}{user}_all artifacts.json')
        aft_dict = json.load(g)
    except:
        return None, None

    found_legs = []
    for item in aft_dict:
        if item[2] == 'L':
            found_legs.append(item)

    legendary_total = ''
    total = 0
    for legendary in legendary_types:
        amount = 0
        for found_leg in found_legs:
            if legendary in found_leg:
                amount += 1
        legendary_total = legendary_total + f'{legendary:<25}: {amount:<2} {"✅" if amount > 0 else "❌"}\n'
        total += amount

    g.close()

    return legendary_total, total

def shiny_list(user: str, tier: str):
    try:
        g = open(f'{base_dir}{user}_all artifacts.json')
        aft_dict = json.load(g)
    except:
        return None
    
    rares = []
    epics = []
    legs = []

    for item in aft_dict:
        if item[:3] == f'{tier}R':
            rares.append(item)
        elif item[:3] == f'{tier}E':
            epics.append(item)
        elif item[:3] == f'{tier}L':
            legs.append(item)

    shiny_list = f'     ARTIFACTS       | Rare | Epic | Legs'
    shiny_list = shiny_list + '\n\n'

    h = open(f'{base_dir}shinies.json')
    shiny_dict = json.load(h)

    not_avail = '---'
    not_have = 'NONE'

    for artifact in artifact_types:
        q_r = 0 if 'R' in shiny_dict[tier][artifact] else not_avail
        q_e = 0 if 'E' in shiny_dict[tier][artifact] else not_avail
        q_l = 0 if 'L' in shiny_dict[tier][artifact] else not_avail

        for item in rares:
            if artifact in item:
                q_r += 1

        for item in epics:
            if artifact in item:
                q_e += 1

        for item in legs:
            if artifact in item:
                q_l += 1

        c1 = True if (isinstance(q_r, int) and q_r > 0) or q_r == not_avail else False
        c2 = True if (isinstance(q_e, int) and q_e > 0) or q_e == not_avail else False
        c3 = True if (isinstance(q_l, int) and q_l > 0) or q_l == not_avail else False

        fill_1 = f'{q_r:^4}' if c1 else f'{not_have:^4}'
        fill_2 = f'{q_e:^4}' if c2 else f'{not_have:^4}'
        fill_3 = f'{q_l:^4}' if c3 else f'{not_have:^4}'

        shiny_list = shiny_list + f'{artifact:<21}: {fill_1} | {fill_2} | {fill_3}\n'

    g.close()
    h.close()
    return shiny_list

def get_llc(id: str) -> str:
    url = f'https://eggincdatacollection.azurewebsites.net/api/formulae/llc?eid={id}'
    response = requests.get(url)
    #print(response.status_code)
    #print(response.text)
    return response.text

def check_valid_artifact(artifact: str) -> bool:
    valid = False
    for ingredient in ingredient_types:
        if ingredient in artifact:
            if artifact[:2] in ['T1', 'T2', 'T3']:
                valid = True

    for stone in stone_types:
        if stone in artifact:
            if artifact[:2] in ['T1', 'T2', 'T3']:
                valid = True
            if artifact[:2] == 'T0' and 'FRAGMENT' in artifact:
                valid = True

    return valid

def verify_prereqs(user: str) -> tuple[bool, str | None]:
    met = False
    other = None
    with open('C://Desktop//Discord Bot//bot_data//egg_inc_data//ei_registered_ids.json', 'r') as f:
        ids = json.load(f)
        if user in ids:
            met = True
            other = ids[user]
    return met, other

def craft(artifact: str, user: str):
    with open(f'C://Desktop//Discord Bot//bot_data//egg_inc_data//{user}_quantity data.json') as f:
        quantity_data = json.load(f)
    with open('C://Desktop//Discord Bot//bot_data//egg_inc_data//crafting_tree.json') as f2:
        crafting_tree = json.load(f2)

    if artifact not in crafting_tree:
        return None, None
    
    full_tree = []
    def find(artifact: str, rec_mult: int, depth: int, prev_path: str, full_tree: list[tuple[str, str, int, int]]) -> list[tuple[str, str, int, int]]:
        needed_artifacts = [need for need in crafting_tree[artifact]]
        quantities = [crafting_tree[artifact][need] for need in needed_artifacts]
        rec_quantities = [rec_mult * crafting_tree[artifact][need] for need in needed_artifacts]
        paths = [prev_path + f'{depth}{["L","R"][quantities.index(amount)]}' for amount in quantities]
        for i in range(len(paths)):
            full_tree.append((paths[i], needed_artifacts[i], quantities[i], rec_quantities[i]))

        for i in range(len(paths)):
            if needed_artifacts[i] in crafting_tree:
                full_tree = find(needed_artifacts[i], rec_quantities[i], depth+1, paths[i], full_tree)

        return full_tree

    full_tree = find(artifact, 1, 1, '', full_tree)
    paths, needed, quantities, rec_quantities = zip(*full_tree)

    available = {}
    for need in needed:
        if need not in available:
            if need in quantity_data['stones']:
                available[need] = quantity_data['stones'][need][0]
            elif need in quantity_data['ingredients']:
                available[need] = quantity_data['ingredients'][need][0]
            else:
                available[need] = quantity_data['artifacts'][need]

    # start off by calculating with proportional distribution and show remainders
    # if remainders exist, "uncraft" and transfer remainder materials to other side if needed
    # craft again
    # hope it works
    return full_tree, available

def legendary_odds(user: str, qty: int) -> str:
    # read the clrafing multiplier:
    with open(f'{base_dir}{user}_player info.json') as statfile:
        stat_dict = json.load(statfile)
        multiplier = stat_dict["ODDS MULTTIPLIER"]

    with open(f'{base_dir}{user}_quantity data.json') as quantities:
        artifact_dict = json.load(quantities)["artifacts"]

    def calculate_chance(const, mult, crafts):
        chance = min(const, min(0.1, (max(10.,const/mult))**(0.3*min(1., crafts/400.) - 1.)))
        return chance
    
    def calc_group_chance(start, crafts, const, mult):
        N = crafts
        
        fail0 = 1
        for i in range(0, N):
            fail0 *= (1.0 - calculate_chance(const, mult, start + i))
        return 1 - fail0
    
    probs = {}
    probability = ''
    
    for artifact in legendary_base:
        const = legendary_base[artifact]
        crafted = artifact_dict[f"{artifact[0:2]} {artifact[4:]}"][1]
        chance = round(100*calc_group_chance(crafted, qty, const, multiplier),4) # const, multiplier, crafted
        probs[artifact] = chance
        probability = probability + f'{artifact:<25}: {chance:<6} %\n'
        

    return probability
