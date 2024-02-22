MATCH (organisation:ORGANISATION)-[:LOCATED_IN]->(location:LOCATION)
RETURN organisation, location
LIMIT 100
