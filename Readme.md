# Export OTP From Microsoft Authenticator

## Referance article

[Chinese article](https://zhufan.net/2023/10/05/%E6%89%8B%E5%8A%A8%E5%AF%BC%E5%87%BA-microsoft-authenticator-%E4%B8%AD%E7%9A%84%E5%AF%86%E9%92%A5/)


## Export Microsoft Authenticator database

You can use a rooted phone or a rooted android virtual machine，and use root explore app(like mt管理器 root explore ) to export database file from this path "/data/data/com.azure.authenticator/databases/PhoneFactor".

## Get data from PhoneFactor and generate QR images

I add the generate image part to the python script form the reference article. 

This is the full script:

```shell
pip install qrcode[pil]
```

```python3
import sqlite3
import uuid
import json
import qrcode
# connect to sqlite3 database
conn = sqlite3.connect('PhoneFactor')
cursor = conn.cursor()

# execute SQL query，only select account_type=0,because outlook account not supported
cursor.execute("SELECT name, username, oath_secret_key FROM accounts WHERE account_type = 0")

result = []

# put result to object array 
for row in cursor.fetchall():
    name, username, secret_key = row
    uuid_str = str(uuid.uuid4())
    otpauthstr = f"otpauth://totp/{name}:{username}?secret={secret_key}"
    result.append({
        "uuid": uuid_str,
        "otpauthstr": otpauthstr
    })

# close database connection
conn.close()

# generate qrcode images
output_json = json.dumps(result, indent=4)
for i in result:
    print(i)
    img = qrcode.make(i['otpauthstr'])
    img.save(f"{i['uuid']}.png")
```
