FROM klakegg/hugo:0.101.0-ext-ubuntu

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3 /usr/bin/python

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app/

# Make scripts executable
RUN chmod +x /app/notion_hugo_app.py /app/run_hugo.py

# Install Python dependencies
RUN pip3 install --no-cache-dir \
    pyyaml \
    python-dotenv \
    notion-client \
    fs \
    tabulate 
    
# Create directory for temporary files
RUN mkdir -p /app/data/error_temp

# Set the entrypoint to the notion_hugo_app.py script
ENTRYPOINT ["python", "/app/notion_hugo_app.py"]

# Default command is to run Hugo server after processing
CMD ["--hugo-args=server --bind=0.0.0.0"]
