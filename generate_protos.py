import os
import subprocess

def generate_protos(proto_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Find all .proto files
    proto_files = []
    for root, _, files in os.walk(proto_dir):
        for file in files:
            if file.endswith('.proto'):
                proto_files.append(os.path.join(root, file))

    if not proto_files:
        print("No .proto files found.")
        return

    # Generate Python code for each .proto file
    for proto_file in proto_files:
        relative_path = os.path.relpath(proto_file, proto_dir)
        output_path = os.path.join(output_dir, os.path.dirname(relative_path))
        os.makedirs(output_path, exist_ok=True)

        command = [
            'python', '-m', 'grpc_tools.protoc',
            f'-I{proto_dir}',
            f'--python_out={output_dir}',
            f'--grpc_python_out={output_dir}',
            proto_file
        ]

        print(f"Generating code for: {relative_path}")
        subprocess.run(command, check=True)

    print("Proto generation complete.")

if __name__ == "__main__":
    proto_dir = 'protos'  # Directory containing your .proto files
    output_dir = 'pythonProtos'  # Directory where generated files will be placed
    generate_protos(proto_dir, output_dir)