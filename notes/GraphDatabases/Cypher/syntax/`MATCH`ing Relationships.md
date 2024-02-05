```
MATCH (s:Student {first:'Alia'})--(c:Country)
```

- **`MATCH (s: Student {first:'Alia'})`**: This part of the query matches nodes labeled `Student` with a property `first` equal to `'Alia'`.
- **`--(c:Country)`**: The double dash `--` represents a relationship in any direction between the matched student and any node labeled `Country`.


```
MATCH (s:Student {first:'Alia'})-[:STUDIED_ABROAD_IN]->(c:Country)
```
- **`MATCH (s:Student {first:'Alia'})`**: Matches `Student` nodes where `first` equals 'Alia'.
- **-`[:STUDIED_ABROAD_IN]->(c:Country)`**: This specifies a directed relationship of type `STUDIED_ABROAD_IN` from `Alia` to a `Country` node.



```
MATCH (s:Student)-[r:OBTAINED]->()
WHERE r.gpa >3.98
RETURN s.first, s.last, r.gpa
```