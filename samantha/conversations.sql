DROP TABLE conversations;
DROP TABLE conversations_embedding;
BEGIN;
CREATE TABLE IF NOT EXISTS public.conversations
(
    id bigserial NOT NULL,
	dialog bigserial NOT NULL,
	role VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
	sequence bigserial NOT NULL,
	tags VARCHAR(200) NOT NULL,
    CONSTRAINT conv_info_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.conversations_embedding
(
    id bigserial NOT NULL,
	conv_id bigserial NOT NULL,
    embedding vector,
    CONSTRAINT convemb_info_pkey PRIMARY KEY (id)
);

END;

GRANT ALL PRIVILEGES ON DATABASE synaia TO drfadul;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO drfadul;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO drfadul;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO drfadul;
GRANT ALL PRIVILEGES ON SCHEMA public TO drfadul;



SELECT id, dialog, role, message, sequence, tags FROM conversations ORDER BY id;


SELECT 
	1 - (e.embedding <=> %s::vector) AS similarity,
	c.message,
	c.sequence,
	c.tags,
	COALESCE((SELECT x.message FROM conversations x WHERE x.sequence = c.sequence + 1 AND x.dialog = c.dialog), '') AS next_message,
	COALESCE((SELECT x.message FROM conversations x WHERE x.sequence = c.sequence + 2 AND x.dialog = c.dialog), '') AS hop_message
FROM conversations_embedding e, conversations c
WHERE e.conv_id = c.id
ORDER BY e.embedding <=> %s::vector 
LIMIT %s



SELECT x.* FROM conversations x WHERE x.sequence = 20 AND x.dialog = 5;


SELECT count(*), role FROM conversations GROUP BY role ORDER BY count(*)

SELECT * FROM conversations WHERE dialog = 1 ORDER BY id;


DELETE FROM conversations WHERE dialog = 41



