--   -------------------------------------------------- 
--   Generated by Enterprise Architect Version 7.5.845
--   Created On : �������, 22 ������, 2011 
--   DBMS       : PostgreSQL 
--   -------------------------------------------------- 




--  Create Tables 
CREATE TABLE BF_ActiveSession ( 
	session_guid char(32) NOT NULL,
	user_id integer NOT NULL,
	session_start timestamp NOT NULL
)
;

CREATE SEQUENCE BF_ApplicationInterface_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_ApplicationInterface ( 
	id bigint DEFAULT NEXTVAL('BF_ApplicationInterface_id_seq'::TEXT) NOT NULL,
	sid varchar(50) NOT NULL,
	url varchar(255),
	db_connect_string varchar(1024),
	description varchar(1024)
)
;

CREATE SEQUENCE BF_Audit_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_Audit ( 
	id bigint DEFAULT NEXTVAL('BF_Audit_id_seq'::TEXT) NOT NULL,
	object_type smallint NOT NULL,
	object_id bigint NOT NULL,
	audit_type smallint NOT NULL,
	datetime timestamp NOT NULL,
	audit_message varchar(1024)
)
;

CREATE TABLE BF_AuditObject ( 
	id smallint NOT NULL,
	sid varchar(50) NOT NULL,
	name varchar(255) NOT NULL,
	description varchar(1024)
)
;

CREATE SEQUENCE BF_AuditType_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_AuditType ( 
	id smallint DEFAULT NEXTVAL('BF_AuditType_id_seq'::TEXT) NOT NULL,
	sid varchar(50) NOT NULL,
	audit_level smallint NOT NULL,    --  0 - fatal 1 - error 2 - warn 3 - info 4 - debug 
	name varchar(255) NOT NULL,
	description varchar(1024)
)
;
COMMENT ON COLUMN BF_AuditType.audit_level
    IS '0 - fatal 1 - error 2 - warn 3 - info 4 - debug'
;

CREATE TABLE BF_CURSOR ( 
	cursor_sid varchar(50) NOT NULL,
	sql_statement varchar(1024) NOT NULL,
	interface_id bigint NOT NULL,
	session_guid char(32) NOT NULL
)
;

CREATE SEQUENCE BF_Department_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_Department ( 
	id integer DEFAULT NEXTVAL('BF_Department_id_seq'::TEXT) NOT NULL,
	name varchar(100) NOT NULL,
	description varchar(1024),
	parent_id integer,
	symbol_id varchar(255) NOT NULL
)
;

CREATE TABLE BF_DepartmentDisableRole ( 
	department_id integer NOT NULL,
	role_id integer NOT NULL
)
;

CREATE SEQUENCE BF_Form_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_Form ( 
	id integer DEFAULT NEXTVAL('BF_Form_id_seq'::TEXT) NOT NULL,
	name varchar(50) NOT NULL,
	version varchar(50) NOT NULL,
	status smallint,    --  1 - active 2 - not active 
	checksum varchar(32),
	form_source bytea NOT NULL,
	modify_datetime timestamp DEFAULT current_timestamp
)
;
COMMENT ON COLUMN BF_Form.status
    IS '1 - active 2 - not active'
;

CREATE TABLE BF_FormPermission ( 
	form_id integer NOT NULL,
	role_id integer NOT NULL,
	perm_type smallint NOT NULL    --  1 - read permission 2 - write permission 
)
;
COMMENT ON COLUMN BF_FormPermission.perm_type
    IS '1 - read permission 2 - write permission'
;

CREATE SEQUENCE BF_Group_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_Group ( 
	id integer DEFAULT NEXTVAL('BF_Group_id_seq'::TEXT) NOT NULL,
	name varchar(50) NOT NULL,
	description varchar(1024),
	parent_id integer,
	type smallint DEFAULT 1 NOT NULL    --  group type: 0 - system 1 - user 
)
;
COMMENT ON COLUMN BF_Group.type
    IS 'group type: 0 - system 1 - user'
;

CREATE TABLE BF_GroupRole ( 
	group_id integer NOT NULL,
	role_id integer NOT NULL
)
;

CREATE SEQUENCE BF_Language_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_Language ( 
	id smallint DEFAULT NEXTVAL('BF_Language_id_seq'::TEXT) NOT NULL,
	lang_sid varchar(50) NOT NULL,
	lang_name varchar(100) NOT NULL
)
;

CREATE SEQUENCE BF_Menu_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_Menu ( 
	id integer DEFAULT NEXTVAL('BF_Menu_id_seq'::TEXT) NOT NULL,
	parent_id integer,
	form_sid varchar(50),
	name varchar(20) NOT NULL,
	help_description varchar(1024),
	shortcut varchar(20)
)
;

CREATE TABLE BF_MenuRole ( 
	menu_id integer NOT NULL,
	role_id integer NOT NULL
)
;

