# # Stage 1: Build environment
# FROM gcc:latest as builder

# # Install CMake and other necessary build tools
# RUN apt-get update && \
#     apt-get install -y cmake build-essential && \
#     rm -rf /var/lib/apt/lists/*

# # Set the working directory inside the container
# WORKDIR /app

# # Copy the source code into the container
# COPY . .

# # Create a build directory and configure CMake
# RUN cmake -S . -B build

# # Build the project
# RUN cmake --build build -j --config Release

# # Stage 2: Runtime environment (optional, for smaller final image)
# FROM debian:stable-slim

# # Copy the built executable from the builder stage
# COPY --from=builder /app/build/your_executable_name /usr/local/bin/

# # Set the entry point to run the executable
# CMD ["/usr/local/bin/your_executable_name"]