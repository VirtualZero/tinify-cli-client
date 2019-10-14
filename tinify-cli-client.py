import tinify, os, argparse, sys, re, concurrent.futures
from termcolor import colored
from halo import Halo


tinify.key = os.environ['TINIFY_API_KEY']
script_directory = os.path.dirname(
    os.path.abspath(__file__)
)
valid_extensions = ['jpg', 'png', 'gif']


def compress_image(image_path, output_path, new_name):
    image_name = image_path.strip('/').split('/')[-1]
    with Halo(
        text=f'Compressing {image_name} ...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:
        source = tinify.from_file(image_path)
        name = image_name.split('.')[0]
        extension = image_name.split('.')[1]
        path_regex = re.compile('^(.*/).*$')
        optimized_name = f'{name}-optimized.{extension}'

        if not output_path:
            if not new_name:
                try:
                    save_to_path = os.path.join(
                        path_regex.search(image_path).group(1),
                        optimized_name
                    )

                except AttributeError:
                    save_to_path = optimized_name
                
                source.to_file(save_to_path)

            else:
                path_regex = re.compile('^(.*/).*$')
                save_to_path = os.path.join(
                    path_regex.search(image_path).group(1),
                    new_name
                )
                source.to_file(save_to_path)

        else:
            if not new_name:
                save_to_path = os.path.join(output_path, optimized_name)
                source.to_file(save_to_path)

            else:
                save_to_path = os.path.join(output_path, new_name)
                source.to_file(save_to_path)

    print(
        colored(
            f'Optimized image saved to {save_to_path}',
            'green'
        )
    )
    

def optimize_directory(directory, output_path):
    if not output_path:
        optimized_directory = os.path.join(
            directory,
            'optimized'
        )

    else:
        optimized_directory = output_path

    if not os.path.isdir(optimized_directory):
        os.makedirs(optimized_directory)

    output_messages = []

    def compress_image_(image_path):
        image_name = image_path.strip('/').split('/')[-1]
        save_to_path = os.path.join(optimized_directory, image_name)

        with Halo(
            text=f'Compressing {image_name} ...',
            spinner='dots',
            text_color='white',
            color='green'
        ) as spinner:
            source = tinify.from_file(image_path)
            source.to_file(save_to_path)

        output_messages.append(
            colored(
                f'Optimized image saved to {save_to_path}',
                'green'
            )
        )

    images = [
        f'{os.path.join(directory, image)}' \
        for image in os.listdir(directory) \
        if image.split('.')[-1] in valid_extensions
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(compress_image_, images)        

    for message in output_messages:
        print(
            colored(
                message,
                'green'
            )
        )

    sys.exit(0)


def resize_directory(directory, output_path, method, height, width):
    if not output_path:
        resized_directory = os.path.join(
            directory,
            method
        )

    else:
        resized_directory = output_path

    if not os.path.isdir(resized_directory):
        os.makedirs(resized_directory)

    output_messages = []

    def resize_image_(image_path):
        image_name = image_path.strip('/').split('/')[-1]
        with Halo(
            text=f'Resizing {image_name} ...',
            spinner='dots',
            text_color='white',
            color='green'
        ) as spinner:
            save_to_path = os.path.join(resized_directory, image_name)
            source = tinify.from_file(image_path)

            if method == 'scale':
                if height:
                    resized_image = source.resize(
                        method=method,
                        height=int(height)
                    )

                elif width:
                    resized_image = source.resize(
                        method=method,
                        width=int(width)
                    )

            else:
                resized_image = source.resize(
                    method=method,
                    width=int(width),
                    height=int(height)
                )

            resized_image.to_file(save_to_path)

        output_messages.append(
            colored(
                f'Resized image saved to {save_to_path}',
                'green'
            )
        )

    images = [
        f'{os.path.join(directory, image)}'
        for image in os.listdir(directory)
        if image.split('.')[-1] in valid_extensions
    ]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(resize_image_, images)

    for message in output_messages:
        print(
            colored(
                message,
                'green'
            )
        )

    sys.exit(0)


def resize_image(image_path, output_path, new_name, method, height, width):
    image_name = image_path.strip('/').split('/')[-1]
    with Halo(
        text=f'Resizing {image_name} ...',
        spinner='dots',
        text_color='white',
        color='green'
    ) as spinner:
        path_regex = re.compile('^(.*/).*$')
        name = image_name.split('.')[0]
        extension = image_name.split('.')[1]
        source = tinify.from_file(image_path)

        if method == 'scale':
            if height:
                resized_image = source.resize(
                    method=method,
                    height=int(height)
                )

                resized_name = f'{name}-scaled-h{height}.{extension}'

            elif width:
                resized_image = source.resize(
                    method=method,
                    width=int(width)
                )

                resized_name = f'{name}-scaled-w{width}.{extension}'

        else:
            resized_image = source.resize(
                method=method,
                width=int(width),
                height=int(height)
            )

            resized_name = f'{name}-{method}-{width}x{height}.{extension}'

        if not output_path:
            if not new_name:
                try:
                    save_to_path = os.path.join(
                        path_regex.search(image_path).group(1),
                        resized_name
                    )

                except AttributeError:
                    save_to_path = resized_name

                resized_image.to_file(save_to_path)

            else:
                try:
                    save_to_path = os.path.join(
                        path_regex.search(image_path).group(1),
                        new_name
                    )

                except AttributeError:
                    save_to_path = new_name

                resized_image.to_file(save_to_path)

        else:
            if not new_name:
                save_to_path = os.path.join(output_path, resized_name)
                resized_image.to_file(save_to_path)

            else:
                save_to_path = os.path.join(output_path, new_name)
                resized_image.to_file(save_to_path)

    print(
        colored(
            f'Resized image saved to {save_to_path}',
            'green'
        )
    )


def verify_input(image, directory):
    if not image and not directory:
        print(
            colored(
                'You must specify either -i or -d option.',
                'red'
            )
        )

        sys.exit(1)


def validate_output_path(output_path):
    if not os.path.isdir(output_path):
        print(
            colored(
                f'Output directory: {output_path} is not a directory.',
                'red'
            )
        )

        sys.exit(1)


def validate_directory(directory):
    if not os.path.isdir(directory):
        print(
            colored(
                f'{directory} is not a directory',
                'red'
            )
        )

        sys.exit(1)


def validate_image(image_path):
    if not os.path.isfile(image_path):
        print(
            colored(
                f'{image_path} is not a valid image path.',
                'red'
            )
        )

        sys.exit(1)

    extension = image_path.split('.')[-1].lower()
    image_name = image_path.strip('/').split('/')[-1]

    if extension not in valid_extensions:
        print(
            colored(
                f'{image_name} is not a valid image, must be .jpg, .png, or .gif.',
                'red'
            )
        )

        sys.exit(1)


def validate_resize_options(args):
    if not args.scale \
        and not args.fit \
        and not args.cover \
        and not args.thumb:

        print(
            colored(
                f'You must specify either -s, -f, -t, or -c option when resizing an image.',
                'red'
            )
        )

        sys.exit(1)


def validate_height_and_width(args):
    if args.scale:
        if not args.height and not args.width:
            print(
                colored(
                    f'You must specify either -H OR -w option when scaling an image.',
                    'red'
                )
            )

            sys.exit(1)

        if args.height and args.width:
            print(
                colored(
                    f'You must specify ONLY -H OR -w option when scaling an image, not both.',
                    'red'
                )
            )

            sys.exit(1)

    elif args.fit or args.cover or args.thumb:
        if not args.height or not args.width:
            print(
                colored(
                    f'You must specify both -H AND -w options with this operation.',
                    'red'
                )
            )

            sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Manipulate images using the tinify API."
    )

    parser.add_argument(
        '-C',
        '--compress',
        help=f'Choose this option to compress images.',
        action='store_true'
    )

    parser.add_argument(
        '-i',
        '--image',
        help=f'Compresses and optimizes a single image. '\
        f'Usage: python tinify-cli-client -Ci /path/to/image.png'
    )

    parser.add_argument(
        '-d',
        '--directory',
        help=f'Compresses and optimizes all images within a directory. '\
        f'Usage: python tinify-cli-client -Cd /path/to/directory'
    )

    parser.add_argument(
        '-o',
        '--output',
        help=f'Output the optimized image(s) to a specified directory. ' \
        f'Default action with -d option is to create a subdirectory named "optimized" within the '\
        f'directory specified by the -d option. All optimized images are saved within. Default ' \
        f'action with the -i option is to append "-optimized" to the image name and save the optimized ' \
        f'image to the same directory as the source image. ' \
        f'Usage: python tinify-cli-client -Ci /path/to/image.jpg -o /path/to/save/directory'
    )

    parser.add_argument(
        '-n',
        '--name',
        help=f'Rename the optimized image. DOES NOT WORK WITH -d OPTION. ' \
        f'Usage: python tinify-cli-client -Ci /path/to/image.jpg -o /path/to/save/directory -n new-image-name.jpg'
    )

    parser.add_argument(
        '-R',
        '--resize',
        help=f'Choose this option to resize images. This option requires either -s, -f, -t, or -c options, ' \
        f'as well as either the -H or -w options, or both. Refer to -s, -f, -t, and -c options for more on this.',
        action='store_true'
    )

    parser.add_argument(
        '-s',
        '--scale',
        help=f'Scale the optimized image(s) to a desired width or height while keeping aspect ratio. ' \
        f'Requires either -w OR -H option, but not both. ' \
        f'Usage: python tinify-cli-client -Rsi /path/to/image.jpg -w 125',
        action='store_true'
    )

    parser.add_argument(
        '-f',
        '--fit',
        help=f'Scale and fit the optimized image(s) within a desired width and height. ' \
        f'Requires both -w AND -H options. ' \
        f'Usage: python tinify-cli-client -Rfi /path/to/image.jpg -w 125 -H 125',
        action='store_true'
    )

    parser.add_argument(
        '-t',
        '--thumb',
        help=f'Create a thumbnail of the optimized image(s) to a desired width and height. ' \
        f'Requires both -w AND -H options. '
        f'Usage: python tinify-cli-client -Rti /path/to/image.jpg -w 125 -H 125',
        action='store_true'
    )

    parser.add_argument(
        '-c',
        '--cover',
        help=f'Scale and crop the optimized image(s) to a desired width and height. '
        f'Requires both -w AND -H options. '
        f'Usage: python tinify-cli-client -Rci /path/to/image.jpg -w 125 -H 125',
        action='store_true'
    )

    parser.add_argument(
        '-H',
        '--height',
        help=f'The desired height in PIXELS of the image(s) when resizing.'
    )

    parser.add_argument(
        '-w',
        '--width',
        help=f'The desired width in PIXELS of the image(s) when resizing.'
    )

    return parser.parse_args()


def main():
    args = parse_args()
    verify_input(args.image, args.directory)


    if args.output:
        validate_output_path(args.output)
        output_path = args.output

    else:
        output_path = False


    if args.name:
            new_name = args.name

    else:
        new_name = False


    if args.directory:
        validate_directory(args.directory)

    elif args.image:
        validate_image(args.image)

    if args.compress:

        if args.directory:
            optimize_directory(args.directory, output_path)
                
        elif args.image:
            compress_image(args.image, output_path, new_name)

    elif args.resize:
        validate_resize_options(args)
        validate_height_and_width(args)

        if args.scale:
            method = 'scale'

        elif args.fit:
            method = 'fit'

        elif args.cover:
            method = 'cover'

        elif args.thumb:
            method = 'thumb'

        if args.directory:
            resize_directory(args.directory, output_path, method, args.height, args.width)

        elif args.image:
            resize_image(args.image, output_path, new_name, method, args.height, args.width)
                

if __name__ == '__main__':
    main()
