FROM mambaorg/micromamba:1.2.0

# Set the working directory in the container
WORKDIR /app

COPY environment.yml .
RUN micromamba env create -f environment.yml -n ercot_env && \
    micromamba clean --all --yes

# Copy the current directory contents into the container at /app
COPY . .
COPY credentials-api-project.json /opt/conda/envs/ercot_env/bin/credentials-api-project.json

# Make RUN commands use the new environment:
SHELL ["micromamba", "run", "-n", "ercot_env", "/bin/bash", "-c"]

# Make port 8080 available to the world outside this container
EXPOSE 8050

# Define an environment variable
ENV APP_MODE=Production

# Ensure the environment is activated:
CMD ["micromamba", "run", "-n", "ercot_env", "gunicorn", "app:server", "--bind", "0.0.0.0:8050"]
