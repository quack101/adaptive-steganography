# Diffusion-Based Nested Audio Steganography

This project explores a generative steganography approach for concealing encrypted data within AI-generated multimedia carriers.

The current implementation uses **Riffusion**, a diffusion-based audio generation approach that represents audio as spectrogram images. The project combines generative media, cryptography, error correction, and multi-carrier data hiding.

The primary objective is to generate seemingly normal audio carriers while concealing protected payload data through a nested two-carrier architecture.

---

## Current Architecture

The current pipeline uses two generated carriers:

### Carrier A — Key Carrier

Carrier A is generated using Riffusion as a spectrogram image and converted into an audio waveform.

It stores part of the cryptographic information required to reconstruct the encryption key.

### Carrier B — Payload Carrier

Carrier B is also generated using Riffusion as a spectrogram image.

The encrypted and error-corrected payload is embedded into this carrier before it is converted into audio.

The AES key is split across the two carriers, meaning that both carriers are required to reconstruct the complete key.

---

## Encoding Pipeline

The current encoding process is structured as follows:

```text
Original Payload
      │
      ▼
AES-CBC Encryption
      │
      ▼
Ciphertext + IV
      │
      ▼
Reed-Solomon Error Correction
      │
      ▼
Protected Payload
      │
      ├───────────────────────┐
      │                       │
      ▼                       ▼
Carrier A                 Carrier B
Key Fragment A            Key Fragment B
                              +
                        Protected Payload
      │                       │
      └──────────┬────────────┘
                 ▼
        Riffusion-Generated
         Spectrogram Carriers
                 │
                 ▼
           Audio Output
```

---

## Cryptographic Protection

The payload is protected using:

### AES-CBC

The original payload is encrypted using AES in CBC mode.

This ensures that the hidden content is not directly recoverable even if the embedded data is extracted.

An initialization vector (IV) is used during encryption and is required during decryption.

### Split AES Key

The AES key is divided into two fragments.

```text
AES Key
   │
   ├── First Half ──► Carrier A
   │
   └── Second Half ─► Carrier B
```

The complete key can only be reconstructed when both carriers are available.

### Reed-Solomon Error Correction

Reed-Solomon error correction is applied to the encrypted data before embedding.

This is intended to allow recovery of the payload even when small amounts of embedded data are corrupted during storage, processing, or carrier conversion.

---

## Generative Carrier Creation

The project uses:

```python
MODEL_ID = "riffusion/riffusion-model-v1"
```

Riffusion generates spectrogram-like images using a Stable Diffusion-based pipeline.

The generated image acts as an intermediate representation:

```text
Text Prompt
     │
     ▼
Riffusion / Diffusion Model
     │
     ▼
Generated Spectrogram Image
     │
     ▼
Data Embedding
     │
     ▼
Modified Spectrogram
     │
     ▼
Griffin-Lim Reconstruction
     │
     ▼
WAV Audio Carrier
```

The current implementation therefore uses the generated spectrogram as the embedding medium and converts it into an audio waveform.

---

## Current Embedding Approach

At the current stage, the protected payload data is embedded into the generated Carrier B spectrogram.

The embedding is performed after the Riffusion generation stage.

Conceptually:

```text
Generate Carrier B
        │
        ▼
Riffusion Spectrogram Image
        │
        ▼
Embed Protected Payload
        │
        ▼
Stego Spectrogram
        │
        ▼
Convert to Audio
        │
        ▼
Final Stego Carrier
```

Carrier A similarly serves as a generated carrier for part of the cryptographic key material.

---

## Decoding Pipeline

The decoder performs the reverse operation:

```text
Carrier A + Carrier B
          │
          ▼
Extract Embedded Information
          │
          ▼
Recover Key Fragment A
          +
Recover Key Fragment B
          │
          ▼
Reconstruct AES Key
          │
          ▼
Recover Reed-Solomon Encoded Ciphertext
          │
          ▼
Reed-Solomon Error Correction
          │
          ▼
AES-CBC Decryption
          │
          ▼
Original Payload
```

Both carriers are required for successful reconstruction of the complete encryption key and recovery of the payload.

---

## Technologies Used

* Python
* PyTorch
* Hugging Face Diffusers
* Riffusion
* Stable Diffusion Pipeline
* NumPy
* Pillow
* Librosa
* SoundFile
* PyCryptodome
* Reed-Solomon

---

## Current Status

The project has progressed through the following stages:

* [x] Generation of audio carriers using Riffusion-generated spectrograms
* [x] Conversion of generated spectrograms into WAV audio
* [x] Two-carrier architecture
* [x] Payload encryption using AES-CBC
* [x] Initialization vector handling
* [x] Reed-Solomon error correction for the encrypted payload
* [x] Split AES key architecture
* [x] Distribution of AES key fragments across Carrier A and Carrier B
* [x] Payload embedding into the generated carrier representation
* [x] Initial encoding and decoding pipeline development

---

## Current Research Direction

The current implementation primarily performs data embedding **after the diffusion model generates the spectrogram**.

The next stage of the research is to investigate whether the embedding itself can be moved into the **diffusion model's latent representation**, allowing the generative process to directly produce a carrier containing the protected information.

The main challenge is reliable recovery.

A potential research direction is therefore to investigate:

```text
Protected Payload
        │
        ▼
Diffusion Latent Space
        │
        ▼
Generated Spectrogram
        │
        ▼
Audio Carrier
```

followed by reliable reverse recovery:

```text
Audio Carrier
        │
        ▼
Spectrogram Representation
        │
        ▼
Latent Recovery / Inversion
        │
        ▼
Protected Payload
```

This direction builds upon the existing implementation while shifting the steganographic operation from post-generation embedding toward generative latent-space steganography.

---

## Project Goal

The overall goal is to develop a robust generative steganography framework that combines:

* Diffusion-based carrier generation
* Audio-based information hiding
* Multi-carrier or nested architectures
* Cryptographic protection
* Error correction
* Reliable payload recovery

The current implementation serves as the baseline system from which the next iteration of the research will explore architectural and deep-learning-based improvements.
