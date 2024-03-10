// CALL apoc.load.json("file:///data.jsonl") YIELD value AS data
CALL apoc.load.json("file:///data_with_contextual_relevance_and_doc_embddings.jsonl") YIELD value AS data
UNWIND data.mentions AS mention
WITH data, COLLECT(mention) AS mentions
MERGE (doc:DOCUMENT {doc_id: data.IAID, text: data.text, text_embedding: data.text_embedding })

FOREACH(mention IN mentions |

    // Handle DATE mentions by creating or merging DATE nodes
    FOREACH(_ IN CASE WHEN mention.ne_type = 'DATE' THEN [1] ELSE [] END |
        MERGE (date:DATE {date: mention.formatted_date})
        MERGE (doc)-[:MENTIONED_ON {ne_type: mention.ne_type,
            ne_start: mention.ne_start,
            ne_end: mention.ne_end,
            total_tfidf_score: mention.total_tfidf_score}]->(date)
    )

    // Handle PERSON mentions by creating or merging PERSON nodes
    FOREACH(_ IN CASE WHEN mention.ne_type = 'PER' THEN [1] ELSE [] END |
        MERGE (person:PERSON {name: mention.ne_span})
        FOREACH (_ IN CASE WHEN mention.id IS NOT NULL THEN [1] ELSE [] END |
            SET person.wiki_ID = mention.id
        )
        MERGE (doc)-[:MENTIONS {ne_type: mention.ne_type,
            ne_start: mention.ne_start,
            ne_end: mention.ne_end,
            total_tfidf_score: mention.total_tfidf_score}]->(person)
    )

    // Handle ORGANISATION mentions by creating or merging ORGANISATION nodes
    FOREACH(_ IN CASE WHEN mention.ne_type = 'ORG' THEN [1] ELSE [] END |
        MERGE (organisation:ORGANISATION {name: mention.ne_span})
        FOREACH (_ IN CASE WHEN mention.id IS NOT NULL THEN [1] ELSE [] END |
            SET organisation.wiki_ID = mention.id
        )
        MERGE (doc)-[:MENTIONS {ne_type: mention.ne_type,
            ne_start: mention.ne_start,
            ne_end: mention.ne_end,
            total_tfidf_score: mention.total_tfidf_score}]->(organisation)
    )

    // Handle LOCATION mentions by creating or merging LOCATION nodes
    FOREACH(_ IN CASE WHEN mention.ne_type = 'LOC' THEN [1] ELSE [] END |
        MERGE (location:LOCATION {name: mention.ne_span})
        FOREACH (_ IN CASE WHEN mention.id IS NOT NULL THEN [1] ELSE [] END |
            SET location.wiki_ID = mention.id
        )
        MERGE (doc)-[:MENTIONS {ne_type: mention.ne_type,
            ne_start: mention.ne_start,
            ne_end: mention.ne_end,
            total_tfidf_score: mention.total_tfidf_score}]->(location)
    )

    // Handle MISCELLANEOUS mentions by creating or merging MISCELLANEOUS nodes
    FOREACH(_ IN CASE WHEN mention.ne_type = 'MISC' THEN [1] ELSE [] END |
        MERGE (misc:MISCELLANEOUS {name: mention.ne_span})
        FOREACH (_ IN CASE WHEN mention.id IS NOT NULL THEN [1] ELSE [] END |
            SET misc.wiki_ID = mention.id
        )
        MERGE (doc)-[:MENTIONS {ne_type: mention.ne_type,
            ne_start: mention.ne_start,
            ne_end: mention.ne_end,
            total_tfidf_score: mention.total_tfidf_score}]->(misc)
    )


)