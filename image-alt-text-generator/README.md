# Image alt text generator

I had the need to generate alt text for a handful of images and the chatgpt UI would only allow 2 file uploads on the free plan.

## Install requirements

### tkinter

tkinter is required to use a file dialog, make sure it's installed

```sh
sudo apt install python3-tk
```

you can verify if you have this by running the following command:

```sh
python tkinter_verify.py
```

### script requirements

install any packages listed in the requirements.txt

```sh
pip install -r requirements.txt
```

## OpenAI

### payment

this will use a paid feature of openai, ensure that you have payment information set up on your account.

### api key

generate and add an openAI key to a .env file in this directory:

```sh
touch .env
echo "OPENAI_API_KEY=" >> .env
```

copy and paste your openAI key into the .env file.

## Run script

```sh
python run.py
```
