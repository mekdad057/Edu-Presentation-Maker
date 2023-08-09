import logging

CONTENT_PLACEHOLDER_IDX = 13
DEFAULT_BULLET_POINT_FONT_SIZE = 18
NUM_OF_LINES_PER_SLIDE = 10


def replace_with_image(img, shape, slide):
    """
    replaces the shape with an image and make sure it's not cropped
    and resized properly
    :param img: path of the image
    :param shape: the shape which the image will be inserted into,
     usually it's a placeholder.
    :param slide: the current slide the image will be inserted in.
    :return:
    """
    pic = slide.shapes.add_picture(img, shape.left, shape.top)

    # calculate max width/height for target size
    ratio = min(shape.width / float(pic.width), shape.height / float(pic.height))

    pic.height = int(pic.height * ratio)
    pic.width = int(pic.width * ratio)

    pic.left = int(shape.left + ((shape.width - pic.width) / 2))
    pic.top = int(shape.top + ((shape.height - pic.height) / 2))

    placeholder = shape.element
    placeholder.getparent().remove(placeholder)


def estimate_line_count(shape):
    """
    Estimate the number of lines the text will take inside the shape.
    """
    if shape is None:
        logging.warning("shape passed to 'estimate_line_count' is NONE")
        return 0
    # Get the width of the shape
    shape_width = shape.width

    # Initialize variables
    lines = 0

    # Iterate over each paragraph
    text_frame = shape.text_frame
    for paragraph in text_frame.paragraphs:
        # Initialize variables for this paragraph
        # indentation value 2 tabs for the bullet point
        chars_in_line = 8*paragraph.level

        # Iterate over each run in the paragraph
        for run in paragraph.runs:
            # Get the font size
            font_size = run.font.size or DEFAULT_BULLET_POINT_FONT_SIZE

            # Estimate the width of a character
            char_width = font_size / 1.5  # This is an approximation, actual width may vary based on the font

            # Calculate the number of characters that can fit in a line
            chars_per_line = shape_width / char_width

            # Check if the run fits in the current line
            if chars_in_line + len(run.text) > chars_per_line:
                # If it doesn't fit, calculate how many new lines are needed
                chars_over = (chars_in_line + len(run.text)) - chars_per_line
                new_lines = chars_over // chars_per_line + (chars_over % chars_per_line > 0)
                lines += new_lines
                chars_in_line = chars_over % chars_per_line
            else:
                # If it fits, add the run to the current line
                chars_in_line += len(run.text)

        # Each paragraph is a new line
        lines += 2
    return lines
