--   -------------------------------------------------- 
--   Generated by Enterprise Architect Version 7.5.845
--   Created On : �������, 09 ����, 2011 
--   DBMS       : PostgreSQL 
--   -------------------------------------------------- 




--  Create Tables 
CREATE TABLE NM_CLUSTER ( 
	id serial NOT NULL,
	cluster_sid varchar(50) NOT NULL,
	cluster_type bigint NOT NULL,
	cluster_name varchar(255) NOT NULL,
	description varchar(1024),
	organization varchar(100),
	status smallint NOT NULL,
	last_modifier_id bigint NOT NULL,
	DC timestamp,
	DM timestamp
)
;

CREATE TABLE NM_CLUSTER_TYPE ( 
	id serial NOT NULL,
	type_sid varchar(128),
	description varchar(1024)
)
;

CREATE TABLE NM_CONFIG ( 
	id serial NOT NULL,
	object_id bigint NOT NULL,
	parameter_id bigint NOT NULL,
	parameter_value varchar(1024) NOT NULL,
	last_midifier_id bigint,
	DC timestamp,
	DM timestamp
)
;

CREATE TABLE NM_CONFIG_SPEC ( 
	id serial NOT NULL,
	config_object smallint NOT NULL,    --  1 - cluster 2 - node 
	object_type_id bigint NOT NULL,
	parameter_name varchar(128) NOT NULL,
	parameter_type smallint DEFAULT 1 NOT NULL,    --  1 - string 2 - integer 3 - bool 4 - hidden string 
	posible_values_list text,
	default_value varchar(1024)
)
;
COMMENT ON COLUMN NM_CONFIG_SPEC.config_object
    IS '1 - cluster 2 - node'
;
COMMENT ON COLUMN NM_CONFIG_SPEC.parameter_type
    IS '1 - string 2 - integer 3 - bool 4 - hidden string'
;

CREATE TABLE NM_NODE ( 
	id serial NOT NULL,
	cluster_id integer NOT NULL,
	node_type bigint NOT NULL,
	hostname varchar(50) NOT NULL,
	logic_name varchar(128) NOT NULL,
	admin_status smallint DEFAULT 0 NOT NULL,    --  0 - not active 1 - active 2 - failure 
	current_state smallint DEFAULT 0 NOT NULL,    --  0 - down 1 - up 
	last_datestart timestamp NOT NULL,
	login varchar(50) NOT NULL,
	password varchar(50) NOT NULL,
	last_modifier_id bigint NOT NULL,
	hw_info text,
	sw_info text,
	DC timestamp,
	DM timestamp
)
;
COMMENT ON COLUMN NM_NODE.admin_status
    IS '0 - not active 1 - active 2 - failure'
;
COMMENT ON COLUMN NM_NODE.current_state
    IS '0 - down 1 - up'
;

CREATE TABLE NM_NODE_TYPE ( 
	id serial NOT NULL,
	type_sid varchar(128) NOT NULL,
	description varchar(1024)
)
;

CREATE TABLE NM_OPERATION ( 
	id serial NOT NULL,
	name varchar(128) NOT NULL,    --  symbol identifier 
	timeout bigint NOT NULL,    --  operation timeout in seconds 
	node_type_id bigint,    --  if NULL - for all nodes types 
	description varchar(1024)
)
;
COMMENT ON COLUMN NM_OPERATION.name
    IS 'symbol identifier'
;
COMMENT ON COLUMN NM_OPERATION.timeout
    IS 'operation timeout in seconds'
;
COMMENT ON COLUMN NM_OPERATION.node_type_id
    IS 'if NULL - for all nodes types'
;

CREATE TABLE NM_OPERATION_INSTANCE ( 
	id serial NOT NULL,
	operation_id bigint NOT NULL,
	initiator_id bigint NOT NULL,
	start_datetime timestamp NOT NULL,
	end_datetime timestamp,
	status smallint    --  0 - inprogress 1 - complete 2 - error 
)
;
COMMENT ON COLUMN NM_OPERATION_INSTANCE.status
    IS '0 - inprogress 1 - complete 2 - error'
;

CREATE TABLE NM_OPERATION_PROGRESS ( 
	id serial NOT NULL,
	node_id bigint NOT NULL,
	instance_id bigint NOT NULL,
	progress smallint NOT NULL,
	ret_code smallint,
	ret_message varchar(1024),
	end_datetime timestamp
)
;

CREATE TABLE NM_ROLE ( 
	id serial NOT NULL,
	role_sid varchar(50) NOT NULL,
	role_name varchar(128) NOT NULL
)
;

CREATE TABLE NM_USER ( 
	id serial NOT NULL,
	name varchar(255) NOT NULL,
	password_hash varchar(50) NOT NULL,
	email_address varchar(128),
	additional_info varchar(1024)
)
;

CREATE TABLE NM_USER_ROLE ( 
	id serial NOT NULL,
	user_id bigint NOT NULL,
	role_id bigint NOT NULL
)
;


--  Create Primary Key Constraints 
ALTER TABLE NM_CLUSTER ADD CONSTRAINT PK_CLUSTER 
	PRIMARY KEY (id)
;


ALTER TABLE NM_CLUSTER_TYPE ADD CONSTRAINT PK_NM_CLUSTER_TYPE 
	PRIMARY KEY (id)
