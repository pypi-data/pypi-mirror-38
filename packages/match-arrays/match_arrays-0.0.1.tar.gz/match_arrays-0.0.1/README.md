# Match Arrays

`match_arrays` lets you match the values of two NumPy arrays:

```python
a = np.arange(100)
b = np.random.permutation(a)
idx_a, idx_b = match_arrays(a, b)
assert(np.all(a[idx_a] == b[idx_b]))
```

This allows you to perform a database-like join on NumPy arrays.