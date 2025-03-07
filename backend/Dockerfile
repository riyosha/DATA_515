# Use Miniconda as the base image
FROM conda/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the environment.yml file and install dependencies
COPY environment.yml .
RUN conda env create -f environment.yml

# Activate the environment
SHELL ["conda", "run", "-n", "letterboxd", "/bin/bash", "-c"]

# Copy the source code
COPY . .

# Expose the backend port
EXPOSE 5515

# Command to run the application
CMD ["conda", "run", "--no-capture-output", "-n", "letterboxd", "python", "src/main.py"]
