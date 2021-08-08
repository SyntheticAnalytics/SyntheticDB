# SyntheticDB

Simulate querying industry-scale ML datasets locally with real SQL statements
without having to access, manage or pay for industry-scale infrastructure.

## How Does It Work?

SyntheticDB generates data only on an as-needed basis.
That is to say, instead of generating 10000 rows and 
then filtering to get back 250 rows,
SyntheticDB returns you 250 rows without needing 
to materialize the whole original dataset.

Data returned from SyntheticDB queries follow statistical distributions
that you specify when defining the columns for your tables.
In particular, each column is defined by its data type and distribution.
When you use WHERE clauses in your queries SyntheticDB 
samples from the corresponding conditional distributions.

### Demo Notebook

TODO
// insert link to shared google compute notebook here // 

### Supported Features

TODO

### Limitations

TODO

## What's Next?

TODO

## About The Authors

TODO

