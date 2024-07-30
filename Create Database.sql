
-- -----------------------------------------------------
-- Schema mbt
-- -----------------------------------------------------
 DROP SCHEMA IF EXISTS mbt;
 CREATE SCHEMA mbt;
 USE mbt;
-- -----如果在同一数据库服务中存在多个数据库（例如MySQL服务器上有多个数据库），通过 USE mbt; 可以告诉数据库系统，后续的SQL语句应该在 mbt 数据库中执行。
-- 一旦选择了特定的数据库模式，所有后续的SQL操作（如创建表、插入数据、查询数据等）都将在该数据库模式的命名空间内进行。这意味着，表格和其他对象的名称在同一数据库内必须是唯一的，但是在不同的数据库之间可以重复。
-- 使用 USE mbt; 可以简化SQL语句，因为后续的SQL操作不需要再显式指定数据库模式的名称，而是默认在已选定的模式下执行。
-- -----------------------------------------------------
DROP TABLE IF EXISTS replies;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS users;

  CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    password_hash CHAR(64) NOT NULL COMMENT 'SHA256 password hash stored in hexadecimal (64 characters)',
    email VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
    role ENUM('member', 'moderator', 'admin') NOT NULL,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    dob Date,
    location VARCHAR(100),
    profile_image VARCHAR(255),
    status ENUM('active','inactive') NOT NULL,
    PRIMARY KEY (user_id)
    );




  CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    title VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
  );


  CREATE TABLE IF NOT EXISTS replies (
    reply_id INT AUTO_INCREMENT PRIMARY KEY,
    content VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    message_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
  );
-- 须删去unique (user_id),否则一名用户只能发一条消息