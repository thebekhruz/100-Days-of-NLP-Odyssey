```
MATCH n
RETURN n LIMIT 10
```
- **`MATCH n`**: This part of the query matches all nodes in the graph, regardless of their labels or properties.

```
MATCH (n:student)
RETURN n LIMIT 10
```
- **`MATCH (n:student)`**: Matches all nodes with the label `student`.


```
MATCH (n {first : 'Alia'})
RETURN n LIMIT 10
```
- **`MATCH (n {first : 'Alia'})**`: Matches nodes with a property `first` that has the value `'Alia'`.

```
MATCH (n:Student)
WHERE n.first = 'Alia'
RETURN n
```

- **`MATCH (n:Student)`**: Matches all nodes with the label `Student`.
- **`WHERE n.first = 'Alia`'**: Narrows down the result to nodes where the property `first` equals `'Alia'`.
[[Syntax -- `MATCH`ing Relationships]]
