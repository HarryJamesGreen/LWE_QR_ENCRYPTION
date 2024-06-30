# Learning With Errors (LWE) Cryptography

This repository contains a Python implementation of the Learning With Errors (LWE) encryption and decryption scheme, a fundamental concept in lattice-based cryptography. This implementation demonstrates key generation, encryption, and decryption processes, showcasing the mathematical foundations of post-quantum cryptographic algorithms.

## Overview

Lattice-based cryptography relies on the hardness of certain lattice problems, such as the Shortest Vector Problem (SVP) and Learning With Errors (LWE). These problems are believed to be resistant to attacks by both classical and quantum computers. The LWE problem forms the basis of various cryptographic protocols, including encryption schemes that are secure against quantum attacks.

## Features

- **Key Generation**: Generate random matrix `A`, secret vector `s`, and error vector `e`. Compute the public vector `b`.
- **Encryption**: Encrypt a message `m` using the public matrix `A` and a random vector `r`.
- **Decryption**: Decrypt the ciphertext using the secret vector `s` and recover the original message.

## Mathematical Foundations

### Learning With Errors (LWE) Problem

Given a matrix \( A \in \mathbb{Z}_q^{n \times m} \) and a vector \( s \in \mathbb{Z}_q^m \), the goal is to find \( s \) given \( A \) and \( b = As + e \), where \( e \) is a small error vector. Mathematically, the problem is to solve \( b = As + e \). The security of LWE relies on the difficulty of solving this equation, especially when the error vector \( e \) is small and the dimension
