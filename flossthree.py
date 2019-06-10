#!/usr/bin/env python

import argparse
from PIL import Image

import pattern

def main():
    parser = argparse.ArgumentParser(description='''
        Convert a pixel art image to a cross-stitch charg
    ''')
    parser.add_argument(
        '-p',
        '--picture',
        metavar='Pixellated Image File',
        required=True,
        help='Enter path to image; max size is 150x150 pixels'
    )
    parser.add_argument(
        '-s',
        '--style',
        metavar='Render style',
        required=False,
        help='options are print or default'
    )
    parser.add_argument(
        '-f',
        '--force_size',
        metavar='Force a larger size',
        required=False,
        help='careful with this one'
    )
    args = parser.parse_args()
    if args.style != 'print' and args.style != 'default':
        parser.print_help()
        return 1

    im = Image.open(args.picture)
    if not im:
        print("Danger danger")
    image_size = im.size
    if (image_size[0] > 150 or image_size[1] > 150) and not args.force_size:
        parser.print_help()
        return 1
    else:
        make_chart(im, args.style)

def make_chart(image, style):
    my_pattern = pattern.Pattern(image, 'dmcfloss')
    my_pattern.build_pattern()
    my_pattern.render_chart(style)
    return


if __name__ == '__main__':
    main()
