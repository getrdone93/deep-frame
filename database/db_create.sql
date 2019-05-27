CREATE DATABASE prod;
USE prod;

create table if not exists backbone ( 
       backbone_id smallint unsigned not null auto_increment primary key, 
       name text not null);

create table if not exists meta_architecture (
       meta_architecture_id smallint unsigned not null auto_increment primary key,
       name text not null);

create table if not exists model (
       model_id smallint unsigned not null auto_increment primary key, 
       meta_architecture_id_fk smallint unsigned not null,
       backbone_id_fk smallint unsigned not null,
       foreign key (meta_architecture_id_fk) references meta_architecture(meta_architecture_id),
       foreign key (backbone_id_fk) references backbone(backbone_id),
       learning_rate float not null);

create table if not exists metrics (
       metric_id smallint unsigned not null auto_increment primary key,
       model_id_fk smallint unsigned not null,
       foreign key (model_id_fk) references model(model_id));             
       
