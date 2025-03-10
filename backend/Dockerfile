# Use Miniconda as the base image
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the environment.yml file and install dependencies
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate the environment
RUN echo "conda activate letterboxd" >> ~/.bashrc

# Copy the source code
COPY . .

# Expose the backend port
EXPOSE 5515

# Set entrypoint to ensure Conda environment is always activated
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "letterboxd"]

# Command to run the application
CMD ["python", "src/main.py"]