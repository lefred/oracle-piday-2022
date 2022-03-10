-- No SQL Statements

db=session.createSchema('piday)
col=db.createCollection('devices')

col.add({"name": "Raspberry Pi 2011.12", "short_name": "lefredPi", "temperature": "0.0"})

cold.find()

-- SQL Statements 

use piday

create table temperature_history (id bigint unsigned auto_increment primary key,
             time_stamp timestamp default current_timestamp, device_id varchar(32) not null, 
             value decimal(5,2) default 0 not null, 
       key device_id_idx(device_id));

create table humidity_history (id bigint unsigned auto_increment primary key,
             time_stamp timestamp default current_timestamp, device_id varchar(32) not null, 
             value decimal(5,2) default 0 not null, 
       key device_id_idx(device_id));

create table publicip_history (id bigint unsigned auto_increment primary key,
             ip_time_stamp timestamp default current_timestamp, device_id varchar(32) not null, 
             ip_addess varchar(40),
       key device_id_idx(device_id, ip_timestamp));

