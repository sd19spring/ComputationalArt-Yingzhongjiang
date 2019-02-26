"""
MP2
@author: Anne Jiang
"""

import random
import math
from PIL import Image

def prod(a,b):
    return a*b
def avg(a,b):
    return 0.5*(a+b)
def cos_pi(a):
    return math.cos(math.pi*a)
def sin_pi(a):
    return math.sin(math.pi*a)
def x(a,b):
    return a
def y (a,b):
    return b
def squared(a):
    return a**2
def root(a):
    return a**(0.5)


def build_random_function(min_depth, max_depth):
    """Build a random function.

    Builds a random function of depth at least min_depth and depth at most
    max_depth. (See the assignment write-up for the definition of depth
    in this context)

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
        (See the assignment writ-eup for details on the representation of
        these functions)
    """
    #creating elements that will be used within functoin
    listt=[]
    elements_one= ["cos_pi", "root", "sin_pi", "prod", "avg", "squared"]
        # put all buiding blocks into one list to fiddle with
    platypus=random.randint(0, len(elements_one)-1)

    #basecase
    if max_depth <= 1 or min_depth <=1:
        options = [["x"],["y"]]
        index = random.randint (0,1)
        return options[index]

    #not base case scenarios, and elaborates elements within elements_one
    else:
        #create two if statements. one if statement for content that require one value as input
        #and other if statement for content that require two values as input

        if elements_one[platypus]=="cos_pi" or elements_one[platypus]=="sin_pi"or elements_one[platypus]=="squared" or elements_one[platypus]=="root":
            listt.append(elements_one[platypus])
            listt.append(build_random_function(min_depth-1, max_depth-1))

        if elements_one[platypus]=="prod" or elements_one[platypus]=="avg":
            listt.append(elements_one[platypus])
            listt.append(build_random_function(min_depth-1, max_depth-1))
            listt.append(build_random_function(min_depth-1, max_depth-1))
    #return newly appended list called listt
    return listt



def evaluate_random_function(f, x, y):
    """Evaluate the random function f with inputs x,y.
    The representation of the function f is defined in the assignment write-up.
    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
    Returns:
        The function value

    Examples:
        >>> evaluate_random_function(["x"],-0.5, 0.75)

        for a in range(1):
            return random.randint(min_depth, max_depth)
        #min_depth specifies minimum amount of nesting in function-0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    #basecase
    if f[0] == "x":
        return x
    elif f[0] =="y":
        return y
    #afer basecase
    elif f[0] == "prod":
        return evaluate_random_function(f[1],x,y)*evaluate_random_function(f[2], x,y)
    elif f[0]=="avg":
        return (evaluate_random_function(f[1],x,y)+evaluate_random_function(f[2],x,y))/2
    elif f[0]=="cos_pi":
        return math.cos(math.pi*evaluate_random_function(f[1], x, y))
    elif f[0]=="sin_pi":
        return math.cos(math.pi*evaluate_random_function(f[1],x,y))
    elif f[0]=="squared":
        return evaluate_random_function(f[1],x,y)**2
    elif f[0]=="root":
        return evaluate_random_function(f[1],x,y)**(1/2)
    else:
        return "input error"


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values

    Returns:
        The value remapped from the input to the output interval

    Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # return val-input_interval_start)*((output_interval_end-output_interval_start)/(input_interval_end-input_interval_start))+output_interval_start

    # x=(input_interval_end)-(val)
    # r=(output_interval_end-output_interval_start)/(input_interval_end-input_interval_start)
    # e=output_interval_end-r*x
    # return e

    # a=(input_interval_end)-(val)
    # r= ((output_interval_end)-(output_interval_start))/((input_interval_end)-(input_interval_start))
    # e= (output_interval_end)-r * x
    # return e

    inn= (float) (input_interval_end-input_interval_start)
    outt=(float) (output_interval_end-output_interval_start)
    remapp=(val-input_interval_end)*(float) (outt/inn)+output_interval_end
    return remapp
    #thank you Katie for helping me create a remap function that my computer would actually accept! (I guess my computer is picky)

def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]

    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """Generate a test image with random pixels and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel
    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    # red_function = ["x"]
    # green_function = ["y"]
    # blue_function = ["x"]
    red_function = build_random_function(2,9)
    green_function = build_random_function(7,9)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
            )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("art.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
