def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)

    return tuple(rgb)

def rgb_to_hex(rgb):
    for i in range(len(rgb)):
        rgb[i] = int(rgb[i])
    return '%02x%02x%02x' % tuple(rgb)

def adjacents(sequence, circular=False):
    adjacents = []

    if not sequence:
        return None

    for i in range(len(sequence) - 1):
        adjacents.append([sequence[i], sequence[i+1]])

    if circular:
        adjacents.append([sequence[-1], sequence[0]])

    return adjacents

