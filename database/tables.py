list_tables = []

joined_users_table = """
CREATE TABLE joined_users (
  id INTEGER PRIMARY KEY,
  name TEXT(45) NULL,
  code TEXT(45) NULL,
  chat_id TEXT(45) NOT NULL,
  status INTEGER NOT NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL);
"""


list_tables.append(joined_users_table)