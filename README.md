# tinify-cli-client
Powered by [VirtualZero](https://virtualzero.net "VirtualZero's Website")

tinify-cli-client is a light-weight, Python, command-line client for the TinyPNG API. The same, amazing, image compression and resizing features found at [TinyPNG.com](https://tinypng.com "TinyPNG's Website") are now available in your favorite terminal. tinify-cli-client allows for compression and resizing of both single files or entire directories, while tinify-cli-client's multithreading capabilities ensure that you harness TinyPNG's tech faster than ever.

## Installation

### 1. Clone the tinify-cli-client repository to your machine. 

Copy the following command to clone the repository:

```sh
git clone https://github.com/VirtualZero/tinify-cli-client.git
```

### 2. Install pip3 & pipenv

If you do not have pip3 installed on your machine, copy the following command:

```sh
sudo apt install pip3 -y
```

If you do not have pipenv installed on your machine, copy the following command:

```sh
pip3 install --user pipenv
```

### 3. Create the virtual environment and install the dependencies

Copy the following command to move into the cloned directory, create the virtual environment, and install the dependencies:

```sh
cd tinify-cli-client && pipenv install
```

## Using Your TinyPNG API Key
### Obtaining the API Key

Usage of TinyPNG's API requires an API key that can be obtained from their [website](https://tinypng.com/developers "TinyPNG's Website"). Fortunately, TinyPNG makes the process super-simple.

1. Visit TinyPNG's [developer page](https://tinypng.com/developers "TinyPNG's Developer Page").
2. In the Developer API section of the page, enter your first & last name in the text field on the left, your email in the text field on the right, then click the 'Get your API key' button.
3. TinyPNG will email you a link to your dashboard. Click the link and retrieve your API key.

#### Note:

*TinyPNG permits 500 free image compressions or resizes per month. After reaching the 500 mark, TinyPNG requires a credit card and will charge an extremely fair $0.009 per compression or resize for the next 9,500 images. After reaching 10,000 image compressions and resizes (500 Free + 9,500 @ $0.009), the price per operation drops to only $0.002.*

### Using the API Key with the Script
Now that the API key has been obtained, the script will need access to it. There are two ways to do this.

1. The recommended, easiest, and most secure option is to create an environment variable containing the API key. From within the tinify-cli-client directory, enter the following command:

   ```sh
   echo "TINIFY_API_KEY='YOUR-API-KEY-GOES-HERE'" >> .env && chmod 400 .env
   ```
   *Make sure to replace YOUR-API-KEY-GOES-HERE with your actual API key.*

   That's it! Pipenv always looks for the .env file on launch.
2. This is the least secure option, but the script will function the same. Open tinify-cli-client.py in a text editor. Locate the line of code near the top that reads:

   ```python
   tinify.key = os.environ['TINIFY_API_KEY']
   ```

   Modify the line so that it reads:

   ```python
   tinify.key = 'YOUR-API-KEY-GOES-HERE'
   ```
   *Make sure to replace YOUR-API-KEY-GOES-HERE with your actual API key.*

   And done!

## Usage
### Flags

tinify-cli-client's desired features can be accessed by providing the corresponding flags when running the script. The available flags are detailed below.

| Flag | Operation |
| :--- | :--- |
| -h<br>&#45;&#45;help | Displays the help menu, flags, and flag descriptions |
| -C<br>&#45;&#45;compress | Choose this option to compress images |
| -i<br>&#45;&#45;image | Choose this option to compress a single image |
| -d<br>&#45;&#45;directory | Choose this option to compress all images within a directory |
| -o<br>&#45;&#45;output | Choose this option to specify an output directory for processed images |
| -n<br>&#45;&#45;name | Choose this option to specify a name for a processed image<br>*Only works with single image operations* |
| -R<br>&#45;&#45;resize | Choose this option to resize images<br>*Requires -s, -f, -t, or -c flag* |
| -s<br>&#45;&#45;scale | Scale image(s) to a desired width or height while keeping aspect ratio<br>*Requires **EITHER** -w **OR** -H flag, but not both.* |
| -f<br>&#45;&#45;fit | Scale and fit image(s) within a desired width and height while keeping aspect ratio.<br>*Requires **BOTH** -w **AND** -H flags.* |
| -t<br>&#45;&#45;thumb | Create intelligent thumbnails that match a desired width and height from image(s)<br>*Requires **BOTH** -w **AND** -H flags.* |
| -c<br>&#45;&#45;cover | Scale and crop  image(s) to a desired width and height.<br>*Requires **BOTH** -w **AND** -H flags.*
| -H<br>&#45;&#45;height | The desired height in *PIXELS* of the image(s) when resizing |
| -w<br>&#45;&#45;width | The desired width in *PIXELS* of the image(s) when resizing |

You can view these flags at any time when using tinify-cli-client. From within tinify-cli-client's directory, enter the following command to view the flags:

```sh
pipenv run python tinify-cli-client.py -h
```

### Compression

With tinify-cli-client, you can compress a single image or an entire directory. The optional flags `-o` and `-n` may also be specified.

#### Examples

- **Single Image**

   To compress an image:

   ```sh
   pipenv run python tinify-cli-client.py -Ci /path/to/image/example.png
   ```

   To compress an image and save it to a different directory:

   ```sh
   pipenv run python tinify-cli-client.py -Ci /path/to/image/example.png -o /path/to/different/directory
   ```

   To compress an image and change its name:

   ```sh
   pipenv run python tinify-cli-client.py -Ci /path/to/image/example.png -n new-image-name.png
   ```

   To compress an image, change its name, and save it to a different directory:

   ```sh
   pipenv run python tinify-cli-client.py -Ci /path/to/image/example.png -n new-image-name.png -o /path/to/different/directory
   ```

- **Directory**

   To compress all images in a directory:

   ```sh
   pipenv run python tinify-cli-client.py -Cd /path/to/directory
   ```

   To compress all images in a directory and save them to a different directory:

   ```sh
   pipenv run python tinify-cli-client.py -Cd /path/to/directory -o /path/to/different/directory
   ```

### Resizing
With tinify-cli-client, there are four methods of image resizing.

#### Examples
1. **Scale**

   Scale an image to a desired height or width. Scaling requires either `-H` or `-w` flags, but not both. If both are provided, only the flag that comes first will be considered.

   - **Single Image**
      
      To scale an image:

      ```sh
      pipenv run python tinify-cli-client.py -Rsi /path/to/image/example.png -w 75
      ```

      To scale an image and save it to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rsi /path/to/image/example.png -H 75 -o /path/to/different/directory
      ```

      To scale an image and change its name:

      ```sh
      pipenv run python tinify-cli-client.py -Rsi /path/to/image/example.png -w 75 -n new-image-name.png
      ```

      To scale an image, change its name, and save it to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rsi /path/to/image/example.png -H 75 -n new-image-name.png -o /path/to/different/directory
      ```

   - **Directory**

      To scale all images in a directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rsd /path/to/directory -w 75
      ```

      To scale all images in a directory and save them to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rsd /path/to/directory -H 75 -o /path/to/different/directory
      ```

2. **Fit**

   Scale and fit an image to a desired height and width. Fitting requires both `-H` and `-w` flags and will not work without them.

   - **Single Image**

      To fit an image:

      ```sh
      pipenv run python tinify-cli-client.py -Rfi /path/to/image/example.png -w 75 -H 75
      ```

      To fit an image and save it to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rfi /path/to/image/example.png -w 75 -H 75 -o /path/to/different/directory
      ```

      To fit an image and change its name:

      ```sh
      pipenv run python tinify-cli-client.py -Rfi /path/to/image/example.png -w 75 -H 75 -n new-image-name.png
      ```

      To fit an image, change its name, and save it to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rfi /path/to/image/example.png -w 75 -H 75 -n new-image-name.png -o /path/to/different/directory
      ```

   - **Directory**

      To fit all images in a directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rfd /path/to/directory -w 75 -H 75
      ```

      To fit all images in a directory and save them to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rfd /path/to/directory -w 75 -H 75 -o /path/to/different/directory
      ```

3. **Thumbnail**

   Create intelligent thumbnails that match a desired width and height from image(s). Thumbnails require both `-H` and `-w` flags and will not work without them.

   - **Single Image**

      To create a thumbnail:

      ```sh
      pipenv run python tinify-cli-client.py -Rti /path/to/image/example.png -w 25 -H 25
      ```

      To create a thumbnail and save it to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rti /path/to/image/example.png -w 25 -H 25 -o /path/to/different/directory
      ```

      To create a thumbnail and change its name:

      ```sh
      pipenv run python tinify-cli-client.py -Rti /path/to/image/example.png -w 25 -H 25 -n new-image-name.png
      ```

      To create a thumbnail, change its name, and save it to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rti /path/to/image/example.png -w 25 -H 25 -n new-image-name.png -o /path/to/different/directory
      ```

   - **Directory**

      To create thumbnails of images in a directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rtd /path/to/directory -w 25 -H 25
      ```

      To create thumbnails of images in a directory and save them to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rtd /path/to/directory -w 25 -H 25 -o /path/to/different/directory
      ```

4. **Cover**

    Cover a desired width and height with an image. Covering requires both `-H` and `-w` flags and will not work without them.

   - **Single Image**

      To cover an image:

      ```sh
      pipenv run python tinify-cli-client.py -Rci /path/to/image/example.png -w 75 -H 75
      ```

      To cover an image and save it to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rci /path/to/image/example.png -H 75 -w 75 -o /path/to/different/directory
      ```

      To cover an image and change its name:

      ```sh
      pipenv run python tinify-cli-client.py -Rci /path/to/image/example.png -w 75 -H 75 -n new-image-name.png
      ```

      To cover an image, change its name, and save it to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rci /path/to/image/example.png -H 75 -w 75 -n new-image-name.png -o /path/to/different/directory
      ```

   - **Directory**

      To cover all images in a directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rcd /path/to/directory -w 75 -H 75
      ```

      To cover all images in a directory and save them to a different directory:

      ```sh
      pipenv run python tinify-cli-client.py -Rcd /path/to/directory -w 75 -H 75 -o /path/to/different/directory
      ```