CREATE SEQUENCE BF_Role_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_Role ( 
	id integer DEFAULT NEXTVAL('BF_Role_id_seq'::TEXT) NOT NULL,
	name varchar(128),
	sid varchar(128) NOT NULL,
	description varchar(1024)
)
;

CREATE SEQUENCE BF_SQL_QUERY_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_SQL_QUERY ( 
	id bigint DEFAULT NEXTVAL('BF_SQL_QUERY_id_seq'::TEXT) NOT NULL,
	interface_id bigint NOT NULL,
	sid varchar(100) NOT NULL,
	query varchar(1024) NOT NULL,
	description varchar(1024),
	modify_datetime timestamp NOT NULL
)
;

CREATE SEQUENCE BF_Translate_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_Translate ( 
	id bigint DEFAULT NEXTVAL('BF_Translate_id_seq'::TEXT) NOT NULL,
	translate_obj smallint NOT NULL,
	object_id bigint NOT NULL,
	lang_id smallint NOT NULL,
	translation varchar(1024) NOT NULL
)
;

CREATE SEQUENCE BF_TranslateObject_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_TranslateObject ( 
	id smallint DEFAULT NEXTVAL('BF_TranslateObject_id_seq'::TEXT) NOT NULL,
	object_sid varchar(50) NOT NULL,
	description varchar(1024)
)
;

CREATE SEQUENCE BF_User_id_seq INCREMENT 1 START 1
;

CREATE TABLE BF_User ( 
	id integer DEFAULT NEXTVAL('BF_User_id_seq'::TEXT) NOT NULL,
	department_id integer NOT NULL,
	name varchar(255) NOT NULL,
	status smallint DEFAULT 1 NOT NULL,    --  1 - active user 2 - blocked user 3 - archive user 
	login varchar(20) NOT NULL,
	password_checksum varchar(32) NOT NULL,
	email varchar(255),
	birthday timestamp,
	description varchar(1024)
)
;
COMMENT ON COLUMN BF_User.status
    IS '1 - active user 2 - blocked user 3 - archive user'
;

CREATE TABLE BF_UserGroup ( 
	user_id integer NOT NULL,
	group_id integer NOT NULL
)
;


--  Create Primary Key Constraints 
ALTER TABLE BF_ActiveSession ADD CONSTRAINT PK_BF_ActiveSession 
	PRIMARY KEY (session_guid)
;


ALTER TABLE BF_ApplicationInterface ADD CONSTRAINT PK_BF_URL 
	PRIMARY KEY (id)
;


ALTER TABLE BF_Audit ADD CONSTRAINT PK_BF_Audit 
	PRIMARY KEY (id)
;


ALTER TABLE BF_AuditObject ADD CONSTRAINT PK_BF_AuditObject 
	PRIMARY KEY (id)
;


ALTER TABLE BF_AuditType ADD CONSTRAINT PK_BF_AuditType 
	PRIMARY KEY (id)
;


ALTER TABLE BF_CURSOR ADD CONSTRAINT PK_BF_CURSOR 
	PRIMARY KEY (cursor_sid)
;


ALTER TABLE BF_Department ADD CONSTRAINT PK_Department 
	PRIMARY KEY (id)
;


ALTER TABLE BF_DepartmentDisableRole ADD CONSTRAINT PK_BF_DepartmentRole 
	PRIMARY KEY (department_id, role_id)
;


ALTER TABLE BF_Form ADD CONSTRAINT PK_BF_Form 
	PRIMARY KEY (id)
;


ALTER TABLE BF_FormPermission ADD CONSTRAINT PK_BF_FormPerm 
	PRIMARY KEY (form_id, role_id, perm_type)
;


ALTER TABLE BF_Group ADD CONSTRAINT PK_Group 
	PRIMARY KEY (id)
;


ALTER TABLE BF_GroupRole ADD CONSTRAINT PK_BF_GroupRole 
	PRIMARY KEY (group_id, role_id)
;


ALTER TABLE BF_Language ADD CONSTRAINT PK_BF_LANGUAGE 
	PRIMARY KEY (id)
;


ALTER TABLE BF_Menu ADD CONSTRAINT PK_Menu 
	PRIMARY KEY (id)
;


ALTER TABLE BF_MenuRole ADD CONSTRAINT PK_BF_MenuRole 
	PRIMARY KEY (menu_id, role_id)
;


ALTER TABLE BF_Role ADD CONSTRAINT PK_Role 
	PRIMARY KEY (id)
;


ALTER TABLE BF_SQL_QUERY ADD CONSTRAINT PK_BF_SQL_QUERY 
	PRIMARY KEY (id)
;


ALTER TABLE BF_Translate ADD CONSTRAINT PK_BF_Translate 
	PRIMARY KEY (id)
;


ALTER TABLE BF_TranslateObject ADD CONSTRAINT PK_BF_TranslateObject 
	PRIMARY KEY (id)
;


