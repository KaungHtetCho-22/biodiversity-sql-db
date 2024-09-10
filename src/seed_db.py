import os
import json
from model import create_session, AudioAnalysis, SpeciesCounts
from datetime import datetime

# # Function to insert data into the database for a single JSON data entry
# def insert_data_from_json(json_data):
#     session = create_session()

#     # Extract general information
#     iot_id = json_data["iot_id"]
#     date_str = json_data["date"]
#     analysis_date = datetime.strptime(date_str, "%Y%m%d").date()  # Parse the date

#     # Create a new AudioAnalysis record
#     # total_segments = len(json_data["species"][0])
#     audio_analysis = AudioAnalysis(iot_id=iot_id, analysis_date=analysis_date)

#     # Add the AudioAnalysis entry to the session
#     session.add(audio_analysis)
#     session.flush()  # Flush to get the audio_analysis.id for foreign key relationship

#     # Loop over the species data and create SpeciesClassification entries
#     for segment_data in json_data["species"]:
#         for segment_time, classification_data in segment_data.items():
#             species_class = classification_data["Class"]
#             score = classification_data["Score"]

#             # Create a new SpeciesClassification record
#             species_classification = SpeciesClassification(
#                 audio_id=audio_analysis.id,
#                 segment_time=segment_time,
#                 species_class=species_class,
#                 score=score
#             )

#             # Add the SpeciesClassification entry to the session
#             session.add(species_classification)

#     # Commit the transaction to save the records to the database
#     session.commit()
#     session.close()

# # Function to recursively traverse the directory structure and process all .json files
# def insert_data_from_nested_folders(root_folder):
#     for iot_folder in os.listdir(root_folder):  # Traverse IOT folders
#         iot_folder_path = os.path.join(root_folder, iot_folder)
#         if os.path.isdir(iot_folder_path):  # Check if it's a directory
#             for date_folder in os.listdir(iot_folder_path):  # Traverse date folders
#                 date_folder_path = os.path.join(iot_folder_path, date_folder)
#                 if os.path.isdir(date_folder_path):  # Check if it's a directory
#                     for filename in os.listdir(date_folder_path):  # Process JSON files
#                         if filename.endswith(".json"):  # Only process .json files
#                             json_file_path = os.path.join(date_folder_path, filename)
#                             print(f"Processing file: {json_file_path}")
#                             with open(json_file_path, 'r') as f:
#                                 try:
#                                     json_data = json.load(f)
#                                     insert_data_from_json(json_data)
#                                 except json.JSONDecodeError as e:
#                                     print(f"Error parsing {json_file_path}: {e}")
#                                 except Exception as e:
#                                     print(f"Error processing {json_file_path}: {e}")

# # Root folder containing the IOT folders (replace with the actual path)
# root_folder = "input"

# # Insert data from all nested JSON files in the folder structure into the database
# insert_data_from_nested_folders(root_folder)

# Function to add analysis data to the database
def add_analysis_data(file_path):
    # Extract iot_id and date from filename
    filename = os.path.basename(file_path)
    iot_id, date_str = filename.split('_')[0], filename.split('_')[1].split('_')[0]
    analysis_date = datetime.strptime(date_str, "%Y%m%d").date()

    # Load JSON data
    with open(file_path) as f:
        species_data = json.load(f)

    # Create session
    session = create_session()

    # Add audio_analysis record
    audio_analysis = AudioAnalysis(iot_id=iot_id, analysis_date=analysis_date)
    session.add(audio_analysis)
    session.commit()

    # Add species_counts records
    for species, count in species_data.items():
        species_count = SpeciesCounts(audio_id=audio_analysis.id, species_name=species, analysis_date=analysis_date, count=count)
        session.add(species_count)

    session.commit()

# Example usage
file_path = "IOT6_20240808_species_counts.json"
add_analysis_data(file_path)

