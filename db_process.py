import pymongo
import json
import tiktoken
from settings import *

client = pymongo.MongoClient(MONGODB_URI)
    
def authenticate_user(username, password):
    # 连接到 MongoDB 数据库，并检查 user_info 集合中是否存在提供的用户名和密码
    db = client['database']
    user_info = db['user_info']
    count = user_info.count_documents({'user_id': username, 'password': password})

    # 如果找到匹配的用户名和密码，则返回 True，否则返回 False
    return count == 1

def insert_db(result, user_id=None, messages=[]):
    # 获取要插入的结果数据
    now = result.get('datetime')
    user_id = result.get('user_id')
    cn_char_count = result.get('cn_char_count')
    en_char_count = result.get('en_char_count')
    tokens = result.get('tokens')
    
    # 插入数据
    db = client['database']
    collection = db['stats']
    collection.insert_one({
        'user_id': user_id,
        'datetime': now,
        'cn_char_count': cn_char_count,
        'en_char_count': en_char_count,
        'tokens': tokens
    })
    
    if user_id:
        messages_str = json.dumps(messages, ensure_ascii=False)
        collection = db['session']
        collection.update_one({'user_id': user_id}, {'$set': {'messages': messages_str}}, upsert=True)

def clear_messages(user_id):
    # 删除数据
    db = client['database']
    collection = db['session_messages']
    collection.delete_one({'user_id': user_id})
        
def save_user_messages(user_id, messages):
    # 更新数据
    messages_str = json.dumps(messages, ensure_ascii=False)
    db = client['database']
    collection = db['session_messages']
    collection.update_one({'user_id': user_id}, {'$set': {'messages': messages_str}}, upsert=True)
            
def get_user_messages(user_id):
    # 查询数据
    db = client['database']
    collection = db['session_messages']
    row = collection.find_one({'user_id': user_id})
    
    if row is None:
        messages = []
    else:
        messages_str = row['messages']
        messages = json.loads(messages_str)
        
    return messages

def history_messages(user_id):
    rows = 2
    if user_id == 'sonic':
        rows = 4
    return rows

def num_tokens(string: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens
