-- 这是 Melon Chat 的数据库初始化脚本
-- 请在执行前确保数据库已创建
-- 本脚本会删除现有的表并重新创建，如果有老版本数据，请先备份！！！
-- 可以使用本脚本进行重置，将会清空所有原有数据

drop table if exists users;
drop table if exists publicMsg;
drop table if exists chat;
drop table if exists files;
drop table if exists images;
drop table if exists notes;

create table users(
    uid int primary key auto_increment,
    username varchar(255),
    passwordHash varchar(255),
    permissions varchar(255),
    label varchar(255),
    homepage longtext,
    iid int
);

create table publicMsg(
    mid int primary key auto_increment,
    uid int,
    time datetime,
    msg varchar(20000),
    type varchar(255),
);

create table chat(
    cid int primary key auto_increment,
    sender int,
    receiver int,
    time datetime,
    msg varchar(20000),
    type varchar(255)
);

create table files(
    fid int primary key auto_increment,
    uid int,
    time datetime,
    name varchar(255),
    data longblob,
    deleted boolean,
);

create table images(
    iid int primary key auto_increment,
    uid int,
    time datetime,
    name varchar(255),
    data longblob,
    deleted boolean,
);

create table notes(
    nid int primary key auto_increment,
    uid int,
    time datetime,
    title varchar(255),
    content longtext,
    deleted boolean,
)