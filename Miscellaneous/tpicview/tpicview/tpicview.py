#!/usr/bin/env python3
# Copyright (C) 2018 t-r-a-g-e-d-y
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import itertools
import shutil
import time

import PIL.Image
from PIL import Image

def image_to_ansi(image, scale=1.0, sample_method='average'):
    '''
    :param image: PIL Image
    :param scale: scale factor
    :param sample_method: `point` or `average`
    '''
    x_step = 2
    y_step = x_step * 2

    # magic number so that images at 1.0 scale render
    # close to real size based on 10pt monospace font
    magic_scale = x_step / 7

    new_width = int(image.width*magic_scale*scale)
    new_height = int(image.height*magic_scale*scale)

    image = image.resize((new_width, new_height))

    if image.mode != 'RGB':
        image = image.convert('RGB')

    width, height = image.size
    ansi_image = ''

    color_code = '\033[38;2;{};{};{}m\033[48;2;{};{};{}m▀'

    pixels = image.getdata()

    for y in range(0, height-y_step, y_step):
        for x in range(0, width-x_step, x_step):
            if sample_method == 'average':
                top_pxls = [pixels[_y*width+_x]
                            for _y in range(y, y+y_step//2)
                            for _x in range(x, x+x_step)]

                bot_pxls = [pixels[_y*width+_x]
                            for _y in range(y+y_step//2, y+y_step)
                            for _x in range(x, x+x_step)]

                top_px = average_pixels(top_pxls)
                bot_px = average_pixels(bot_pxls)
            elif sample_method == 'point':
                top_px = pixels[y*width+x]
                bot_px = pixels[(y+y_step//2)*width+x]
            else:
                raise ValueError('sample_method must be one of `average`, `point`')

            ansi_image += color_code.format(*top_px, *bot_px)

        ansi_image += '\033[0m\n'

    return ansi_image

def gif_to_ansi(image, scale, sample_method, verbose=False):
    '''
    :param image: PIL Image
    :param scale: scale factor
    :param sample_method: `point` or `average`

    :returns ansi_images: list of gif frames as ansi images
    :returns frame_times: list of frame times in ms
    '''
    ansi_images = []
    frame_times = []
    c = 1

    while(1):
        if verbose:
            print('\033[2K\rProcessing frame {}'.format(c), end='')
        ansi_images.append(image_to_ansi(image, scale, sample_method))
        frame_times.append(image.info['duration'])

        try:
            image.seek(image.tell()+1)
        except EOFError:
            break

        c += 1

    return ansi_images, frame_times

def play_gif(image, scale, maxfps=None, hide_fps=False, sample_method='point'):
    '''
    :param image: PIL Image
    :param scale: scale factor
    :param maxfps: if provided play gif at constant fps int
    :param hide_fps: don't print fps below gif
    :param sample_method: `point` or `average`
    '''
    start_time = time.time()
    last_time = time.time()

    fps_counter = 0
    frame_counter = 0

    frames, frame_times = gif_to_ansi(image, scale, sample_method, verbose=True)

    if sum(frame_times) == 0:
        maxfps = 24

    length = len(frames) - 1

    if maxfps:
        fps_ms = 1 / maxfps

    print('\033[2J') # clear screen

    while(1):
        print('\033[;H') # move cursor to 0,0
        print(frames[frame_counter], end='')

        if maxfps:
            elapsed = time.time() - last_time
            if elapsed < fps_ms:
                time.sleep(fps_ms - elapsed)

            if not hide_fps:
                print('FPS: {:.0f}'.format(fps_counter / (last_time - start_time)))
            last_time = time.time()
        else:
            time.sleep(frame_times[frame_counter]/1000)

        if frame_counter == length:
            frame_counter = 0
        else:
            frame_counter += 1

        fps_counter += 1

def thumbnail(files, size, sample_method='point'):
    '''
    :param files: list of filenames
    :size: (width, height)
    :param sample_method: `point` or `average`
    '''
    ansi_images = []

    for fp in files:
        try:
            image = Image.open(fp)
        except OSError:
            # not an image file
            continue
        image.thumbnail(size)
        ansi_images.append(image_to_ansi(image, sample_method=sample_method).split('\n'))

    if not ansi_images:
        return

    term_cols, _ = shutil.get_terminal_size()
    images_per_row = term_cols // (size[0] // 7) # 7 magic number crap based on 10pt monospace
    num_images = len(ansi_images)

    for i in range(0, num_images, images_per_row):
        zipped = list(itertools.zip_longest(*ansi_images[i:i+images_per_row]))
        width = [s.count('\033') // 2 for s in zipped[0]]
        output = ''
        for row in zipped:
            for i, segment in enumerate(row):
                if not segment:
                    output += '{}{}'.format(' ' if i else '', ' ' * width[i])
                else:
                    output += '{}{}'.format(' ' if i else '', segment)
            output += '\n'
        print(output, end='')

def average_pixels(pixels):
    '''
    :param pixels: list of (r,g,b) tuples
    '''
    num_pixels = len(pixels)
    return [sum(px) // num_pixels for px in zip(*pixels)]

def average_color(image):
    '''
    :param image: PIL Image

    Returns average color of `image` as (r,g,b)

    https://stackoverflow.com/questions/12703871
    '''
    num_pixels = image.width * image.height
    colors = image.getcolors() # A list of (count, rgb) values
    color_sum = [(c[0] * c[1][0], c[0] * c[1][1], c[0] * c[1][2]) for c in colors]
    average = ([sum(c)//num_pixels for c in zip(*color_sum)])
    return average

def squeeze(val, oldmin=0, oldmax=255, newmin=0, newmax=1):
    return ((val - oldmin) * (newmax - newmin) / (oldmax - oldmin)) + newmin

def main():
    import argparse

    sample_methods = [
        'average',
        'point'
    ]

    parser = argparse.ArgumentParser(prog='tpicview',
        description='View images and play gifs in the terminal.')

    parser.add_argument('file', nargs='*', help='Image(s) to display')
    parser.add_argument('-sc', '--scale', default=1.0, help='Scale factor', metavar='n', type=float)
    parser.add_argument('-sp', '--sample', default='average', help='Sample method', choices=sample_methods)
    parser.add_argument('-f', '--fps', default=None, help='Max FPS (for gifs)', metavar='n', type=int)
    parser.add_argument('-hf', '--hide-fps', help='Don\'t print FPS (for gifs)', action='store_true')
    parser.add_argument('-T', '--thumbnail', help='Thumbnail display of files', action='store_true')
    args = parser.parse_args()

    if args.thumbnail:
        thumbnail(args.file, (256,256), args.sample)
        return

    for fp in args.file:
        try:
            image = Image.open(fp)
        except OSError:
            # not an image file
            continue

        if image.format == 'GIF' and image.info.get('duration') is not None:
            try:
                play_gif(image, args.scale, args.fps, args.hide_fps, args.sample)
            except KeyboardInterrupt:
                print('\033[0m\033[2J')
        else:
            ansi_image = image_to_ansi(image, args.scale, args.sample)
            print(ansi_image, end='')

if __name__ == '__main__':
    main()

