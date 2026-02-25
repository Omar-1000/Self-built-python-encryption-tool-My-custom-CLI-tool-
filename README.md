# OmarCrypto 🔐

**OmarCrypto** is a self-developed Python encryption tool packaged as an installable CLI utility.

It implements an enhanced classical Rail Fence approach combined with:

- Rail Fence zigzag distribution (configurable depth)
- Per-rail Caesar cipher transformation
- Key-derived deterministic rail shuffling
- Optional rail direction reversal (left / right)

> ⚠️ Educational cryptography tool based on classical ciphers. Not intended for real-world secure communication.

---

## Installation (from GitHub)

```bash
pip install git+https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
```

---

## Basic Usage

### Encrypt

```bash
omarcrypto enc -t "helloworld" -d 3 -k "secret" --direction right
```

Example output:

```
RF3|right|9|0.1.2::uxqmafunxu
```

---

### Decrypt

```bash
omarcrypto dec -c "RF3|right|9|0.1.2::uxqmafunxu" -k "secret"
```

Output:

```
helloworld
```

---

## Command Structure

OmarCrypto follows a structured CLI format:

```
omarcrypto <command> [options]
```

Available commands:

- `enc` → Encrypt plaintext
- `dec` → Decrypt ciphertext

---

## Parameters Explained

### `-t, --text`
Plaintext input for encryption.

### `-d, --depth`
Number of rails used in the Rail Fence transformation.  
Must be ≥ 2.

### `-k, --key`
Secret key used to:
- Derive Caesar shift value
- Generate deterministic shuffle seed

Using the same key is required for successful decryption.

### `--direction`
Controls rail reading direction:
- `left` (default)
- `right` (reverses each rail)

### `-c, --cipher`
Ciphertext input for decryption.

---

## Internal Design Overview

OmarCrypto performs encryption in multiple stages:

1. Zigzag distribution of characters across rails.
2. Caesar transformation applied per rail.
3. Optional rail reversal.
4. Deterministic shuffle of rails derived from the provided key.
5. Concatenation into final ciphertext with embedded metadata.

The metadata header ensures accurate reconstruction during decryption.

---

## Project Structure

```
src/
└── omarcrypto/
    ├── core.py
    ├── cli.py
    └── __init__.py
```

---

## Author

Omar Ayesh  
Cybersecurity & Cryptography Enthusiast
