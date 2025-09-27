import numpy as np

size = 12
goal = 11

test_matrix = np.random.rand(size, size)
test_matrix = test_matrix / test_matrix.sum(axis=1, keepdims=True)

# Set the 'goal' row to all zeros
test_matrix[goal, :] = 0

# Set the 'goal' column in the 'goal' row to 1
test_matrix[goal, goal] = 1

print(test_matrix)

Q = np.delete(np.delete(test_matrix, goal, axis=0), goal, axis=1)
I_t = np.identity(size - 1)

one_vector = np.ones(size - 1)

print(np.multiply(np.linalg.inv(np.subtract(I_t, Q)), one_vector))

