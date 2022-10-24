# Simple Encrypt Tool

## Why pyEncrypt
- [x] store password in encrypted form, instead of purely store them in memorandum, add even upload to icloud (lollll) 
## Features
- [x] locally config public key & private key
- [x] used in command line, free to get & set password
- [x] memorize in disk, output encrypted code

## Data Structure
- config written in json
- data encrypted written in json file, working like:
    ```json
    {
        "google":"213ab314cf",
        "facebook":"12345fb3cd"
    }
    ```

## Before using:

### generate ssh
```bash
ssh-keygen -t rsa -m PEM
```
Then enter the directory you created `.ssh` file.
```bash
# in .ssh folder
ssh-keygen -f id_rsa.pub -m PEM -e > id_rsa.pub.pem
```

will generate a `.ssh` folder in system path. In windows for example, the folder will be put default in `"C:\\Users\\%Username%\\.ssh"`

The `-m PEM` argument is important in use, cause we use PEM style private & public key


### Setup python environment
```bash
pip install rsa
```

### generate file
```bash
cd pyEncrypt
echo {} >> output.json
echo {} >> config.json
```
currently need this command cause the program will not automatically create an empty json file.
## Usage
### args:
```bash
usage: python encrypt.py [-h] [--set KEY VALUE] [--get GET] [--config ConfigName ConfigValue] [--all]
```

### key config
```bash
python encrypt.py --config ssh-folder <your ssh folder path>
```

### set password
Then, to set a new password, use
```bash
python encrypt.py --set <your-account-name> <your-password>
```
e.g
```bash
python encrypt.py --set google 123456
```

### get password
```bash
python encrypt.py --get <your-account-name> [--all]
```

e.g
```bash
python encrypt.py --get google
```

## TODOs:
- [ ] [ **feat** ] The program currently causes error when file not exist or not in json format. Automatically generate empty json file.
- [ ] [ **feat** ] Release binary version to make it safer.
- [ ] [ **fix** ] Solve the problem of encoding. Some PCs have default coding style rather than utf-8. Should all be adjusted specifically.
- [ ] [ **doc** ] Update doc