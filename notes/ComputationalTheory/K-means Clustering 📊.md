K-means clustering is a popular and simple unsupervised machine learning algorithm used for partitioning a dataset into a set of k groups (or clusters), where k is a predefined or user-defined number. The goal is to minimize the variance within each cluster and maximize the variance between different clusters.

## How It Works 🛠

1. **Initialization**: Start by selecting `k` initial [centroids](Centroids), where `k` is the number of clusters you want. These centroids can be chosen randomly from the dataset or using more complex methods like K-means++.
    
2. **Assignment Step**: Assign each data point to the closest centroid, based on the Euclidean distance (or other distance measures), effectively partitioning the dataset into `k` clusters.
    
3. **Update Step**: Update the centroid of each cluster to be the mean of the points assigned to the cluster.
    
4. **Iteration**: Repeat the assignment and update steps until the centroids do not significantly change between iterations, indicating convergence.


![[Pasted image 20240208125059.png]]
Source: DataCamp [link]([https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.datacamp.com%2Ftutorial%2Fk-means-clustering-python&psig=AOvVaw0Lrg-nd5rTvgxHbuz09DQs&ust=1707483041642000&source=images&cd=vfe&opi=89978449&ved=0CBUQjhxqFwoTCPDOqpPkm4QDFQAAAAAdAAAAABAE))