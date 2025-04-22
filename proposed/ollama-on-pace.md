# Setting Up Ollama on PACE ICE Cluster

## Document Metadata
* **Author**: Alejandro Gomez
* **Date Created**: 2025-04-21
* **Last Updated**: 2025-04-21
* **Applicable Clusters**: ICE

## Overview

This guide provides instructions for setting up Ollama on the Georgia Tech PACE ICE Cluster, based on our successful deployment process. Ollama allows you to run large language models locally on PACE's GPUs.

## Prerequisites

- Access to a PACE ICE Cluster node
- Sufficient storage space in your scratch directory (check with `pace-quota`)

## Installation Steps

### 1. Download and Extract Ollama

```bash
# Navigate to your scratch directory
cd ~/scratch

# Download Ollama
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz

# Extract the archive
tar -xzf ollama-linux-amd64.tgz

# Make the binary executable
chmod +x bin/ollama
```

### 2. Set Up the Ollama Storage Directory

#### Why Use a Symlink?

By default, Ollama stores all its data in the `~/.ollama` directory in your home folder. This includes:
- Model files (which can be 40-80 GB+ each)
- Manifests, fingerprints, server state, etc.

Since your home directory on PACE has a small quota (typically only 30GB), attempting to download and use models without redirecting storage to the scratch directory (which has a larger quota, typically 300GB) would quickly fill up your home directory and cause "disk quota exceeded" errors.

#### Creating the Symlink

We'll use your scratch directory to store the Ollama models:

```bash
# Create a directory for Ollama models in your scratch space
mkdir -p ~/scratch/.ollama_models

# Remove any existing .ollama symlink in your home directory
rm -f ~/.ollama

# Create a symlink from ~/.ollama to your scratch directory
ln -s ~/scratch/.ollama_models ~/.ollama
```

This symbolic link tricks Ollama into thinking it's writing to `~/.ollama` when it's actually writing to `~/scratch/.ollama_models`, thus using your scratch storage allocation instead of your home directory.


### 3. Add Ollama to Your PATH

Add the Ollama binary to your PATH by editing your `~/.bashrc` file:

```bash
# Add this line to your ~/.bashrc
echo 'export PATH="$HOME/scratch/bin:$PATH"' >> ~/.bashrc

# Source the updated .bashrc
source ~/.bashrc
```

## Running Ollama

### Start the Ollama Server

```bash
ollama serve
```

This will start the Ollama server and generate a new SSH key pair if needed. You should see output indicating that Ollama has detected available GPUs.

### Pull and Run Models

In a separate terminal session:

```bash
# Pull a model (example: Llama 3.1)
ollama pull llama3.1:8b

# Run the model
ollama run llama3.1:8b
```

## Troubleshooting

### Disk Quota Exceeded

If you encounter a "disk quota exceeded" error when pulling models, check your storage usage:

```bash
pace-quota
du -sh ~/scratch/*
```

You may need to free up space in your scratch directory. The most common issue is trying to download large models when your scratch directory is nearly full.

### Broken Symlink

If you see errors about broken symlinks or messages like:
```
Couldn't find '/home/hice1/agomez302/.ollama/id_ed25519'. Generating new private key.
Error: could not create directory mkdir /home/hice1/agomez302/.ollama: file exists
```

Check if your symlink is pointing to the correct location:

```bash
# Check the symlink
ls -l ~/.ollama
file ~/.ollama
```

If it's broken or points to a non-existent location (e.g., `/scratch/.ollama_models` instead of `/home/hice1/agomez302/scratch/.ollama_models`), recreate it with the correct path:

```bash
# Remove the broken symlink
rm ~/.ollama

# Create a directory for Ollama models if it doesn't exist
mkdir -p ~/scratch/.ollama_models

# Create a new symlink with the correct absolute path
ln -s ~/scratch/.ollama_models ~/.ollama

# Generate a new SSH key if needed. This should happen automatically but just in case...
ssh-keygen -t ed25519 -f ~/.ollama/id_ed25519 -N ""
```

It's important to use the full absolute path in the symlink to avoid issues with path resolution.


### Server Access Issues

## Storage Considerations

LLM models can be quite large. For reference:
- llama3.1:8b is around 4.7GB
- llama3.3:latest is around 42GB

Be mindful of your quota limits (typically 300GB for scratch space).

## Hardware Information

When running Ollama on the ICE cluster, you'll have access to powerful hardware, such as:
- NVIDIA H200 GPUs (139.8 GiB VRAM each)
- CUDA 12.5 drivers

## Additional Commands

```bash
# List downloaded models
ollama list

# Show system information
ollama -v

# Get help with Ollama commands
ollama --help
```

## Notes

- The current Ollama version is 0.6.0 as of March 2025
- Models are stored in `~/scratch/.ollama_models/`
- Ollama automatically utilizes available GPUs

Sample Structure afterwards:
```bash
[agomez302@atl1-1-03-014-30-0 scratch]$ pwd
/home/hice1/agomez302/scratch
[agomez302@atl1-1-03-014-30-0 scratch]$ tree
.
├── bin
│   └── ollama
├── lib
│   └── ollama
│       ├── cuda_v11
│       │   ├── libcublasLt.so.11 -> libcublasLt.so.11.5.1.109
│       │   ├── libcublasLt.so.11.5.1.109
│       │   ├── libcublas.so.11 -> libcublas.so.11.5.1.109
│       │   ├── libcublas.so.11.5.1.109
│       │   ├── libcudart.so.11.0 -> libcudart.so.11.3.109
│       │   ├── libcudart.so.11.3.109
│       │   └── libggml-cuda.so
│       ├── cuda_v12
│       │   ├── libcublasLt.so.12 -> libcublasLt.so.12.8.4.1
│       │   ├── libcublasLt.so.12.8.4.1
│       │   ├── libcublas.so.12 -> libcublas.so.12.8.4.1
│       │   ├── libcublas.so.12.8.4.1
│       │   ├── libcudart.so.12 -> libcudart.so.12.8.90
│       │   ├── libcudart.so.12.8.90
│       │   └── libggml-cuda.so
│       ├── libggml-base.so
│       ├── libggml-cpu-alderlake.so
│       ├── libggml-cpu-haswell.so
│       ├── libggml-cpu-icelake.so
│       ├── libggml-cpu-sandybridge.so
│       └── libggml-cpu-skylakex.so
└── ollama-linux-amd64.tgz

5 directories, 22 files
[agomez302@atl1-1-03-014-30-0 scratch]$ ls -la
total 1678836
drwx------.   5 agomez302 gtperson      12288 Mar 27 01:18 .
drwxr-xr-x. 310 root      root          20480 Mar 11 12:53 ..
drwxr-xr-x.   2 agomez302 gtperson       4096 Mar 27 00:20 bin
drwxr-xr-x.   3 agomez302 gtperson       4096 Mar 27 00:20 lib
-rw-r--r--.   1 agomez302 gtperson 1719074860 Mar 26 23:58 ollama-linux-amd64.tgz
drwxr-xr-x.   3 agomez302 gtperson       4096 Mar 27 01:41 .ollama_models
[agomez302@atl1-1-03-014-30-0 scratch]$ ls .ollama_models/
history  id_ed25519  id_ed25519.pub  models
[agomez302@atl1-1-03-014-30-0 scratch]$ ls .ollama_models/models/
blobs  manifests
[agomez302@atl1-1-03-014-30-0 scratch]$ 
```
