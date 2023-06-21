create database flask_db;
\c flask_db
create user dummy with password 'password';
grant all privileges on database flask_db to dummy;

create table Menu(
    categoryId  varchar(40), 
    deals       varchar(40)
);

create table Category(
    categoryId  serial primary key
    name        varchar(40) not null
);
create table MenuItem(
    itemId      serial primary key,
    name        varchar(40) not null,
    price       decimal(10, 2),
    foreign key (categoryId) references Menu(categoryId)
)

create table Users(
    userId      serial primary key,
    firstname   varchar(40),
    lastname    varchar(40)
);

create table WaitStaff(
    waitId      integer primary key,
    requests    
    foreign key (userId) references Users(userId),
);

create table KitchenStaff(
    kitchenId   integer primary key,
    orders                
    foreign key (userId) references Users(userId),
);

create table Orders(

);

create table Requests(

);


create table Tables();



create table Statistics(
    type        varchar(40),
);