ALTER TABLE BF_User ADD CONSTRAINT PK_User 
	PRIMARY KEY (id)
;


ALTER TABLE BF_UserGroup ADD CONSTRAINT PK_BF_UserGroup 
	PRIMARY KEY (user_id, group_id)
;



--  Create Indexes 
ALTER TABLE BF_ApplicationInterface
	ADD CONSTRAINT UQ_BF_URL_sid UNIQUE (sid)
;
ALTER TABLE BF_AuditObject
	ADD CONSTRAINT UQ_BF_AuditObject_sid UNIQUE (sid)
;
ALTER TABLE BF_AuditType
	ADD CONSTRAINT UQ_BF_AuditType_sid UNIQUE (sid)
;
ALTER TABLE BF_Department
	ADD CONSTRAINT UQ_BF_Department_symbol_id UNIQUE (symbol_id)
;
ALTER TABLE BF_Role
	ADD CONSTRAINT UQ_Role_sid UNIQUE (sid)
;
ALTER TABLE BF_SQL_QUERY
	ADD CONSTRAINT UQ_BF_SQL_QUERY_sid UNIQUE (sid)
;

--  Create Foreign Key Constraints 
ALTER TABLE BF_ActiveSession ADD CONSTRAINT FK_ActiveSession_User 
	FOREIGN KEY (user_id) REFERENCES BF_User (id)
;

ALTER TABLE BF_Audit ADD CONSTRAINT FK_Audit_AuditObject 
	FOREIGN KEY (object_type) REFERENCES BF_AuditObject (id)
;

ALTER TABLE BF_Audit ADD CONSTRAINT FK_Audit_AuditType 
	FOREIGN KEY (audit_type) REFERENCES BF_AuditType (id)
;

ALTER TABLE BF_CURSOR ADD CONSTRAINT FK_BF_CURSOR_ApplicationInterface 
	FOREIGN KEY (interface_id) REFERENCES BF_ApplicationInterface (id)
;

ALTER TABLE BF_CURSOR ADD CONSTRAINT FK_CURSOR_ActiveSession 
	FOREIGN KEY (session_guid) REFERENCES BF_ActiveSession (session_guid)
;

ALTER TABLE BF_Department ADD CONSTRAINT FK_Department_Department 
	FOREIGN KEY (parent_id) REFERENCES BF_Department (id)
;

ALTER TABLE BF_DepartmentDisableRole ADD CONSTRAINT FK_DepartmentRole_Department 
	FOREIGN KEY (department_id) REFERENCES BF_Department (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_DepartmentDisableRole ADD CONSTRAINT FK_DepartmentRole_Role 
	FOREIGN KEY (role_id) REFERENCES BF_Role (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_FormPermission ADD CONSTRAINT FK_BF_Form_perm_Form 
	FOREIGN KEY (form_id) REFERENCES BF_Form (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_FormPermission ADD CONSTRAINT FK_BF_Form_perm_Role 
	FOREIGN KEY (role_id) REFERENCES BF_Role (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_Group ADD CONSTRAINT FK_Group_Group 
	FOREIGN KEY (parent_id) REFERENCES BF_Group (id)
;

ALTER TABLE BF_GroupRole ADD CONSTRAINT FK_GroupRole_Group 
	FOREIGN KEY (group_id) REFERENCES BF_Group (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_GroupRole ADD CONSTRAINT FK_GroupRole_Role 
	FOREIGN KEY (role_id) REFERENCES BF_Role (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_MenuRole ADD CONSTRAINT FK_BF_MenuRole_BF_Menu 
	FOREIGN KEY (menu_id) REFERENCES BF_Menu (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_MenuRole ADD CONSTRAINT FK_BF_MenuRole_BF_Role 
	FOREIGN KEY (role_id) REFERENCES BF_Role (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_SQL_QUERY ADD CONSTRAINT FK_SQL_QUERY_ApplicationInterface 
	FOREIGN KEY (interface_id) REFERENCES BF_ApplicationInterface (id)
;

ALTER TABLE BF_Translate ADD CONSTRAINT FK_BF_Translate_Language 
	FOREIGN KEY (lang_id) REFERENCES BF_Language (id)
;

ALTER TABLE BF_Translate ADD CONSTRAINT FK_BF_Translate_TranslateObject 
	FOREIGN KEY (translate_obj) REFERENCES BF_TranslateObject (id)
;

ALTER TABLE BF_User ADD CONSTRAINT FK_User_Department 
	FOREIGN KEY (department_id) REFERENCES BF_Department (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_UserGroup ADD CONSTRAINT FK_BF_UserGroup_Group 
	FOREIGN KEY (group_id) REFERENCES BF_Group (id)
ON UPDATE CASCADE
;

ALTER TABLE BF_UserGroup ADD CONSTRAINT FK_BF_UserGroup_User 
	FOREIGN KEY (user_id) REFERENCES BF_User (id)
ON UPDATE CASCADE
;
