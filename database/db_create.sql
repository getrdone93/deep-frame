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
       foreign key (model_id_fk) references model(model_id)
       loss double not null);      


       -- detectionboxes_precision_map double not null,
       -- detectionboxes_precision_large_map double not null,
       -- detectionboxes_precision_medium_map double not null,
       -- detectionboxes_precision_small_map double not null,
       -- detectionboxes_precision_map_0_50_IOU double not null,
       -- detectionboxes_precision_map_0_75_IOU double not null,
       -- detectionboxes_recall_ar_1 double not null,
       -- detectionboxes_recall_ar_10 double not null,
       -- detectionboxes_recall_ar_100 double not null,
       -- detectionboxes_recall_large_ar_100 double not null,
       -- detectionboxes_recall_medium_ar_100 double not null,
       -- detectionboxes_recall_small_ar_100 double not null,
       -- detections_left_groundtruth_right_0_0 double not null,
       -- detections_left_groundtruth_right_1_0 double not null,
       -- detections_left_groundtruth_right_2_0 double not null,
       -- detections_left_groundtruth_right_3_0 double not null

insert into backbone (name) values ('test_mobilenet');
insert into meta_architecture (name) values ('test_ssd');
insert into model (meta_architecture_id_fk, backbone_id_fk, learning_rate) values (1, 1, 1);
insert into model (meta_architecture_id_fk, backbone_id_fk, learning_rate) values (1, 1, 2.0); 
insert into model (meta_architecture_id_fk, backbone_id_fk, learning_rate) 
       values (1, 1,  0.004000000189989805);      
