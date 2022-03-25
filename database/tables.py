
list_tables = []
list_update_tables = []

joined_users_table = """
CREATE TABLE joined_users (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NULL,
  code VARCHAR(45) NULL,
  chat_id VARCHAR(45) NOT NULL,
  status INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL,
  PRIMARY KEY (id));
"""

# update_sessions_for_ui = """
# ALTER TABLE sessions ADD COLUMN login_status INT NULL AFTER password;
# ALTER TABLE sessions ADD COLUMN code VARCHAR(45) NULL AFTER login_status;
# """


list_tables.append(joined_users_table)