CREATE DATABASE flask_db;
\c flask_db
CREATE USER admin WITH PASSWORD 'password';
GRANT all privileges ON DATABASE flask_db TO admin;

-- CREATE TABLE menu(
--     categoryId      varchar(40), 
--     deals           varchar(40),
-- );

CREATE TABLE category(
    categoryId      serial primary key,
    name            varchar(40) not null
);

CREATE TABLE menu_items(
    itemId          serial primary key,
    name            varchar(40) not null,
    price           decimal(10, 2),
    foreign key (categoryId) references category(categoryId)
);

CREATE TYPE user_type AS ENUM ('manager', 'customer', 'wait_staff', 'kitchen_staff');

CREATE TABLE users(
    userId          serial primary key,
    firstname       varchar(40),
    lastname        varchar(40),
    type            user_type              
);

CREATE TABLE customers(
    customerId      integer primary key,
    foreign key (tableId) references tables(tableId),
    foreign key (customerId) references users(userId)
);

CREATE TABLE wait_staff(
    staffId         integer primary key,
    foreign key (requestId) references requests(requestId),    
    foreign key (staffId) references users(userId)
);

CREATE TABLE kitchen_staff(
    staffId         integer primary key,
    foreign key (orderId) references orders(orderId),
    foreign key (staffId) references users(userId)
);

CREATE TABLE orders(
    orderId         serial primary key,
    foreign key (itemId) references menu_items(itemId),
    -- bill            boolean
);

CREATE TABLE requests(
    requestId       serial primary key,
    foreign key (tableId) references tables(tableId),
    summary         varchar(100) not null,
    complete        boolean
);

CREATE TABLE tables(
    tableId         serial primary key,
    occupied        boolean
);

-- CREATE TABLE Statistics(
--     type        varchar(40),
-- );


