BEGIN TRANSACTION;
INSERT INTO "aplicacao_grandeza" VALUES(3303,'Temperatura','C','2017-08-09 21:19:44.601252','2017-08-09 21:19:44.601252');
INSERT INTO "aplicacao_grandeza" VALUES(3304,'Umidade Relativa do Ar','%uR','2017-08-09 21:19:44.601252','2017-08-09 21:19:44.601252');
COMMIT;

BEGIN TRANSACTION;
INSERT INTO "auth_user" VALUES(1,'pbkdf2_sha256$36000$aTMQQ4wMaUux$m9THiT4UirjzVk87gb+ecR2iWHd07LWtMkPkksdRjuU=',NULL,1,'','','tiago.possato@yahoo.com.br',1,1,'2017-08-07 10:01:11.826483','admin');
COMMIT;

