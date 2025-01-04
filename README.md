# IDM-VTON Service

Virtual Try-On service using IDM-VTON model with Streamlit frontend and RunPod deployment.

## Features
- Virtual try-on using IDM-VTON model
- User-friendly Streamlit interface
- RunPod GPU deployment support
- Docker containerization

## Setup

### Prerequisites
- Docker
- Python 3.8+
- NVIDIA GPU (for inference)
- RunPod account (for deployment)

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
