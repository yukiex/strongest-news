CREATE DATABASE IF NOT EXISTS `strongest`
CHARACTER SET   utf8
COLLATE         utf8_general_ci
;

GRANT ALL PRIVILEGES ON `strongest`.*
TO 'strongest'@'%' IDENTIFIED BY '39inakam'
;

GRANT ALL PRIVILEGES ON `strongest`.*
TO 'strongest'@'127.0.0.1' IDENTIFIED BY '39inakam'
;

GRANT ALL PRIVILEGES ON `strongest`.*
TO 'strongest'@'localhost' IDENTIFIED BY '39inakam'
;

FLUSH PRIVILEGES;
