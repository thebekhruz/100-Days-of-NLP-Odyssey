// Step 1A: Set Titles for Documents
LOAD CSV WITH HEADERS FROM 'file:///sample_data.csv' AS row FIELDTERMINATOR '\t'
WITH row WHERE row.type = 'title'
MERGE (doc:Document {doc_id: row.doc_id})
SET doc.doc_title = row.value;



LOAD CSV WITH HEADERS FROM 'file:///sample_data.csv' AS row FIELDTERMINATOR '\t'
WITH row WHERE row.type = 'description'
MATCH (doc:Document {doc_id: row.doc_id})
SET doc.doc_descr = row.value;


LOAD CSV WITH HEADERS FROM 'file:///sample_data.csv' AS row FIELDTERMINATOR '\t'
WITH row WHERE row.type = 'mentions'
MATCH (doc:Document {doc_id: row.doc_id})
MERGE (entity:Entity {url: row.value})
MERGE (doc)-[:Mentions]->(entity);