# Neomodel Utility Functions Documentation

This document provides information on utility functions used with neomodel for interacting with the Neo4j database.

## neomodel_install_labels

This utility function is used to create label constraints and indexes in the Neo4j database for all the models defined in `my_app/db/models.py`.

### Usage

```bash
neomodel_install_labels my_app/db/models.py --db bolt://neo4j:codingRules@localhost:7687§
```

### Description
When executed, this command will inspect your models defined in the specified file and create any necessary constraints and indexes in the Neo4j database that are defined in your models using UniqueIndex or db_property.

### neomodel_inspect_database
This utility function is used to inspect the current database schema and output neomodel class definitions.

Usage
```
neomodel_inspect_database --db bolt://neo4j:codingRules@localhost:7687

```

### Description
This command connects to the Neo4j database and outputs a Python class definition for each label it finds. This can be useful for bootstrapping your models based on an existing database schema.

### neomodel_remove_labels
This utility function is used to remove label constraints and indexes from the Neo4j database that are no longer used in my_app/db/models.py

```
neomodel_remove_labels --db bolt://neo4j:codingRules@localhost:7687 
```