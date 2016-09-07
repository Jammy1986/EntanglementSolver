import collections
import math
import time
from Common.seleniummanager import SeleniumManager


def wrap_to_legal_range(input_position):
    if input_position > 11:
        return input_position - 12
    if input_position < 0:
        return input_position + 12
    return input_position


def partner(input_position, options):
    index = options.index(input_position)
    if index % 2 == 0:
        return options[index + 1]
    return options[index - 1]


def partners(input_position, options):
    result = []
    for i in range(0, 12, 2):
        result.append(partner(wrap_to_legal_range(input_position + i), options))
    return result


Hex = collections.namedtuple("Hex", ["q", "r", "s"])


def hex_add(a, b):
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)


def hex_subtract(a, b):
    return Hex(a.q - b.q, a.r - b.r, a.s - b.s)


def hex_scale(a, k):
    return Hex(a.q * k, a.r * k, a.s * k)


# Up, up to the right, down to the right, down, down to the left, up to the left.
hex_directions = [Hex(0, -1, 1), Hex(1, -1, 0), Hex(1, 0, -1), Hex(0, 1, -1), Hex(-1, 1, 0), Hex(-1, 0, 1)]


def hex_direction(direction):
    return hex_directions[direction]


def hex_neighbor(hexagon, direction):
    return hex_add(hexagon, hex_direction(direction))


def create_map(map_radius):
    hex_map = {}
    for q in range(-map_radius, map_radius + 1):
        r1 = max(-map_radius, -q - map_radius)
        r2 = min(map_radius, -q + map_radius)
        for r in range(r1, r2 + 1):
            hex_map[Hex(q, r, -q - r)] = []
    hex_map[Hex(0, 0, 0)] = None
    return hex_map


def next_cell_position(x):
    return {
        0: 7,
        1: 6,
        2: 9,
        3: 8,
        4: 11,
        5: 10,
        6: 1,
        7: 0,
        8: 3,
        9: 2,
        10: 5,
        11: 4
    }[x]


def count_empty_tiles(map):
    count = 0
    for tile in map:
        if tile is []:
            count += 1
    return count


def follow_path(map, start_location, hex_position):
    score = 0
    current_location = start_location
    current_hex = hex_position
    multiplier = 1
    while map.get(current_hex, None):
        output_location = partner(current_location, map[current_hex])
        current_location = next_cell_position(output_location)
        current_hex = hex_neighbor(current_hex, math.floor(output_location / 2))
        score += multiplier
        multiplier += 1
    return score, current_location, current_hex


def brute_force(map, hex_position, entry_location, current_tile, swap_tile, tile_stack):
    highest_score = 0
    next_tile = tile_stack.pop(0)
    best_placement = []
    for tile, backup_tile in [(current_tile, swap_tile), (swap_tile, current_tile)]:
        for rotation, partner in enumerate(partners(entry_location, tile)):
            map[hex_position] = [wrap_to_legal_range(i + 2 * rotation) for i in tile]
            added_score, new_position, new_hex = follow_path(map, entry_location, hex_position)
            iteration_placement = [(rotation, "normal" if tile == current_tile else "swap")]
            if map.get(new_hex, None) is None:
                iteration_score = added_score
            else:
                highest_score_result, best_placement_result = brute_force(map, new_hex, new_position, next_tile, backup_tile, tile_stack)
                iteration_score = highest_score_result + added_score
                iteration_placement.extend(best_placement_result)
            if iteration_score > highest_score:
                highest_score = iteration_score
                best_placement = iteration_placement
            map[hex_position] = []
            # Uncomment the following two lines to see sample output.
            # if highest_score > 150:
            #     return highest_score, best_placement
    tile_stack.insert(0, next_tile)
    return highest_score, best_placement


if __name__ == '__main__':
    map = create_map(3)
    with SeleniumManager() as selenium_manager:
        tiles, start_tile, swap_tile = selenium_manager.get_tiles()
        highest_score, best_placement = brute_force(map, hex_direction(0), 7, start_tile, swap_tile, tiles)
        print(highest_score)
        for rotation, tile in best_placement:
            if tile is "swap":
                selenium_manager.swap_tile()
            selenium_manager.rotate(rotation)
            selenium_manager.place()
        time.sleep(10)
