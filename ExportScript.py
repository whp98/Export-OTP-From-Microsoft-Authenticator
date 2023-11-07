import sqlite3
import uuid
import json
import qrcode
# 连接到SQLite数据库
conn = sqlite3.connect('PhoneFactor')
cursor = conn.cursor()

# 执行SQL查询，仅选择account_type为0的行
cursor.execute("SELECT name, username, oath_secret_key FROM accounts WHERE account_type = 0")

result = []

# 遍历查询结果，并创建所需的JSON对象
for row in cursor.fetchall():
    name, username, secret_key = row
    uuid_str = str(uuid.uuid4())
    otpauthstr = f"otpauth://totp/{name}:{username}?secret={secret_key}"
    result.append({
        "uuid": uuid_str,
        "otpauthstr": otpauthstr
    })

# 关闭数据库连接
conn.close()

# 将结果以JSON格式输出
output_json = json.dumps(result, indent=4)
for i in result:
    print(i)
    img = qrcode.make(i['otpauthstr'])
    img.save(f"{i['uuid']}.png")



