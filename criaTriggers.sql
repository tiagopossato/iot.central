DROP TRIGGER IF EXISTS "main"."ativa_alarme";
CREATE TRIGGER IF NOT EXISTS "main"."ativa_alarme" 
	AFTER UPDATE ON "central_entradadigital" 
	WHEN
		NEW.estado = NEW.triggerAlarme AND
		(NEW.codigoAlarme <> NULL OR NEW.codigoAlarme <> "") AND
		NOT EXISTS (SELECT * FROM central_alarme WHERE codigoAlarme=NEW.codigoAlarme AND ativo=1)
	BEGIN
		INSERT INTO central_alarme(codigoAlarme, mensagemAlarme, prioridadeAlarme, ativo, tempoAtivacao,syncAtivacao, syncInativacao, ambiente_id)
			VALUES(NEW.codigoAlarme, NEW.mensagemAlarme, NEW.prioridadeAlarme, 1,  DATETIME('NOW'),0,0, NEW.ambiente_id);
	END;

DROP TRIGGER IF EXISTS "main"."desativa_alarme";
CREATE TRIGGER IF NOT EXISTS "main"."desativa_alarme" 
	AFTER UPDATE ON "central_entradadigital" 
	WHEN
		NEW.estado <> NEW.triggerAlarme AND
		(NEW.codigoAlarme <> NULL OR NEW.codigoAlarme <> "") AND
		EXISTS (SELECT * FROM central_alarme WHERE codigoAlarme=NEW.codigoAlarme AND ativo=1)
	BEGIN
		UPDATE central_alarme SET ativo = 0, tempoInativacao = DATETIME('NOW'), syncInativacao = 0
			WHERE codigoAlarme = NEW.codigoAlarme;
	END;