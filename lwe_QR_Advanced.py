import numpy as np
from scipy.stats import norm
import secrets
import hashlib

def discrete_gaussian_sampler(sigma, size):
    """
    Generate samples from a discrete Gaussian distribution with standard deviation sigma.
    """
    return np.round(norm.rvs(scale=sigma, size=size)).astype(int)

def generate_lwe_instance(n, m, q, sigma):
    A = np.array([secure_random_int(q, m) for _ in range(n)], dtype=np.int64)
    s = secure_random_int(q, m)
    e = discrete_gaussian_sampler(sigma, n) % q
    b = (np.dot(A, s) + e) % q
    return A, b, s, e

def secure_random_int(q, size):
    return np.array([secrets.randbelow(q) for _ in range(size)])

def encrypt_message(A, m, q):
    # Choose a secure random vector r
    r = secure_random_int(q, A.shape[0])
    
    # Compute the ciphertext c = (A^T r + m) % q
    c = (np.dot(A.T, r) + m) % q
    
    return c, r

def decrypt_message(A, c, r, q):
    # Compute A^T r
    Ar = np.dot(A.T, r) % q
    
    # Recover the message m = (c - Ar) % q
    m = (c - Ar) % q
    
    return m

def hash_key(key):
    # Securely hash the key using SHA-256
    key_bytes = key.tobytes()
    hashed_key = hashlib.sha256(key_bytes).digest()
    return np.frombuffer(hashed_key, dtype=np.uint8)

def clear_sensitive_data(*args):
    for arg in args:
        if isinstance(arg, np.ndarray):
            if not arg.flags.writeable:
                # Create a writable copy and zero it out
                arg_copy = np.copy(arg)
                arg_copy.fill(0)
                arg = arg_copy  # This will not modify the original read-only array
            else:
                arg.fill(0)
        elif isinstance(arg, int):
            arg = 0
        elif isinstance(arg, (list, tuple)):
            for i in range(len(arg)):
                arg[i] = 0





def main():
    try:
        # Parameters
        n = 6024  # Larger dimension for better security
        m = 6024  # Larger dimension for better security
        q = 2**31 - 1  # Larger prime modulus
        sigma = 3.2  # Standard deviation for Gaussian noise

        # Generate LWE instance
        A, b, s, e = generate_lwe_instance(n, m, q, sigma)
        print("Matrix A:\n", A)
        print("Vector b:\n", b)
        print("Secret vector s:\n", s)
        print("Error vector e:\n", e)

        # Encrypt a message
        message = secure_random_int(q, n)
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

        # Securely hash the key for storage
        hashed_s = hash_key(s)
        print("Hashed secret vector s (SHA-256):\n", hashed_s)
    
    finally:
        # Clear sensitive data from memory
        clear_sensitive_data(A, b, s, e, message, ciphertext, r, decrypted_message, hashed_s)

if __name__ == "__main__":
    main()
