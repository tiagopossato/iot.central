INSERT INTO "auth_group" VALUES(1,'Administrador');
INSERT INTO "auth_group" VALUES(2,'Instalador');
INSERT INTO "auth_group" VALUES(3,'Visualizador');

INSERT INTO "auth_group_permissions" VALUES(1,1,1);
INSERT INTO "auth_group_permissions" VALUES(2,1,26);
INSERT INTO "auth_group_permissions" VALUES(3,1,27);
INSERT INTO "auth_group_permissions" VALUES(4,1,28);
INSERT INTO "auth_group_permissions" VALUES(5,1,29);
INSERT INTO "auth_group_permissions" VALUES(6,1,30);
INSERT INTO "auth_group_permissions" VALUES(7,1,31);
INSERT INTO "auth_group_permissions" VALUES(8,1,32);
INSERT INTO "auth_group_permissions" VALUES(9,1,33);
INSERT INTO "auth_group_permissions" VALUES(10,2,32);
INSERT INTO "auth_group_permissions" VALUES(11,2,33);
INSERT INTO "auth_group_permissions" VALUES(12,2,22);
INSERT INTO "auth_group_permissions" VALUES(13,2,23);
INSERT INTO "auth_group_permissions" VALUES(14,2,24);
INSERT INTO "auth_group_permissions" VALUES(15,2,28);
INSERT INTO "auth_group_permissions" VALUES(16,2,29);
INSERT INTO "auth_group_permissions" VALUES(17,2,30);
INSERT INTO "auth_group_permissions" VALUES(18,2,31);
INSERT INTO "auth_group_permissions" VALUES(19,2,26);
INSERT INTO "auth_group_permissions" VALUES(20,2,20);
INSERT INTO "auth_group_permissions" VALUES(21,3,26);
INSERT INTO "auth_group_permissions" VALUES(22,3,20);

INSERT INTO "auth_permission" VALUES(1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES(2,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES(3,7,'add_log','Can add log');
INSERT INTO "auth_permission" VALUES(4,7,'change_log','Can change log');
INSERT INTO "auth_permission" VALUES(5,7,'delete_log','Can delete log');
INSERT INTO "auth_permission" VALUES(6,8,'add_placaexpansaodigital','Can add placa expansao digital');
INSERT INTO "auth_permission" VALUES(7,8,'change_placaexpansaodigital','Can change placa expansao digital');
INSERT INTO "auth_permission" VALUES(8,8,'delete_placaexpansaodigital','Can delete placa expansao digital');
INSERT INTO "auth_permission" VALUES(9,9,'add_alarme','Can add alarme');
INSERT INTO "auth_permission" VALUES(10,9,'change_alarme','Can change alarme');
INSERT INTO "auth_permission" VALUES(11,9,'delete_alarme','Can delete alarme');
INSERT INTO "auth_permission" VALUES(12,10,'add_alarmetipo','Can add alarme tipo');
INSERT INTO "auth_permission" VALUES(13,10,'change_alarmetipo','Can change alarme tipo');
INSERT INTO "auth_permission" VALUES(14,10,'delete_alarmetipo','Can delete alarme tipo');
INSERT INTO "auth_permission" VALUES(15,11,'add_entradadigital','Can add entrada digital');
INSERT INTO "auth_permission" VALUES(16,11,'change_entradadigital','Can change entrada digital');
INSERT INTO "auth_permission" VALUES(17,11,'delete_entradadigital','Can delete entrada digital');
INSERT INTO "auth_permission" VALUES(18,12,'add_configuracoes','Can add Configuração');
INSERT INTO "auth_permission" VALUES(19,12,'change_configuracoes','Can change Configuração');
INSERT INTO "auth_permission" VALUES(20,12,'delete_configuracoes','Can delete Configuração');
INSERT INTO "auth_permission" VALUES(21,13,'add_ambiente','Can add Ambiente');
INSERT INTO "auth_permission" VALUES(22,13,'change_ambiente','Can change Ambiente');
INSERT INTO "auth_permission" VALUES(23,13,'delete_ambiente','Can delete Ambiente');

INSERT INTO "auth_user" VALUES(1,'pbkdf2_sha256$30000$XOD1kB8WL4TI$/lxl+Eqhxg2b5dPerf4F9wbEAo+Y4adxnXCeg4aLbWA=','2017-02-02 19:53:50.201531',1,'Tiago','Possato','dev.tiago.possato@gmail.com',1,1,'2017-01-30 11:52:17','tiago');
INSERT INTO "auth_user" VALUES(2,'pbkdf2_sha256$30000$uaxbPDfncCKL$qf3RxamCDegMFYCLIw+2Nse1Y/qDEFj2uE3lV/74w5E=','2017-01-30 19:30:36.935111',1,'','','',1,1,'2017-01-30 12:02:14','mateuszanini');
INSERT INTO "auth_user" VALUES(3,'pbkdf2_sha256$30000$plGfJ1dUhY2M$nhB1GyS+TmXNPd+TXcpDDgaNIilBJIDDzR2B3bVjp6s=','2017-01-30 16:32:34.802257',0,'','','',1,1,'2017-01-30 16:29:55','mateushanser');
INSERT INTO "auth_user" VALUES(4,'pbkdf2_sha256$30000$7NdlcDO2u25E$qbzGD9u+juofE57ABZbMpTfGRtuUHHDC9MEX+CkLt6A=','2017-02-01 13:38:02.335722',0,'','','',1,1,'2017-02-01 13:10:50','angelita');

INSERT INTO "auth_user_groups" VALUES(1,2,2);
INSERT INTO "auth_user_groups" VALUES(2,3,2);
INSERT INTO "auth_user_groups" VALUES(3,5,3);

INSERT INTO "central_ambiente" VALUES(1,'Estufa de enraizamento','-KbztEo7iVuSWveDg3Ge');
INSERT INTO "central_ambiente" VALUES(2,'Estufa de cultivo de flores','');


INSERT INTO "central_configuracoes" VALUES(1,'AIzaSyCaYACeZvP5sW7MHKA5co7PttejxUxnTTM','testes-apisensores.firebaseapp.com','https://testes-apiSensores.firebaseio.com','testes-apiSensores.appspot.com','tiago.possato@yahoo.com.br','123456','-KbztEuoaYejBSl-nyFx');

