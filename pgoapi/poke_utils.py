import os


def pokemon_iv_percentage(pokemon):
    return ((pokemon.get('individual_attack', 0) + pokemon.get('individual_stamina', 0) + pokemon.get(
        'individual_defense', 0) + 0.0) / 45.0) * 100.0


def get_pokemon_num(res):
    inventory_delta = res['responses']['GET_INVENTORY'].get('inventory_delta', {})
    inventory_items = inventory_delta.get('inventory_items', [])
    inventory_items_dict_list = map(lambda x: x.get('inventory_item_data', {}), inventory_items)
    inventory_items_pokemon_list = filter(lambda x: 'pokemon_data' in x and 'is_egg' not in x['pokemon_data'], inventory_items_dict_list)
    return len(inventory_items_pokemon_list)


def get_inventory_data(res, poke_names):
    inventory_delta = res['responses']['GET_INVENTORY'].get('inventory_delta', {})
    inventory_items = inventory_delta.get('inventory_items', [])
    inventory_items_dict_list = map(lambda x: x.get('inventory_item_data', {}), inventory_items)
    inventory_items_pokemon_list = filter(lambda x: 'pokemon_data' in x and 'is_egg' not in x['pokemon_data'],
                                          inventory_items_dict_list)
    inventory_items_pokemon_list_sorted = sorted(inventory_items_pokemon_list, key=lambda x: poke_names[str(x['pokemon_data']['pokemon_id'])].encode('ascii', 'ignore'))

    inventory_items_pokemon_list_sorted = sorted(
        inventory_items_pokemon_list,
        key=lambda pokemon: pokemon['pokemon_data']['cp']
    )

    pk_list = "\n" # formating to make the pokemon list more readable
    i = 0
    for x in inventory_items_pokemon_list_sorted:
        r = "{0} CP:{1} IV:{2:.2f}".format(poke_names[str(x['pokemon_data']['pokemon_id'])].encode('ascii', 'ignore'), x['pokemon_data']['cp'], pokemon_iv_percentage(x['pokemon_data']))
        i += 1
        if i % 3 == 0:
            pk_list += "{0: <30}\n".format(r)
        else:
            pk_list += "{0: <30}".format(r)
    return pk_list


def get_incubators_stat(res):
    inventory_delta = res['responses']['GET_INVENTORY'].get('inventory_delta', {})
    inventory_items = inventory_delta.get('inventory_items', [])
    inventory_items_dict_list = map(lambda x: x.get('inventory_item_data', {}), inventory_items)
    inventory_items_incubators = map(lambda x: x.get('egg_incubators', {}).get('egg_incubator', {}), inventory_items_dict_list)
    inventory_items_incubator_list = reduce(lambda x, y: x + y, filter(lambda x: len(x) > 0, inventory_items_incubators))
    player_stats = filter(lambda x: len(x) > 0, map(lambda x: x.get('player_stats', {}), inventory_items_dict_list))
    if len(player_stats) > 0:
        km_walked = player_stats[0].get('km_walked', 'None')
    else:
        km_walked = 'None'
    if inventory_items_incubator_list:
        return (os.linesep.join(map(lambda x: "Incubator {0:.2f} km, walked {1:.2f} km".format(
            x['target_km_walked'],
            km_walked), inventory_items_incubator_list)))
    else:
        return 'No incubators'
