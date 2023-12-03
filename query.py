from moviepy.editor import VideoFileClip
from PIL import Image
import imagehash
import numpy as np
import os
import pickle
import glob

def calculate_hashes(video_path, hash_size=8):
    clip = VideoFileClip(video_path)

    hashes = []

    for frame in clip.iter_frames(fps=1, dtype="uint8"):
        # Convert frame to PIL Image for imagehash
        pil_image = Image.fromarray(frame)
        # Compute hash
        frame_hash = str(imagehash.average_hash(pil_image, hash_size=hash_size))
        hashes.append(frame_hash)

    return np.array(hashes)


def build_database_index(index_file='database_index.pkl'):
    database_index = {}
    database_paths = glob.glob(f"videos/*.mp4")

    for database_path in database_paths:
        video_name = os.path.basename(database_path)
        video_hashes = calculate_hashes(database_path)
        database_index[video_name] = {
            'hashes': video_hashes,
            'length': len(video_hashes)
        }

    with open(index_file, 'wb') as index_file:
        pickle.dump(database_index, index_file)

def load_database_index(index_file='database_index.pkl'):
    with open(index_file, 'rb') as index_file:
        return pickle.load(index_file)

def find_query_in_database(query_path, database_index):
    query_hashes = calculate_hashes(query_path)
    query_length = len(query_hashes)

    min_distance = float('inf')
    best_match_info = None

    for video_name, video_info in database_index.items():
        database_hashes = video_info['hashes']
        database_length = video_info['length']

        for i in range(database_length - query_length + 1):
            # Extract a segment from the database video for comparison
            database_segment = database_hashes[i:i + query_length]

            # Compare the hashes
            hamming_distance = np.count_nonzero(query_hashes != database_segment) / query_length

            if hamming_distance < min_distance:
                min_distance = hamming_distance
                best_match_info = {
                    'video_name': video_name,
                    'match_start_query': 0,
                    'match_start_database': i * 30
                }

    return best_match_info


def find_query_video(query_video_path):
    index_file = 'database_index.pkl'

    if not os.path.exists(index_file):
        build_database_index(index_file)

    database_index = load_database_index(index_file)
    result = find_query_in_database(query_video_path, database_index)

    return result