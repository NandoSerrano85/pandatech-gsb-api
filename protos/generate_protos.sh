#!/bin/bash

cd /app
# Directory containing .proto files
PROTO_DIR="./protos"

# Output directories
PYTHON_OUT="./protos/generated"
JS_OUT="./frontend/src/protos/generated"

# Create output directories
mkdir -p $PYTHON_OUT $JS_OUT

# Generate Python files
protoc -I=$PROTO_DIR --python_out=$PYTHON_OUT $PROTO_DIR/*.proto

# Generate JavaScript files
protoc -I=$PROTO_DIR --js_out=import_style=commonjs,binary:$JS_OUT $PROTO_DIR/*.proto

echo "Proto files generated successfully!"
