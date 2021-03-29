# i18n update

## Requirements 

* Python 

```
apt-get install python3
python -m pip install --upgrade pip
#pip install setuptools wheel
pip install Babel
```
* Babel
```
pip install Babel
```

  
## Usage

### Generate base.pot  

`pybabel extract -o locale/base.pot pidroidbot_discord/`

### Update each catalogs with then new base.pot

`pybabel update -i locale/base.pot -d locale`

### Init catalog for a new language

`pybabel init -l en_US -i locale/base.pot -d locale`

### Compile

`pybabel compile -d locale`