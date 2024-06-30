import numpy as np

def generate_lwe_instance(n, m, q):
    # Generate random matrix A
    A = np.random.randint(0, q, size=(n, m))
    
    # Generate secret vector s
    s = np.random.randint(0, q, size=m)
    
    # Generate small error vector e
    e = np.random.randint(-1, 2, size=n)  # small values -1, 0, 1
    
    # Compute b = As + e
    b = (np.dot(A, s) + e) % q
    
    return A, b, s, e

def encrypt_message(A, m, q):
    # Choose a random vector r
    r = np.random.randint(0, q, size=A.shape[0])
    
    # Compute the ciphertext c = A^T r + m
    c = (np.dot(A.T, r) + m) % q
    
    return c

def decrypt_message(A, c, m, q):
    # Compute A^T r = c - m
    Ar = (c - m) % q
    
    return Ar

# Parameters
n = 5  # dimension of b and e
m = 5  # dimension of s
q = 23  # modulus

# Generate LWE instance
A, b, s, e = generate_lwe_instance(n, m, q)
print("Matrix A:\n", A)
print("Vector b:\n", b)
print("Secret vector s:\n", s)
print("Error vector e:\n", e)

# Encrypt a message
message = np.random.randint(0, q, size=n)
ciphertext = encrypt_message(A, message, q)
print("Original message:\n", message)
print("Ciphertext:\n", ciphertext)

# Decrypt the message
decrypted_message = decrypt_message(A, ciphertext, message, q)
print("Decrypted message (A^T r):\n", decrypted_message)
