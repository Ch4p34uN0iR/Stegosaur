"""
Text-to-Image steganography tool.
Created by Chris Phippen
"""


def write_image(txt_name="text.txt", image_name="image.png", repeat=True):

    """
    Takes text from file and uses steganography to hide it within an image.
    :param txt_name: Name of the txt file.
    :param image_name: Name of image file.
    :param repeat: Write text binary multiple times, or end after one iteration.
    :return: None.
    """

    from sys import exit

    # Saves needless importing in programs that already use PIL
    try:
        Image
    except NameError:

        try:
            from PIL import Image
        except ModuleNotFoundError:
            exit("Please install PIL or Pillow.")

    bin_gen = bin_generator(txt_name)
    image_file = Image.open(image_name).convert("RGBA")

    im_width, im_height = image_file.size

    for x in range(im_width):
        for y in range(im_height):

            # Get RGBA values for the pixel
            rgba = image_file.getpixel((x, y))
            new_rgba = []
            for channel in rgba:

                # Do we have more text to write
                try:
                    txt_temp = next(bin_gen)
                except StopIteration:
                    if not repeat:
                        break

                chn_temp = format(channel, "08b")[:6] + txt_temp
                new_rgba.append(int(chn_temp, 2))

            # Deals with case wherein not all channels need editing.
            for i in range(len(new_rgba), 4):
                new_rgba.append(rgba[i])

            new_rgba = tuple(new_rgba)
            image_file.putpixel((x, y), new_rgba)

    image_file.save(image_name)


def bin_generator(txt_name):

    """
    Generator of bit pairs to be added to a pixel channel.
    :param txt_name: Name of txt file.
    :return: None.
    """

    txt_file = open(txt_name)

    for line in txt_file:
        for char in line:
            # Formats the character's ascii number into 8-bit binary.
            cur_bin = format(ord(char), "08b")

            for x in range(4):
                yield cur_bin[x: x + 2]

    txt_file.close()


if __name__ == "__main__":
    write_image(repeat=False)
