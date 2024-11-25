
# TreasureBook API

## Overview

TreasureBook is a dynamic, graph-based platform that enables adventurers to connect treasures, locations, and maps, similar to the architecture used by Facebook's TAO. This project involves building and deploying the TreasureBook API using **Flask**, **MongoDB**, **Docker**, and **Kubernetes**.

The goal is to deploy and manage the API and MongoDB, with autoscaling and performance monitoring to handle high traffic during treasure hunts.

## Features

- **Graph-based architecture**: Nodes for treasures, locations, and maps; Edges for relationships (trails, hidden locations, leads to).
- **API Endpoints**:
  - **POST `/node`**: Add treasures, locations, or maps.
  - **POST `/edge`**: Add trails, map leads, or hidden-at relationships.
  - **GET `/status`**: Check if the API is running.
- **Deployment**: Deployed using **Docker** and **Kubernetes**, with Horizontal Pod Autoscaler (HPA) to handle dynamic scaling.

## Requirements

- **Python**: 3.9 or higher
- **Docker**
- **Kubernetes Cluster**
- **MongoDB** (Dockerized)

## Project Structure

```
TreasureBook/
│
├── app/
│   ├── app.py                   # Flask API code
│   ├── requirements.txt         # Python dependencies
│
├── docker/
│   ├── Dockerfile               # Dockerfile to containerize the API
│
├── kubernetes/
│   ├── api-deployment.yaml      # Kubernetes deployment for the API
│   ├── mongo-deployment.yaml    # Kubernetes deployment for MongoDB
│   ├── api-service.yaml         # Service to expose the API
│   ├── mongo-service.yaml       # Service to expose MongoDB
│   ├── hpa.yaml                 # Horizontal Pod Autoscaler configuration
│
├── README.md                    # Documentation for the project
└── scripts/
    ├── simulate_traffic.py      # Script to simulate API traffic
    ├── monitor_scaling.py       # Script to monitor resource usage and scaling
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd TreasureBook
```

### 2. Install Python Dependencies

Install the required Python libraries:

```bash
cd app
pip install -r requirements.txt
```

### 3. Dockerize the API

Build and run the Docker container for the API:

```bash
# Build Docker image
docker build -t treasurebook-api .

# Run Docker container
docker run -d -p 5000:5000 --name treasurebook-api treasurebook-api
```

### 4. Run MongoDB in Docker

Run MongoDB in a separate container (for local setups):

```bash
docker run -d -p 27017:27017 --name treasurebook-mongo mongo
```

### 5. Deploy on Kubernetes

1. **Apply Kubernetes Manifests**:

```bash
kubectl apply -f kubernetes/mongo-deployment.yaml
kubectl apply -f kubernetes/api-deployment.yaml
kubectl apply -f kubernetes/hpa.yaml
```

2. **Expose API Service**:

```bash
kubectl apply -f kubernetes/api-service.yaml
```

3. **Check Pods and Services**:

```bash
kubectl get pods
kubectl get services
```

4. **Access API**:

Use `NodePort` to access the API:
```
http://<NodeIP>:30001/status
```

### 6. Traffic Simulation

Use the `simulate_traffic.py` script to simulate high traffic to the API:

```bash
python scripts/simulate_traffic.py
```

### 7. Monitor Scaling

Monitor the Horizontal Pod Autoscaler (HPA) behavior during high traffic:

```bash
kubectl get hpa treasurebook-api-hpa --watch
```

## Performance Monitoring

1. **CPU and Memory Usage**: Use `kubectl top pods` to monitor resource usage.

2. **Scaling Metrics**: Use the `kubectl describe hpa` to observe scaling behavior.

3. **Logs**: Use `kubectl logs -f <pod-name>` to monitor API pod logs in real-time.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
