SELECT lead_heat_check FROM hr_applicant WHERE phone_sanitized = '18099999999';



DROP TABLE chat_history;
DROP TABLE va_stage_app;
DROP TABLE speech_log;

CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    msisdn VARCHAR(20) NOT NULL,
    campaign VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    source VARCHAR(100) NOT NULL,
    whatsapp_id VARCHAR(100) NOT NULL,
    sending_date TIMESTAMP NOT NULL,
	readed BOOL DEFAULT FALSE,
	collected BOOL DEFAULT FALSE
);

-- Add indexes
CREATE INDEX idx_msisdn ON chat_history (msisdn);
CREATE INDEX idx_campaign ON chat_history (campaign);
CREATE INDEX idx_whatsapp_id ON chat_history (whatsapp_id);


CREATE TABLE IF NOT EXISTS va_stage_app (
    id SERIAL PRIMARY KEY,
    msisdn VARCHAR(20) NOT NULL,
    campaign VARCHAR(20) NOT NULL,
    state VARCHAR(20) NOT NULL,
    last_update TIMESTAMP NOT NULL
);

-- Add indexes
CREATE INDEX idva_msisdn ON va_stage_app (msisdn);
CREATE INDEX idva_campaign ON va_stage_app (campaign);


CREATE TABLE speech_log (
    id SERIAL PRIMARY KEY,
    msisdn VARCHAR(20) NOT NULL,
    campaign VARCHAR(20) NOT NULL,
    response JSONB,
	audio_path VARCHAR(500),
	response_date TIMESTAMP NOT NULL
);

-- Add indexes
CREATE INDEX idsp_msisdn ON speech_log (msisdn);
CREATE INDEX idsp_campaign ON speech_log (campaign);





SELECT * FROM chat_history ORDER by id DESC;
SELECT * FROM va_stage_app ORDER by id DESC;

SELECT cefr_score FROM hr_applicant WHERE phone_sanitized = '18296456177';
SELECT * FROM hr_recruitment_stage;
SELECT * FROM speech_log;

SELECT * FROM company_info;

---- ------ - - - - - - ------------------

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



CREATE OR REPLACE VIEW  hr_heat_check AS
	SELECT 
		a.id AS applicant_id, s.name->>'en_US' AS lead_stage,
		a.lead_last_update, a.lead_last_client_update,
		computed_heat_check(a.id, a.lead_last_update, a.lead_last_client_update) AS lead_heat_check,
		computed_lead_temperature(a.lead_last_update) AS lead_temperature,
		computed_lead_temperature(a.lead_last_client_update) AS lead_client_temperature
	FROM hr_applicant a, hr_recruitment_stage s
	WHERE a.stage_id = s.id;




SELECT 
	a.id, a.kanban_state, s.name->>'en_US' AS kanban_stage,
	a.lead_last_update, a.lead_last_client_update,
	a.create_date, a.write_date, a.date_last_stage_update, a.date_closed, a.date_open
FROM hr_applicant a, hr_recruitment_stage s
	WHERE a.stage_id = s.id
ORDER by id desc;



UPDATE hr_applicant SET lead_last_update = NOW() - interval '9' day WHERE phone_sanitized = '18099999999';
UPDATE hr_applicant SET lead_last_client_update = NOW() - interval '1' day WHERE phone_sanitized = '18099999999';
UPDATE hr_applicant SET stage_id = 4 WHERE id = 20; -- 4 == "Evaluation"




SELECT lead_last_update, speech_overall_score, lead_max_temperature FROM hr_applicant WHERE phone_sanitized = '18099999999';

UPDATE hr_applicant set speech_overall_score = 75.89, speech_duration = 134.78, speech_fluency = 45, lead_max_temperature = 100
	WHERE phone_sanitized = '18099999999';


SELECT * FROM hr_heat_check;


 SELECT h.lead_heat_check 
                FROM public.hr_applicant AS a
                INNER JOIN public.hr_heat_check AS h
                ON a.id = h.applicant_id;


SELECT * FROM va_chat_history ORDER BY id DESC;
SELECT * FROM va_applicant_stage;
SELECT * FROM va_speech_log;

TRUNCATE TABLE va_chat_history;
TRUNCATE TABLE va_applicant_stage;
TRUNCATE TABLE va_speech_log;




