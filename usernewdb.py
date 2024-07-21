import sqlite3

# 创建 user.db 数据库并建立表格
conn = sqlite3.connect('C:\\Users\\17590\\PycharmProjects\\onnxcaffe\\database\\user.db')
c = conn.cursor()

# 创建用户表，包括 online 列
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        userid TEXT PRIMARY KEY,
        password TEXT,
        authentic BOOLEAN,
        auntheninfo TEXT,
        online BOOLEAN
    )
''')

# 生成十组用户数据，所有 online 初始化为 False
users = [
    ('user1', 'password1', False, None, False),
    ('user2', 'password2', True, 'feature1', False),
    ('user3', 'password3', False, None, False),
    ('user4', 'password4', True, 'feature2', False),
    ('user5', 'password5', False, None, False),
    ('user6', 'password6', True, 'feature3', False),
    ('user7', 'password7', False, None, False),
    ('user8', 'password8', True, 'feature4', False),
    ('user9', 'password9', False, None, False),
    ('user10', 'password10', True, 'feature5', False)
]

# 插入用户数据
c.executemany('''
    INSERT INTO users (userid, password, authentic, auntheninfo, online)
    VALUES (?, ?, ?, ?, ?)
''', users)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("user.db created and populated successfully with online column set to False.")
