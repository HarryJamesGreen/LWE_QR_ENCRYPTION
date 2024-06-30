import numpy as np
from scipy.stats import norm

def generate_lwe_instance(n, m, q, sigma):
    # Generate random matrix A
    A = np.random.randint(0, q, size=(n, m))
    
    # Generate secret vector s
    s = np.random.randint(0, q, size=m)
    
    # Generate Gaussian error vector e
    e = np.round(norm.rvs(scale=sigma, size=n)).astype(int) % q
    
    # Compute b = As + e
    b = (np.dot(A, s) + e) % q
    
    return A, b, s, e

def encrypt_message(A, m, q):
    # Choose a random vector r
    r = np.random.randint(0, q, size=A.shape[0])
    
    # Compute the ciphertext c = A^T r + m
    c = (np.dot(A.T, r) + m) % q
    
    return c, r

def decrypt_message(A, c, r, q):
    # Compute A^T r
    Ar = np.dot(A.T, r) % q
    
    # Recover the message m = c - A^T r
    m = (c - Ar) % q
    
    return m

# Parameters
n = 50  # larger dimension for better security
m = 50  # larger dimension for better security
q = 65537  # larger prime modulus
sigma = 3.2  # standard deviation for Gaussian noise

# Generate LWE instance
A, b, s, e = generate_lwe_instance(n, m, q, sigma)
print("Matrix A:\n", A)
print("Vector b:\n", b)
print("Secret vector s:\n", s)
print("Error vector e:\n", e)

# Encrypt a message
message = np.random.randint(0, q, size=n)
ciphertext, r = encrypt_message(A, message, q)
print("Original message:\n", message)
print("Ciphertext:\n", ciphertext)

# Decrypt the message
decrypted_message = decrypt_message(A, ciphertext, r, q)
print("Decrypted message:\n", decrypted_message)

# Check if decryption is successful
if np.array_equal(message, decrypted_message):
    print("Decryption successful!")
else:
    print("Decryption failed.")
