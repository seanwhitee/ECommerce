# ECommerce
[Youtube Demo](https://youtu.be/TKgHaxGVatA)
## Database design
```
users ( username, password, name, email )
products ( product_id, product_name, price, seller(F.K.), description )
buy_table ( buy_id, username(F.K.), product_id(F.K.) )
```

## Usage
### 1. Create venv
```bash
# Create venv
python3 -m venv <venv-name>

# activate
## for windows
<venv-name>\Scripts\activate

## for mac
source <venv-name>/bin/activate
```

### 2. Install dependency

I already create requirements.txt for you.
```bash
pip install -r requirements.txt
```
If there is some dependency not in the <strong>requirements.txt</strong>, feel free to use <strong>pip install</strong>.

### 3. Create secrets.toml for streamlit database.

In <strong>./streamlit/secrets.toml</strong>, type in the database server setting.

For example,
```bash
[mysql]
host = ""
port = 
database = ""
user = ""
password = ""
```
### 4. Create config.yaml
You can follow the instruction [here](https://github.com/mkhorasani/Streamlit-Authenticator).
