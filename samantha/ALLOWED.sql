SELECT * FROM hr_applicant WHERE phone_sanitized = '18296456177';



DROP TABLE chat_history;
DROP TABLE va_stage_app;
DROP TABLE speechace_log;

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


CREATE TABLE speechace_log (
    id SERIAL PRIMARY KEY,
    msisdn VARCHAR(20) NOT NULL,
    campaign VARCHAR(20) NOT NULL,
    response JSONB,
	audio_path VARCHAR(300),
	response_date TIMESTAMP NOT NULL
);

-- Add indexes
CREATE INDEX idsp_msisdn ON speechace_log (msisdn);
CREATE INDEX idsp_campaign ON speechace_log (campaign);





SELECT * FROM chat_history ORDER by id DESC;
SELECT * FROM va_stage_app ORDER by id DESC;

SELECT cefr_score FROM hr_applicant WHERE phone_sanitized = '18296456177';
SELECT * FROM hr_recruitment_stage;
SELECT * FROM speechace_log;

SELECT * FROM company_info;