;


ALTER TABLE NM_CONFIG ADD CONSTRAINT PK_NM_CONFIG 
	PRIMARY KEY (id)
;


ALTER TABLE NM_CONFIG_SPEC ADD CONSTRAINT PK_NM_CONFIG_SPEC 
	PRIMARY KEY (id)
;


ALTER TABLE NM_NODE ADD CONSTRAINT PK_CLUSTER_NODE 
	PRIMARY KEY (id)
;


ALTER TABLE NM_NODE_TYPE ADD CONSTRAINT PK_NM_NODE_TYPE 
	PRIMARY KEY (id)
;


ALTER TABLE NM_OPERATION ADD CONSTRAINT PK_NM_OPERATION 
	PRIMARY KEY (id)
;


ALTER TABLE NM_OPERATION_INSTANCE ADD CONSTRAINT PK_NM_OPERATION_INSTANCE 
	PRIMARY KEY (id)
;


ALTER TABLE NM_OPERATION_PROGRESS ADD CONSTRAINT PK_NM_OPERATION_PROGRESS 
	PRIMARY KEY (id)
;


ALTER TABLE NM_ROLE ADD CONSTRAINT PK_ROLE 
	PRIMARY KEY (id)
;


ALTER TABLE NM_USER ADD CONSTRAINT PK_USER 
	PRIMARY KEY (id)
;


ALTER TABLE NM_USER_ROLE ADD CONSTRAINT PK_USER_ROLE 
	PRIMARY KEY (id)
;



--  Create Indexes 
ALTER TABLE NM_CLUSTER
	ADD CONSTRAINT UQ_CLUSTER_cluster_sid UNIQUE (cluster_sid)
;
ALTER TABLE NM_CLUSTER_TYPE
	ADD CONSTRAINT UQ_NM_CLUSTER_TYPE_type_sid UNIQUE (type_sid)
;
ALTER TABLE NM_NODE
	ADD CONSTRAINT UQ_CLUSTER_NODE_hostname UNIQUE (hostname)
;
ALTER TABLE NM_NODE
	ADD CONSTRAINT UQ_CLUSTER_NODE_logic_name UNIQUE (logic_name)
;
ALTER TABLE NM_NODE_TYPE
	ADD CONSTRAINT UQ_NM_NODE_TYPE_type_sid UNIQUE (type_sid)
;
ALTER TABLE NM_OPERATION
	ADD CONSTRAINT UQ_NM_OPERATION_name UNIQUE (name)
;
ALTER TABLE NM_USER
	ADD CONSTRAINT UQ_NM_USER_name UNIQUE (name)
;

--  Create Foreign Key Constraints 
ALTER TABLE NM_CLUSTER ADD CONSTRAINT FK_CLUSTER_TYPE 
	FOREIGN KEY (cluster_type) REFERENCES NM_CLUSTER_TYPE (id)
;

ALTER TABLE NM_CONFIG ADD CONSTRAINT FK_NM_CONFIG_USER 
	FOREIGN KEY (last_midifier_id) REFERENCES NM_USER (id)
;

ALTER TABLE NM_CONFIG ADD CONSTRAINT FK_PARAM_CONFIG_SPEC 
	FOREIGN KEY (parameter_id) REFERENCES NM_CONFIG_SPEC (id)
;

ALTER TABLE NM_NODE ADD CONSTRAINT FK_NODE_TYPE 
	FOREIGN KEY (node_type) REFERENCES NM_NODE_TYPE (id)
;

ALTER TABLE NM_NODE ADD CONSTRAINT FK_CLUSTER_NODE 
	FOREIGN KEY (cluster_id) REFERENCES NM_CLUSTER (id)
;

ALTER TABLE NM_OPERATION ADD CONSTRAINT FK_OPER_NODE_TYPE 
	FOREIGN KEY (node_type_id) REFERENCES NM_NODE_TYPE (id)
;

ALTER TABLE NM_OPERATION_INSTANCE ADD CONSTRAINT FK_INSTANCE_NM_OPERATION 
	FOREIGN KEY (operation_id) REFERENCES NM_OPERATION (id)
;

ALTER TABLE NM_OPERATION_INSTANCE ADD CONSTRAINT FK_OPER_INSTANCE_USER 
	FOREIGN KEY (initiator_id) REFERENCES NM_USER (id)
;

ALTER TABLE NM_OPERATION_PROGRESS ADD CONSTRAINT FK_OPER_PROGRESS_INSTANCE 
	FOREIGN KEY (instance_id) REFERENCES NM_OPERATION_INSTANCE (id)
;

ALTER TABLE NM_OPERATION_PROGRESS ADD CONSTRAINT FK_OPER_PROGRESS_NODE 
	FOREIGN KEY (node_id) REFERENCES NM_NODE (id)
;

ALTER TABLE NM_USER_ROLE ADD CONSTRAINT FK_USER_ROLE__ROLE 
	FOREIGN KEY (role_id) REFERENCES NM_ROLE (id)
;

ALTER TABLE NM_USER_ROLE ADD CONSTRAINT FK_USER_ROLE__USER 
	FOREIGN KEY (user_id) REFERENCES NM_USER (id)
;
