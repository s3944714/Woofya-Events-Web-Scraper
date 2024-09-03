output_file = "libraries.output.txt"

with open(output_file, "w") as file:
    try:
        import bs4
        import requests
        import boto3
        import pandas as pd
        import sqlalchemy
        import flask

        file.write("All libraries imported successfully!\n")
        print("All libraries imported successfully! Output written to libraries.output.txt")
    except ImportError as e:
        error_message = f"An error occurred: {e}\n"
        file.write(error_message)
        print(error_message)
