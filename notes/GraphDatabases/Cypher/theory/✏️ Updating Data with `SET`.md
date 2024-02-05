To update data in a node, you use the `SET` clause. This allows you to add new properties to a node or change the values of existing properties.


```
MATCH (var1: Learner {name: 'Bekhruz'})
SET var1.instagram = 'thebekhruz'
```


- **Step 1:** Use the `MATCH` clause to find the node you want to update. Here, we're looking for a `Learner` node named 'Bekhruz'.
- **Step 2:** Use the `SET` clause to update the node's property. In this example, we're setting the `instagram` property to 'thebekhruz'.