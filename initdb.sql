drop table users;
drop table messages;
drop table images;
drop table files;

create table users
(
id int primary key auto_increment,
username varchar(255),
password varchar(255)
);

create table messages
(
id int primary key auto_increment,
time datetime,
username varchar(255),
text varchar(1023),
type varchar(255)
);

create table images
(
id int primary key auto_increment,
username varchar(255),
filename varchar(255),
data longblob
);

create table files
(
id int primary key auto_increment,
username varchar(255),
filename varchar(255),
data longblob
);