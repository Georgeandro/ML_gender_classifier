# Gender Prediction Model

This project aims to create a production-ready image recognition application capable of determining the gender (male/female) of a person in a given image. The application uses a pre-trained model from [fastai](https://fast.ai/) and is built and deployed using Docker.

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Model Development](#model-development)
- [Web Application Development](#web-application-development)
  - [Backend Overview](#backend-overview)
  - [APIs Used](#apis-used)
  - [Docker Overview](#docker-overview)
- [Docker Setup](#docker-setup)
- [NGINX Configuration](#nginx-configuration)
- [Installation and Setup](#installation-and-setup)
- [How to Run](#how-to-run)
- [API Usage](#api-usage)
- [Acknowledgments](#acknowledgments)

## Overview

The objective of this project is to create a free-to-use web application where users can upload an image and receive a prediction of the person's gender. The project leverages a pre-trained ResNet50 model from the fastai library and involves building a web application using FastAPI and NGINX for deployment.

## Dataset

The dataset used for training the model was gathered using the DuckDuckGo search engine to obtain images of different genders. The images were then labeled accordingly to train the model.

## Model Development

Using the fastai library, a pre-trained ResNet50 model was fine-tuned with the dataset. This approach leverages transfer learning for better accuracy and efficiency. The model was then exported for use in the web application.

## Web Application Development

### Backend Overview

The backend is developed using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints. The backend handles image uploads and returns predictions using the trained model. Here's an overview of how the backend POST request works:
Follow the steps below to set up a virtual enviroment and download the required python libraries

For Linux/macOS:
-python3 -m venv venv
-source venv/bin/activate

For Windows:
-python -m venv venv
-venv\Scripts\activate

-pip install -r backend/requirements.txt
-pip list

If you want to deactivate the virtual enviroment 
-deactivate



1. **File Upload**: The user uploads an image file to the backend via a POST request.
2. **Image Processing**: The backend reads the image file and converts it into a format suitable for the model.
3. **Model Prediction**: The processed image is passed to the pre-trained model, which predicts the gender.
4. **Response**: The prediction result is returned to the user in JSON format.

### APIs Used

- **FastAPI**: Used to create the web API for handling image uploads and returning predictions.
- **fastai**: Utilized for loading the pre-trained model and making predictions.
- **PIL (Python Imaging Library)**: Used for image processing to prepare the uploaded image for prediction.

### Docker Overview

Docker is used to containerize the application, making it easy to deploy and manage. The project consists of two main Docker containers: one for the backend and one for the frontend.

- **Backend Dockerfile**: This defines the environment for running the FastAPI application, including the necessary Python libraries.
- **Frontend Dockerfile**: This sets up an NGINX server to serve the static HTML frontend.

The `docker-compose.yml` file orchestrates these two containers, ensuring they can communicate with each other and are correctly configured.

## Docker Setup

To set up Docker and Docker Compose, follow these steps:

1. **Install Docker**:
   - **Ubuntu/Debian**:
     ```bash
     sudo apt update
     sudo apt install apt-transport-https ca-certificates curl software-properties-common
     curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
     sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
     sudo apt update
     sudo apt install docker-ce
     ```
   - **Fedora**:
     ```bash
     sudo dnf install docker-ce docker-ce-cli containerd.io
     sudo systemctl start docker
     sudo systemctl enable docker
     ```
   - **macOS**:
     Install Docker Desktop from [Docker Hub](https://www.docker.com/products/docker-desktop).

2. **Install Docker Compose**:
   - **Linux**:
     ```bash
     sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     sudo chmod +x /usr/local/bin/docker-compose
     ```
   - **macOS**:
     Docker Desktop includes Docker Compose, so no additional installation is needed.

## NGINX Configuration

NGINX is used to proxy requests to the backend and frontend services. Follow these steps to configure NGINX:

### Installation

- **Ubuntu/Debian**:
  ```bash
  sudo apt update
  sudo apt install nginx

- **Fedora**:
  ```bash
  sudo dnf update
  sudo dnf install nginx
  brew install nginx

We then create a configuration file for NGINX in the directory /etc/nginx/sites-available/default 

nginx configuration file:
server {
    listen 80;
    server_name localhost;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:8080;  # Proxy to frontend service on port 8080
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://localhost:8000;  # Proxy to backend service on port 8000
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

## Create a symlink to enable the site configuration
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

## Restart NGINX to apply the changes
sudo systemctl restart nginx

##Instalation and Setup

git clone https://github.com/yourusername/ml_project.git
cd ml_project
docker-compose up --build -d


## Check the api usage (in this example we have used port 8000 which is the port for the backend and the file trump.jpg that we will pass
## to the pretrained model in order to recognize if its a man or a woman)
curl -X POST "http://localhost:8000/api/predict" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@trump.jpg"

