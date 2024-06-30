import numpy as np
from scipy.stats import norm
import secrets
import hashlib
from numpy.random import default_rng
import os
import argparse
import pickle

def discrete_gaussian_sampler(sigma, size):
    rng = default_rng()
    return np.round(rng.normal(0, sigma, size)).astype(int)

def generate_lwe_instance(n, m, q, sigma):
    A = np.array([secure_random_int(q, m) for _ in range(n)], dtype=np.int64)
    s = secure_random_int(q, m)
    e = discrete_gaussian_sampler(sigma, n) % q
    b = (np.dot(A, s) + e) % q
    return A, b, s, e

def secure_random_int(q, size):
    return np.array([secrets.randbelow(q) for _ in range(size)], dtype=np.int64)

def pad_message(message, n):
    message_length = len(message)
    if message_length < n:
        padding_length = n - message_length
        padding = np.zeros(padding_length, dtype=np.int64)
        padded_message = np.concatenate((message, padding))
    else:
        padded_message = message[:n]
    return padded_message

def encrypt_message(A, m, q):
    r = secure_random_int(q, A.shape[0])
    c = (np.dot(A.T, r) + m) % q
    return c, r

def decrypt_message(A, c, r, q):
    Ar = np.dot(A.T, r) % q
    m = (c - Ar) % q
    return m

def hash_key(key):
    key_bytes = key.tobytes()
    hashed_key = hashlib.sha256(key_bytes).digest()
    return np.frombuffer(hashed_key, dtype=np.uint8)

def clear_sensitive_data(*args):
    for arg in args:
        if isinstance(arg, np.ndarray):
            if not arg.flags.writeable:
                arg.flags.writeable = True
            arg.fill(0)
        elif isinstance(arg, int):
            arg = 0
        elif isinstance(arg, (list, tuple)):
            for i in range(len(arg)):
                arg[i] = 0

def encrypt_file(input_file, output_file, A, q, sigma):
    with open(input_file, 'rb') as f:
        file_data = f.read()
    file_data_int = np.frombuffer(file_data, dtype=np.uint8).astype(np.int64) % q
    padded_length = A.shape[0] * ((len(file_data_int) // A.shape[0]) + 1)
    padded_data = np.zeros(padded_length, dtype=np.int64)
    padded_data[:len(file_data_int)] = file_data_int
    ciphertext, r = encrypt_message(A, padded_data, q)
    with open(output_file, 'wb') as f:
        pickle.dump((ciphertext, r), f)

def decrypt_file(input_file, output_file, A, q):
    with open(input_file, 'rb') as f:
        ciphertext, r = pickle.load(f)
    decrypted_message = decrypt_message(A, ciphertext, r, q)
    decrypted_bytes = decrypted_message.astype(np.uint8).tobytes()
    with open(output_file, 'wb') as f:
        f.write(decrypted_bytes)

def main():
    parser = argparse.ArgumentParser(description="LWE-based encryption and decryption")
    parser.add_argument('--action', choices=['encrypt-message', 'decrypt-message', 'encrypt-file', 'decrypt-file'], required=True, help="Action to perform")
    parser.add_argument('--message', type=str, help="Message to encrypt/decrypt")
    parser.add_argument('--input-file', type=str, help="Input file for encryption/decryption")
    parser.add_argument('--output-file', type=str, help="Output file for encryption/decryption")
    parser.add_argument('--param-file', type=str, default="encryption_params.pkl", help="File to save/load encryption parameters")
    args = parser.parse_args()

    try:
        # Parameters
        n = 1024  # Dimension for better security
        m = 1024  # Dimension for better security
        q = 2**31 - 1  # Prime modulus
        sigma = 3.2  # Standard deviation for Gaussian noise

        if args.action in ['encrypt-message', 'encrypt-file']:
            # Generate LWE instance
            A, b, s, e = generate_lwe_instance(n, m, q, sigma)

            if args.action == 'encrypt-message':
                if not args.message:
                    raise ValueError("Message must be provided for encryption")
                message = np.frombuffer(args.message.encode(), dtype=np.uint8).astype(np.int64) % q
                padded_message = pad_message(message, n)
                ciphertext, r = encrypt_message(A, padded_message, q)
                with open(args.param_file, "wb") as f:
                    pickle.dump((A, b, s, e, r, ciphertext), f)
                print("Ciphertext:", ciphertext)
                print("Random vector r:", r)
                print(f"Encryption parameters saved to {args.param_file}")

            elif args.action == 'encrypt-file':
                if not args.input_file or not args.output_file:
                    raise ValueError("Input and output files must be provided for encryption")
                encrypt_file(args.input_file, args.output_file, A, q, sigma)
                with open(args.param_file, "wb") as f:
                    pickle.dump((A, b, s, e), f)
                print(f"Encryption parameters saved to {args.param_file}")

        elif args.action in ['decrypt-message', 'decrypt-file']:
            with open(args.param_file, "rb") as f:
                params = pickle.load(f)

            if args.action == 'decrypt-message':
                if len(params) == 6:
                    A, b, s, e, r, ciphertext = params
                else:
                    raise ValueError("Incorrect number of parameters for message decryption.")
                if not args.message:
                    raise ValueError("Message must be provided for decryption")
                decrypted_message = decrypt_message(A, ciphertext, r, q)
                decrypted_text = ''.join([chr(x) for x in decrypted_message if x < 256])
                print("Decrypted message:", decrypted_text)

            elif args.action == 'decrypt-file':
                if len(params) == 4:
                    A, b, s, e = params
                else:
                    raise ValueError("Incorrect number of parameters for file decryption.")
                if not args.input_file or not args.output_file:
                    raise ValueError("Input and output files must be provided for decryption")
                decrypt_file(args.input_file, args.output_file, A, q)
                print(f"File decrypted and saved to {args.output_file}")

    finally:
        try:
            # Clear sensitive data from memory
            clear_sensitive_data(A, b, s, e)
        except NameError:
            # If any variable is not defined due to an earlier error, skip clearing
            pass

if __name__ == "__main__":
    main()
