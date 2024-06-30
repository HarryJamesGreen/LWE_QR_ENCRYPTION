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

Given a matrix \( A \in \mathbb{Z}_q^{n \times m} \) and a vector \( s \in \mathbb{Z}_q^m \), the goal is to find \( s \) given \( A \) and \( b = As + e \), where \( e \) is a small error vector. Mathematically, the problem is to solve \( b = As + e \). The security of LWE relies on the difficulty of solving this equation, especially when the error vector \( e \) is small and the dimension \( n \) is large.

### Key Generation

1. Choose a random matrix \( A \in \mathbb{Z}_q^{n \times m} \).
2. Choose a secret vector \( s \in \mathbb{Z}_q^m \).
3. Generate a small error vector \( e \in \mathbb{Z}_q^n \).
4. Compute \( b = (As + e) \mod q \).

### Encryption

1. Choose a random vector \( r \in \mathbb{Z}_q^n \).
2. Compute the ciphertext \( c = (A^T r + m) \mod q \).

### Decryption

1. Compute \( A^T r \).
2. Recover the message \( m = (c - A^T r) \mod q \).

## Installation

To run the code, you need to have Python and the necessary libraries installed. You can install the required libraries using pip:

```bash
pip install numpy scipy
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/LWE-Cryptography.git
cd LWE-Cryptography
```

2. Run the python script:
 ```
python lwe_encryption.py
```

## Example output
```
 Matrix A:
 [[47155 52929 56115 ... 56787  3981 16389]
 [41602   153 26370 ... 18047 11774 59422]
 [22709 20554 18615 ...  3644 27440 59837]
 ...
 [65142  2831 35494 ...  1781 26443 61604]
 [20712  4955  3447 ... 61003 28127 33689]
 [65396 34080 37728 ...  9575 27011 39065]]
Vector b:
 [50859 32961 26843 53769 45936 24100 29937 34589 28732 20152  2152 38055
  7959 30053 19179 41050 47932 44186 29339 26945 13626 14843  9978 30490
 53990 27811 15892 61863 30824 41203 26193 56328 52228 63762  1638 13311
 15265 33256 24529 52388 34427 12013 64686 54438  2216 50351 24867  2521
 15393 31008]
Secret vector s:
 [51274 24317 29688 27376 33903 22787 33302  5274 59619  3311 61472 11808
 24538  8948  2008 61868 15105 41291 21948  8486 25142 62710  9960 21952
    62  2562  3097 24409 18129 36642 55860 33461 11857  2730 41097 61466
 38811 24195 22304 49921  1640 56269 31909 27654 57452   677 20500 63293
  9961 42986]
Error vector e:
 [65536 65533 65536     0 65534     2     4 65536     0     1 65534     3
     3     3 65534 65535     0     3     1 65533     3     1     0     5
     0     0 65532     1 65532 65532     5     3     3     0 65533     4
     0     6     3     2     2 65535     8     5 65535     1     1 65536
 65535 65536]
Original message:
 [23937 34307 60275 50920   131 32113 59980  3115 41365 25354 29983 42848
 30479 49762 28285 24909 50466 42954 17902  9784   271 51235 50625  2631
  8736 33996 59537   822 31582 28745 57461 39376 31167 29104 16943 37435
 53296  4895 20932 36871 47143 37665 46870 39762 39643 15688 42366  4960
  2078 41581]
Ciphertext:
 [55701 14169  6662 24130 48250 50624 51987 38546 42228 42967 52941 25656
 24378 58697 26209 27441 45760 47039 26594 28924 57738  1760  3566 21475
 55858 49899 53486 41395 37905 20332 62136 58877  8814 63446 57545  8984
 17544 21674 60241 63877 19278 40402 55543 63994 35179  2257 50247 57914
 33505  7508]
Decrypted message:
 [23937 34307 60275 50920   131 32113 59980  3115 41365 25354 29983 42848
 30479 49762 28285 24909 50466 42954 17902  9784   271 51235 50625  2631
  8736 33996 59537   822 31582 28745 57461 39376 31167 29104 16943 37435
 53296  4895 20932 36871 47143 37665 46870 39762 39643 15688 42366  4960
  2078 41581]
Decryption successful!
