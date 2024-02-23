CALL apoc.load.json("file:///data_formatted_date.jsonl") YIELD value AS data
UNWIND data.mentions AS mention
WITH data, COLLECT(mention) AS mentions
MERGE (doc:DOCUMENT {doc_id: data.IAID, text: data.text})

WITH doc
MATCH (doc)-[:MENTIONS]->(org:ORGANISATION), (doc)-[:MENTIONS]->(loc:LOCATION)
MERGE (org)-[:LOCATED_IN]->(loc);