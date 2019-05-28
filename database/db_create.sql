CREATE DATABASE prod;
USE prod;

create table if not exists backbone ( 
       backbone_id int unsigned not null auto_increment primary key, 
       name text not null);

create table if not exists meta_architecture (
       meta_architecture_id int unsigned not null auto_increment primary key,
       name text not null);

create table if not exists model (
       model_id int unsigned not null auto_increment primary key, 
       meta_architecture_id_fk int unsigned not null,
       backbone_id_fk int unsigned not null,
       foreign key (meta_architecture_id_fk) references meta_architecture(meta_architecture_id),
       foreign key (backbone_id_fk) references backbone(backbone_id),
       learning_rate double not null);

create table if not exists metrics (
       metric_id int unsigned not null auto_increment primary key,
       model_id_fk int unsigned not null,
       foreign key (model_id_fk) references model(model_id),
       loss double not null);      

insert into backbone (name) values ('test_mobilenet');
insert into meta_architecture (name) values ('test_ssd');
