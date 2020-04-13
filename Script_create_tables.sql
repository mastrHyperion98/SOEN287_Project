show databases;

use Chatty;

create table users
(
	id INTEGER AUTO_INCREMENT NOT NULL,
	email VARCHAR(50) NOT NULL,
	password VARCHAR(16) NOT NULL,
	username VARCHAR(32) NOT NULL,
	permalink VARCHAR(8) NOT NULL,
	login DATE NOT NULL,
	PRIMARY KEY (id, email, username, permalink)
);

create table channels
(
	id INTEGER AUTO_INCREMENT NOT NULL,
	admin_id INTEGER NOT NULL,
	name VARCHAR(16) NOT NULL,
	permalink VARCHAR(8) NOT NULL,
	PRIMARY KEY (id, permalink),
	FOREIGN KEY (admin_id) REFERENCES users(id)
);

create table members
(
	id INTEGER AUTO_INCREMENT NOT NULL,
	channel_id INTEGER NOT NULL,
	user_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (channel_id) REFERENCES channels(id),
	FOREIGN KEY (user_id) REFERENCES users(id)
);

create table messages
(
	id INTEGER AUTO_INCREMENT NOT NULL,
	member_id INTEGER NOT NULL,
	content VARCHAR(255) NOT NULL,
	date_time DATETIME NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (member_id) REFERENCES members(id)
);
