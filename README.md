# tinify-cli-client
tinify-cli-client is a Python, command-line client for the TinyPNG API. The same, amazing, image compression and resizing features found at [TinyPNG.com](https://tinypng.com "TinyPNG's Web App") are now available in your favorite terminal. tinify-cli-client allows for compression and resizing of both single files or entire directories, while tinify-cli-client's multithreading capabilities ensure that you harness TinyPNG's tech faster than ever.

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