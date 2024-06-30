import numpy as np
from scipy.stats import norm
import os
import pickle

def generate_lwe_instance(n, m, q, sigma):
    # Generate random matrix A
    A = np.random.randint(0, q, size=(n, m))
    
    # Generate secret vector s
    s = np.random.randint(0, q, size=m)
    
    # Generate Gaussian error vector e
    e = np.round(norm.rvs(scale=sigma, size=n)).astype(int) % q
    
    # Compute b = (As + e) % q
    b = (np.dot(A, s) + e) % q
    
    return A, b, s, e

def encrypt_message(A, m, q):
    # Choose a random vector r
    r = np.random.randint(0, q, size=A.shape[0])
    
    # Compute the ciphertext c = (A^T r + m) % q
    c = (np.dot(A.T, r) + m) % q
    
    return c, r

def decrypt_message(A, c, r, q):
    # Compute A^T r
    Ar = np.dot(A.T, r) % q
    
    # Recover the message m = (c - Ar) % q
    m = (c - Ar) % q
    
    return m

def save_to_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_from_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def encrypt_file(input_file, output_file, A, q):
    with open(input_file, 'rb') as f:
        file_data = f.read()
    
    # Convert file data to an integer array
    file_data_int = np.frombuffer(file_data, dtype=np.uint8)
    message = file_data_int % q
    
    ciphertext, r = encrypt_message(A, message, q)
    
    # Save ciphertext and r to file
    save_to_file(output_file, (ciphertext, r))

def decrypt_file(input_file, output_file, A, s, q):
    # Load ciphertext and r from file
    ciphertext, r = load_from_file(input_file)
    
    decrypted_message = decrypt_message(A, ciphertext, r, q)
    
    # Convert decrypted message back to bytes
    file_data_bytes = np.array(decrypted_message, dtype=np.uint8).tobytes()
    
    with open(output_file, 'wb') as f:
        f.write(file_data_bytes)

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

# Example usage for encrypting and decrypting a file
input_file = 'input.txt'
encrypted_file = 'encrypted.pkl'
decrypted_file = 'decrypted.txt'

# Encrypt the file
encrypt_file(input_file, encrypted_file, A, q)

# Decrypt the file
decrypt_file(encrypted_file, decrypted_file, A, s, q)
