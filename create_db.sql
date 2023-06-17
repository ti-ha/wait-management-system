create database flask_db;
\c flask_db
create user dummy with password 'password';
grant all privileges on database flask_db to dummy;
create table Menu(category varchar(40), deals varchar(40));