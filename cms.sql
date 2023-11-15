CREATE DATABASE IF NOT EXISTS `web_cms_database`;

USE `web_cms_database`;

/* login */

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    middle_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    user_role VARCHAR(20) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY username (username)
)
