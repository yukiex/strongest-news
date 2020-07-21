SET CHARSET UTF8;

CREATE TABLE IF NOT EXISTS users
(
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  name TEXT NOT NULL,
  created_at DATETIME,
  updated_at DATETIME,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS articles
(
  id MEDIUMINT NOT NULL,
  title MEDIUMTEXT NOT NULL,
  detail LONGTEXT,
  type TEXT,
  img_url TEXT,
  created_at DATETIME,
  updated_at DATETIME,
  PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS comments
(
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  user_id MEDIUMINT,
  article_id MEDIUMINT NOT NULL,
  detail LONGTEXT NOT NULL,
  created_at DATETIME,
  updated_at DATETIME,
  PRIMARY KEY(id)
); 
