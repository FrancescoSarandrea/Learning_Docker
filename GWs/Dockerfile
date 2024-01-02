FROM python:3.8

# Install Jupyter and other dependencies
RUN pip install jupyter gwpy pandas

# Install additional system dependencies for GWpy
RUN apt-get update && apt-get install -y \
    libfftw3-dev \
    libhdf5-dev \
    libgsl-dev

# Install PyTorch
RUN pip install torch==1.9.0
#+cpu torchvision==0.10.0+cpu torchaudio==0.9.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Set the working directory
WORKDIR /app

# Copy the notebook into the container
COPY WaveFormEncoder.ipynb /app/

# Expose the Jupyter notebook port
EXPOSE 8888

# Command to run Jupyter notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
