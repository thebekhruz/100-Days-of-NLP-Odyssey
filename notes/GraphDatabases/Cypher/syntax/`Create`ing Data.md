

```
CREATE (learner: Learner {name: 'Bekhruz'}),
       (hello: Greeting {message: 'Nice to meet you'}),
       (learner)-[r:SAYS]->(hello)
```

## Notes

- In this snippet, we create two nodes (`learner` and `hello`) with labels and properties.
- We then create a directed relationship of type `SAYS` from `learner` to `hello`.
- This structure could represent, for example, a scenario where a learner is saying a greeting.
![[CypherNodes.png]]
### 1. `CREATE` Statement 🌱

- The `CREATE` statement adds new nodes and relationships to the graph.

### 2. Nodes and Labels 📌 ![[Nodes and Labels 📌]]
### 3. Relationships and Relationship Types 🔗

- **Relationship Creation**:
    - `(learner)-[r:SAYS]->(hello)`
	- This line creates a relationship from the `learner` node to the `hello` node.
- **Relationship Type**:
    - `SAYS` is a type of relationship similar to a label for relationships.
- **Direction**:
    - The arrow `->` indicates the direction of the relationship (from `learner` to `hello`).
- **Relationship Variable**:
    - `r` is a variable assigned to this relationship, which can be used for later reference.