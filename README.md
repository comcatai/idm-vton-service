# IDM-VTON Service

Virtual Try-On service using IDM-VTON model with Streamlit frontend and RunPod deployment.

## Features
- Virtual try-on using IDM-VTON model
- User-friendly Streamlit interface
- RunPod GPU deployment support
- Docker containerization

## Setup

### System Requirements
- NVIDIA GPU (RTX 4000 or better)
- CUDA drivers
- Docker with NVIDIA container toolkit

### Python Setup
1. Ensure Python is in your PATH:
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="/usr/local/bin/python3:$PATH"

# If using a specific Python version
export PATH="/usr/bin/python3:$PATH"
```

2. Verify Python installation:
```bash
python3 --version
which python3
```

3. Install pip if not present:
```bash
sudo apt-get update
sudo apt-get install python3-pip
```

### Installation
1. Clone the repository
2. Build the Docker image:
```bash
docker build -t idm-vton:cuda .
```

3. Install frontend dependencies:
```bash
pip install -r frontend/requirements.txt
```

### Running Locally
1. Start the Docker container:
```bash
docker run --gpus all -p 7860:7860 idm-vton:cuda
```

2. Run the Streamlit frontend:
```bash
cd frontend
streamlit run app.py
```

### RunPod Deployment
1. Push Docker image to registry
2. Create RunPod endpoint/pod using the image
3. Update frontend configuration with endpoint URL

## Project Structure
```
├── docker/              # Docker configuration
├── frontend/           # Streamlit frontend
│   ├── app.py         # Main frontend application
│   └── requirements.txt
├── models/            # Model files and weights
├── src/              # Source code
└── README.md
```

## Environment Variables
- `RUNPOD_API_KEY`: RunPod API key
- `CUDA_VISIBLE_DEVICES`: GPU device selection

## License
[License details]
