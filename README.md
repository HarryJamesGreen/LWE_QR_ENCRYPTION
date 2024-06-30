# Learning With Errors (LWE) Cryptography

This repository contains a Python implementation of the Learning With Errors (LWE) encryption and decryption scheme, a fundamental concept in lattice-based cryptography. This implementation demonstrates key generation, encryption, and decryption processes, showcasing the mathematical foundations of post-quantum cryptographic algorithms.

## Table of Contents
- [Learning With Errors (LWE) Cryptography](#learning-with-errors-lwe-cryptography)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Mathematical Foundations](#mathematical-foundations)
    - [Learning With Errors (LWE) Problem](#learning-with-errors-lwe-problem)
    - [Key Generation](#key-generation)
    - [Encryption](#encryption)
    - [Decryption](#decryption)
  - [Installation](#installation)
  - [Usage](#usage)

## Overview

Lattice-based cryptography relies on the hardness of certain lattice problems, such as the Shortest Vector Problem (SVP) and Learning With Errors (LWE). These problems are believed to be resistant to attacks by both classical and quantum computers. The LWE problem forms the basis of various cryptographic protocols, including encryption schemes that are secure against quantum attacks.

## Features

- **Key Generation**: Generate random matrix `A`, secret vector `s`, and error vector `e`. Compute the public vector `b`.
- **Encryption**: Encrypt a message `m` using the public matrix `A` and a random vector `r`.
- **Decryption**: Decrypt the ciphertext using the secret vector `s` and recover the original message.

## Mathematical Foundations

### Learning With Errors (LWE) Problem

Given a matrix `A ∈ ℤ_q^{n × m}` and a vector `s ∈ ℤ_q^m`, the goal is to find `s` given `A` and `b = As + e`, where `e` is a small error vector. Mathematically, the problem is to solve `b = As + e`. The security of LWE relies on the difficulty of solving this equation, especially when the error vector `e` is small and the dimension `n` is large.

### Key Generation

1. Choose a random matrix `A ∈ ℤ_q^{n × m}`.
2. Choose a secret vector `s ∈ ℤ_q^m`.
3. Generate a small error vector `e ∈ ℤ_q^n`.
4. Compute `b = (As + e) mod q`.

### Encryption

1. Choose a random vector `r ∈ ℤ_q^n`.
2. Compute the ciphertext `c = (A^T r + m) mod q`.

### Decryption

1. Compute `A^T r`.
2. Recover the message `m = (c - A^T r) mod q`.

## Installation

To run the code, you need to have Python and the necessary libraries installed. You can install the required libraries using pip:

```bash
pip install numpy scipy
```

## Usage

Encrypting and Decrypting Messages
Encrypt a Message:

```bash
python lwe_qr_file_encrypt.py --action encrypt-message --message "Your message here" --param-file encryption_params.pkl
```

This command will encrypt the provided message and save the encryption parameters to encryption_params.pkl.
Decrypt a Message:

```bash
python lwe_qr_file_encrypt.py --action decrypt-message --message "Ciphertext from 
encryption step" --param-file encryption_params.pkl

```

Use the exact ciphertext saved from the encryption step for decryption.
Encrypting and Decrypting Files
Encrypt a File:

```bash
python lwe_qr_file_encrypt.py --action encrypt-file --input-file yourfile.txt 
--output-file encrypted.pkl --param-file encryption_params.pkl

```

This command will encrypt the contents of yourfile.txt and save the encrypted data to encrypted.pkl.
Decrypt a File:

```bash
python lwe_qr_file_encrypt.py --action decrypt-file --input-file encrypted.pkl 
--output-file decrypted.txt --param-file encryption_params.pkl

```

This command will decrypt the contents of encrypted.pkl and save the decrypted data to decrypted.txt.