import turtle
import math
from deep_translator import GoogleTranslator
import random
import webcolors
import ru_local as ru

def get_color_choice() -> str:
    
    """
    Function to get user's color choice with validation
    Returns:
        color (str): Chosen color as a string
    """

    available_colors = {
        "1": "red", "2": "blue", "3": "green", "4": "yellow",
        "5": "purple", "6": "cyan", "7": "turquoise", "8": "magenta",
        "9": "pink", "10": "orange", "11": "brown", "12": "custom"
    }

    print(ru.AVAILABLE_COLORS)
    print(ru.COLOR_OPTIONS_1)
    print(ru.COLOR_OPTIONS_2)
    print(ru.COLOR_OPTIONS_3)
    print(ru.COLOR_OPTIONS_4)
    print(ru.COLOR_OPTIONS_5)
    print(ru.COLOR_OPTIONS_6)
    print(ru.COLOR_PROMPT, end="")

    while True:
        choice = input().strip()

        if choice in available_colors:
            if choice == "12":
                return get_custom_color_input()
            else:
                return available_colors[choice]
        else:
            print(f"'{choice}' {ru.INVALID_COLOR_MESSAGE}", end="")


def get_custom_color_input() -> str:

    """
    Function to get custom color input from user with validation using Turtle
    Returns:
        custom_color (str): Validated custom color as a string
    """

    print(ru.CUSTOM_COLOR_PROMPT, end="")

    while True:
        custom_color = input().strip()

        if custom_color.startswith("#") and len(custom_color) == 7:
            try:
                int(custom_color[1:], 16)
                return custom_color
            except ValueError:
                print(f"'{custom_color}' {ru.INVALID_HEX_MESSAGE}", end="")

        custom_color = custom_color.lower()
        translated = GoogleTranslator().translate(custom_color)
        try:
            test_turtle = turtle.Turtle()
            test_turtle.color(translated)
            test_turtle.hideturtle()
            test_turtle.clear()
            return translated
        except turtle.TurtleGraphicsError:
            print(f"'{custom_color}' {ru.INVALID_COLOR_MESSAGE}", end="")


def get_num_hexagons() -> int:

    """
    Function to get number of hexagons with validation
    Returns:
        n (int): Number of hexagons in a row
    """

    print(ru.NUM_HEXAGONS_PROMPT, end="")

    while True:
        user_input = input().strip()

        try:
            n = int(user_input)

            if 4 <= n <= 20:
                return n
            else:
                print(ru.INVALID_NUMBER_MESSAGE_1, end="")
        except ValueError:
            print(f"'{user_input}' {ru.INVALID_NUMBER_MESSAGE_2}", end="")


def display_welcome_message() -> None:

    """
    Function to display welcome message and instructions
    """

    print(ru.WELCOME_MESSAGE)


def calculate_side_length(n: int, canvas_size: int) -> float:

    """
    Evaluates the maximum possible side length of N x N hexagons that can fit within a square canvas of given size. 
    Args:
        n (int): Number of hexagons along one side of the square grid.
        canvas_size (int): Size of the square canvas (width and height).
    Returns:
        side (float): Maximum side length of the hexagons.
    """           

    max_side_by_width = canvas_size / (math.sqrt(3) * (n + 0.5))
    max_side_by_height = canvas_size / (1.5 * n + 0.5)

    side = min(max_side_by_width, max_side_by_height)

    return side


def calculate_hexagon_centers(n: int, canvas_size: int) -> list:

    """
    Calculates the centers of N x N hexagons arranged in a grid within a square canvas.
    Args:
        n (int): Number of hexagons along one side of the square grid.
        canvas_size (int): Size of the square canvas (width and height).
    Returns:
        centers (list): List of tuples representing the (x, y) coordinates of the hexagon centers.
    """

    side = calculate_side_length(n, canvas_size)

    w = math.sqrt(3) * side    
    v = 1.5 * side           

    max_center_x = w * (n - 0.5)  
    center_of_centers_x = max_center_x / 2

    max_center_y = v * (n - 1)
    center_of_centers_y = max_center_y / 2

    unoptimized_centers = []
    for r in range(n):
        row_offset = (r % 2) * (w / 2)
        for c in range(n):
            x_un = c * w + row_offset
            y_un = r * v
            x = x_un - center_of_centers_x
            y = y_un - center_of_centers_y
            unoptimized_centers.append((x, y))

    centers = []
    for (x, y) in unoptimized_centers:
        x = round(x * 2) / 2
        y = round(y * 2) / 2
        centers.append((x, y))

    print(centers)

    return centers


def name_to_hex(name: str) -> str:

    """
    Converts a color name to its HEX representation.
    Args:
        name (str): Color name
    Returns:
        hex (str): HEX representation of the color
    """

    return webcolors.name_to_hex(name)


def hex_to_ints(hexstr: str) -> tuple:

    """
    Converts a HEX color string to its RGB components.
    Args:
        hexstr (str): HEX color string
    Returns:
        tuple(int, int, int): RGB components
    """

    s = hexstr.lstrip("#")
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return (r, g, b)


def ints_to_hex(r: int, g: int, b: int) -> str:

    """
    Converts RGB components to a HEX color string.
    Args:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
    Returns:
        hex (str): HEX color string
    """

    ri = max(0, min(255, int(round(r))))
    gi = max(0, min(255, int(round(g))))
    bi = max(0, min(255, int(round(b))))
    return f"#{ri:02X}{gi:02X}{bi:02X}"


