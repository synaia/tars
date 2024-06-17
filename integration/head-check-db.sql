SELECT * FROM va_message_history ORDER BY id;
SELECT * FROM va_task ORDER BY id;
SELECT * FROM va_stage ORDER BY id;
TRUNCATE TABLE va_message_history, va_stage, va_task;


SHOW timezone;
select now();

ALTER TABLE hr_applicant ADD COLUMN dummy timestamp;

SELECT id, phone_sanitized, partner_phone, name, partner_name, lead_last_update, write_date 
FROM hr_applicant
	WHERE phone_sanitized = '18096785400'
ORDER BY id DESC; 

SELECT 
	a.id, a.kanban_state, s.name->>'en_US' AS kanban_stage,
	a.lead_last_update, a.lead_last_client_update,
	a.create_date, a.write_date, a.date_last_stage_update, a.date_closed, a.date_open
FROM hr_applicant a, hr_recruitment_stage s
	WHERE a.stage_id = s.id
ORDER by id desc;


SELECT 
		s.name->>'en_US', CASE WHEN s.name->>'en_US' <> 'Evaluation' THEN 'Es diferente de Evaluation' ELSE 'Es Evaluation' END
	 FROM hr_applicant a, hr_recruitment_stage s
	WHERE a.id = 20
	  AND a.stage_id = s.id;


SELECT * FROM hr_head_check ORDER BY applicant_id DESC;

UPDATE hr_applicant SET lead_last_update = NOW() - interval '2' day WHERE id = 20;
UPDATE hr_applicant SET lead_last_client_update = NOW() - interval '1' day WHERE id = 20;
UPDATE hr_applicant SET stage_id = 4 WHERE id = 20; -- 4 == "Evaluation"

--- ###### IMPORTANTE ####### ---
-- Las computed column se calculan cuando ocurre un evento INSERT/UPDATE sobre los campos [lead_last_update OR lead_last_client_update]
-- Por lo que en los cambios de [stage_id] para tener un comportamiento esperado se debe actualizar el campo [*_update] que corresponda
-- Cuando [stage_id] es "Evaluation" se debe actualizar [lead_last_client_update] para ver efecto.
-- ***** NUEVO --- cambio de enfoque por caso de uso FAIL; usaremos VIEW dimamicos [hr_applicant].
-- NOTA: Cuando el [stage_id] es un estado que sigue luego de "Evaluation"; entonces hay que definir si hacemos un freeze con los indicadores.
-- Esta impl aporta un manejo de mejor flujo y exp de usuario con las funciones que ya vienen con Odoo
 -- como  filtros, reportes de varios tipos, y la impl kanban de facto aporta mucho. 
-- Aun asi tiene sus detalles:
-- a. El kanban debe ser parcialmente read-only [New > hasta > Evaluation] para usuarios de lo contrario se altera el proceso.
-- b. El proceso está asociado a los nombres de los estados, si estos cambian el proceso deja de funcionar.
-- CAMPOS NO NECESARIOS en table [hr_applicant]:
---- lead_stage, lead_head_check, lead_temperature, lead_client_temperature, 
---- NOTA: [lead_last_update] debe ser timestamp 
--- PARA EL MODULO DE Odoo:
--- los campos nuevos:
--- lead_last_update, lead_last_client_update

CREATE OR REPLACE VIEW  hr_head_check AS
	SELECT 
		a.id AS applicant_id, s.name->>'en_US' AS lead_stage,
		a.lead_last_update, a.lead_last_client_update,
		computed_heat_check(a.id, a.lead_last_update, a.lead_last_client_update) AS lead_heat_check,
		computed_lead_temperature(a.lead_last_update) AS lead_temperature,
		computed_lead_temperature(a.lead_last_client_update) AS lead_client_temperature
	FROM hr_applicant a, hr_recruitment_stage s
	WHERE a.stage_id = s.id;


CREATE OR REPLACE FUNCTION computed_heat_check(p_id integer, p_lead_last_update timestamp, p_lead_last_client_update timestamp)
RETURNS varchar AS $$
DECLARE
	head_check_str varchar;
	v_kanban_stage  varchar;
BEGIN
	SELECT 
		s.name->>'en_US' INTO v_kanban_stage
	 FROM hr_applicant a, hr_recruitment_stage s
	WHERE a.id = p_id
	  AND a.stage_id = s.id;

	IF v_kanban_stage <> 'Evaluation' THEN
		IF (NOW() - p_lead_last_update) BETWEEN INTERVAL '4 days' AND INTERVAL '7 days' THEN
			head_check_str := 'warm';
		ELSIF (NOW() - p_lead_last_update) >  INTERVAL '7 days' THEN
			head_check_str := 'cold';
		ELSE
			head_check_str := 'hot';
		END IF;
	ELSE
		IF (NOW() - p_lead_last_client_update) BETWEEN INTERVAL '4 days' AND INTERVAL '7 days' THEN
			head_check_str := 'warm';
		ELSIF (NOW() - p_lead_last_client_update) >  INTERVAL '7 days' THEN
			head_check_str := 'cold';
		ELSE
			head_check_str := 'hot';
		END IF;
	END IF;

	RETURN head_check_str;
END;
$$ LANGUAGE plpgsql IMMUTABLE;


CREATE OR REPLACE FUNCTION computed_lead_temperature(p_lead_last_update timestamp)
RETURNS decimal AS $$
BEGIN
	IF (10 - EXTRACT(DAY FROM (NOW() - p_lead_last_update))) < 0.0 THEN
		RETURN 0.0;
	ELSE
		RETURN (10 - EXTRACT(DAY FROM (NOW() - p_lead_last_update))) * 0.1;
	END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;


-- ALTER TABLE hr_applicant ADD COLUMN lead_last_update timestamp;

-- ALTER TABLE hr_applicant ADD COLUMN lead_last_client_update timestamp;

-- ALTER TABLE hr_applicant ADD COLUMN lead_head_check varchar GENERATED ALWAYS AS (computed_heat_check(id, lead_last_update, lead_last_client_update)) STORED;

-- ALTER TABLE hr_applicant ADD COLUMN lead_temperature decimal GENERATED ALWAYS AS (computed_lead_temperature(lead_last_update)) STORED;

-- ALTER TABLE hr_applicant ADD COLUMN lead_client_temperature decimal GENERATED ALWAYS AS (computed_lead_temperature(lead_last_client_update)) STORED;


