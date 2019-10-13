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

        if not output_path:
            if not new_name:
                name = image_name.split('.')[0]
                extension = image_name.split('.')[1]

                path_regex = re.compile('^(.*/).*$')
                save_to_path = os.path.join(
                    path_regex.search(image_path).group(1),
                    f'{name}-optimized.{extension}'
                )
                
                source.to_file(save_to_path)

            else:
                path_regex = re.compile('^(.*/).*$')
                save_to_path = f'{path_regex.search(image_path).group(1)}{new_name}'
                source.to_file(save_to_path)

        else:
            if not new_name:
                save_to_path = os.path.join(output_path, image_name)
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

def parse_args():
    parser = argparse.ArgumentParser(
        description="Manipulate images using the tinify API."
    )

    parser.add_argument(
        '-c',
        '--compress',
        help=f'Choose this option to compress images.',
        action='store_true'
    )

    parser.add_argument(
        '-i',
        '--image',
        help=f'Compresses and optimizes a single image. '\
        f'Usage: python tiny.py -ci /path/to/image.png'
    )

    parser.add_argument(
        '-d',
        '--directory',
        help=f'Compresses and optimizes all images within a directory. '\
        f'Usage: python tiny.py -cd /path/to/directory'
    )

    parser.add_argument(
        '-o',
        '--output',
        help=f'Output the optimized image(s) to a specified directory. ' \
        f'Default action with -d option is to create a subdirectory named "optimized" within the '\
        f'directory specified by the -d option. All optimized images are saved within. Default ' \
        f'action with the -i option is to append "-optimized" to the image name and save the optimized ' \
        f'image to the same directory as the source image. ' \
        f'Usage: python tiny.py -ci /path/to/image.jpg -o /path/to/save/directory'
    )

    parser.add_argument(
        '-n',
        '--name',
        help=f'Rename the optimized image. DOES NOT WORK WITH -d OPTION. ' \
        f'Usage: python tiny.py -ci /path/to/image.jpg -o /path/to/save/directory -n new-image-name.jpg'
    )

    return parser.parse_args()

def main():
    args = parse_args()


    # Compress Option
    if args.compress:
        if not args.image and not args.directory:
            print(
                colored(
                    'If compress option is chosen, you must specify -i or -d.',
                    'red'
                )
            )

            sys.exit(1)
        

        # Output Option
        if args.output:
            if not os.path.isdir(args.output):
                print(
                    colored(
                        f'Output directory: {args.output} is not a directory.',
                        'red'
                    )
                )

                sys.exit(1)
            
            output_path = args.output

        else:
            output_path = False


        # Name Option
        if args.name:
            new_name = args.name

        else:
            new_name = False


        # Directory Option
        if args.directory:
            if not os.path.isdir(args.directory):
                print(
                    colored(
                        f'{args.directory} is not a directory',
                        'red'
                    )
                )

                sys.exit(1)

            else:
                optimize_directory(args.directory, output_path)

        elif args.image:
            image_path = args.image
            extension = args.image.split('.')[-1].lower()
            image_name = args.image.strip('/').split('/')[-1]

            if not os.path.isfile(image_path):
                print(
                    colored(
                        f'{args.image} is not a valid image path.',
                        'red'
                    )
                )

                sys.exit(1)

            
            if extension not in valid_extensions:
                print(
                    colored(
                        f'{image_name} is not a valid image, must be .jpg, .png, or .gif.',
                        'red'
                    )
                )

                sys.exit(1)

        
            compress_image(
                image_path,
                output_path,
                new_name
            )


if __name__ == '__main__':
    main()