def interpolate_hex(color1_hex: str, color2_hex: str, t: float) -> str:

    """
    Interpolates between two HEX colors.
    Args:
        color1_hex (str): First HEX color  
        color2_hex (str): Second HEX color
        t (float): Interpolation factor (0.0 to 1.0)
    Returns:
        str: Interpolated HEX color
    """

    r1, g1, b1 = hex_to_ints(color1_hex)
    r2, g2, b2 = hex_to_ints(color2_hex)
    r = r1 + (r2 - r1) * t
    g = g1 + (g2 - g1) * t
    b = b1 + (b2 - b1) * t
    return ints_to_hex(r, g, b)


def choose_coloring_mode() -> str:

    """
    Chooses the coloring mode for the hexagon grid.
    Returns:
        mode (str): Chosen coloring mode
    """

    modes = {
        "1": ru.CLASSIC_MODE,
        "2": ru.VERTICAL_GRADIENT_MODE,
        "3": ru.HORIZONTAL_GRADIENT_MODE,
        "4": ru.RANDOM_MODE
    }

    print(ru.AVAILABLE_MODES)
    for key, value in modes.items():
        print(f"{key}. {value}")

    print(ru.CHOOSE_COLORING_MODE, end="")
    while True:
        mode = input().strip()
        if mode in modes:
            return mode
        else:
            print(ru.INVALID_NUMBER_MESSAGE_3, end="")


def get_classic_color(row: int, col: int, color1_hex: str, color2_hex: str) -> str:

    """
    Gets the color for a specific hexagon in classic mode.
    Args:
        row (int): Row index
        col (int): Column index
        color1_hex (str): First HEX color
        color2_hex (str): Second HEX color
    Returns:
        str: HEX color for the hexagon
    """

    if (row + col) % 2 == 0:
        return color1_hex
    return color2_hex


def get_vertical_gradient_color(row: int, n: int, color1_hex: str, color2_hex: str) -> str:

    """
    Gets the color for a specific hexagon in vertical gradient mode.
    Args:
        row (int): Row index
        n (int): Total number of rows
        color1_hex (str): First HEX color
        color2_hex (str): Second HEX color
    Returns:
        str: HEX color for the hexagon
    """

    progress = row / (n - 1) if n > 1 else 0
    return interpolate_hex(color1_hex, color2_hex, progress)


def get_horizontal_gradient_color(col: int, n: int, color1_hex: str, color2_hex: str) -> str:

    """
    Gets the color for a specific hexagon in horizontal gradient mode.
    Args:
        col (int): Column index
        n (int): Total number of columns
        color1_hex (str): First HEX color
        color2_hex (str): Second HEX color
    Returns:
        str: HEX color for the hexagon
    """

    progress = col / (n - 1) if n > 1 else 0
    return interpolate_hex(color1_hex, color2_hex, progress)


def get_random_color(color1_hex: str, color2_hex: str) -> str:

    """
    Gets a random color for a specific hexagon in random mode.
    Args:
        color1_hex (str): First HEX color
        color2_hex (str): Second HEX color
    Returns:
        str: HEX color for the hexagon
    """

    return random.choice([color1_hex, color2_hex])


def draw_hexagon(center: tuple, color: str, side_length: float) -> None:
    
    """
    Animated drawing of a single hexagon with 3D effect.
    Args:
        center (tuple): (x, y) coordinates of the hexagon center
        color (str): Color of the hexagon in HEX format
        side_length (float): Length of the hexagon side
    """
    
    x, y = center
    
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    
    r = int(r * 0.7)
    g = int(g * 0.7) 
    b = int(b * 0.7)
    
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    shadow_color = f'#{r:02x}{g:02x}{b:02x}'
    
    t = turtle.Turtle() 
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color("black", color)
    t.begin_fill()
    
    t.left(30)
    
    for _ in range(6):
        t.forward(side_length)
        t.left(60)
    
    t.end_fill()

    shadow_t = turtle.Turtle()
    shadow_t.penup()
    shadow_t.goto(x, y)
    shadow_t.pendown()
    shadow_t.color(shadow_color)
    shadow_t.pensize(2)

    shadow_t.left(30)
    
    for j in range(3):
        shadow_t.forward(side_length)
        shadow_t.left(60)
    
    shadow_t.hideturtle()
    
    border_t = turtle.Turtle()
    border_t.penup()
    border_t.goto(x, y)
    border_t.pendown()
    border_t.color("black")
    border_t.pensize(1)
    
    border_t.left(30)
    
    for _ in range(6):
        border_t.forward(side_length)
        border_t.left(60)
    
    border_t.hideturtle()
    t.hideturtle()


def main() -> None:

    """
    Main function to run the hexagon art generator.
    """

    display_welcome_message()
    n = get_num_hexagons()
    color1_name = get_color_choice()
    color2_name = get_color_choice()
    mode = choose_coloring_mode()

    color1_hex = name_to_hex(color1_name)
    color2_hex = name_to_hex(color2_name)

    canvas_size = 500
    centers = calculate_hexagon_centers(n, canvas_size)
    side_length = calculate_side_length(n, canvas_size)

    screen = turtle.Screen()
    screen.setup(canvas_size, canvas_size)
    screen.title(ru.WELCOME_MESSAGE)
    screen.tracer(0, 0)
    
    for index, (x, y) in enumerate(centers):
        row = index // n
        col = index % n

        if mode == "1":
            fill_color = get_classic_color(row, col, color1_hex, color2_hex)
        elif mode == "2":
            fill_color = get_vertical_gradient_color(row, n, color1_hex, color2_hex)
        elif mode == "3":
            fill_color = get_horizontal_gradient_color(col, n, color1_hex, color2_hex)
        elif mode == "4":
            fill_color = get_random_color(color1_hex, color2_hex)

        draw_hexagon((x, y), fill_color, side_length)
        
    turtle.update()
    turtle.hideturtle()
    turtle.exitonclick()


if __name__ == "__main__":
    main()



