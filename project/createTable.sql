#Kelly Kung
#CS 304
#Final Project: 
#createTable.sql

#This SQL file creates the different tables we will need for the project

USE kkung_db;

#drop tables if already exists
drop table if exists availability;
drop table if exists events;
drop table if exists users;

#the table 'users' depicts the people who use the site to schedule an appointment
create table users(
       UID integer auto_increment not null primary key,
       user_name varchar(50) not null,
       isCreator enum('yes', 'no')
)
ENGINE = InnoDB;



create table events(
       eventID integer auto_increment not null primary key,
       event_name varchar(50) not null,
       startDate date,
       endDate date,
       UID integer not null,
       INDEX(UID),
       foreign key (UID) references users(UID) on delete restrict

)
ENGINE = InnoDB;


create table availability(
       UID integer not null,
       eventID integer not null,
       INDEX(UID),
       foreign key (UID) references users(UID) on delete restrict,
       INDEX(eventID),
       foreign key (eventID) references events(eventID) on delete restrict,
       availability date
)
ENGINE = InnoDB;


