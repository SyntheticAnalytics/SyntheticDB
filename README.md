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

Check out our [demo notebook](https://colab.research.google.com/drive/1mtF_VAENjdRqodGh9kSXj_AWeg4gJxnI?usp=sharing)
to see SyntheticDB in action!

### Supported Features

- Build synthetic tables by specifying distributions for each column to follow
- Use SQL to query your synthetic dataset just as you would query a real DB
- Supported distributions: uniform, log-uniform, normal, log-normal, gamma, exponential, beta, weibull

### Limitations

- Currently the only supported data type is Float
- SQL JOIN's are not yet supported
- Specifying correlation between columns is not yet supported - i.e., all columns are pairwise independent random variables

### What's Next?

In future releases we aim to:
  - support additional data types and distributions
  - support more complex SQL queries
  - support specifying correlations between columns
  - optimize query / sampling performance 

## About The Authors

TODO

