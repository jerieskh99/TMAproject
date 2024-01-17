import os
import shutil


def move_files_based_on_string_match(input_directory, string_map):
    # Create directories for each string name, if they don't exist
    for string_name in string_map.keys():
        os.makedirs(os.path.join(input_directory, string_name), exist_ok=True)

    session_id_dir = "sessionTracking"
    os.makedirs(os.path.join(input_directory, session_id_dir), exist_ok=True)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_directory):
        file_path = os.path.join(input_directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Check for each string in the map if it exists in the file
            for string_name, string_data in string_map.items():
                if string_data in content:
                    # Move file to the directory with the name matching the string name
                    dest_dir = os.path.join(input_directory, string_name)
                    shutil.copy(file_path, os.path.join(dest_dir, filename))
                    break  # Assuming one file should be moved to only one directory

            negation_session = "Session recording services not found on this website"
            if negation_session not in content:
                dest_dir = os.path.join(input_directory, session_id_dir)
                shutil.copy(file_path, os.path.join(dest_dir, filename))


# Example usage
input_directory = '/Users/jeries/PycharmProjects/simpleCrawler/output_rapid/3/_txt'
string_map = {
    'adTracker': 'Ad tracker found on this site',
    'thirdPartyCookies': 'Third-party cookies found',
    'trackers': 'This website loads trackers on your computer that are designed to evade third-party cookie blockers',
    'googleAnal': 'This site allows Google Analytics to follow you across the internet',
    'facebookPixel': 'When you visit this site, it tells Facebook',
    'keyCaptureMouseClicks': 'This website could be monitoring your keystrokes and mouse clicks.',
    'doubleclick_net': 'doubleclick.net',
    'google_analytics_com': 'google-analytics.com',
    'google_com': 'google.com',
    'googleapis_com': 'googleapis.com',
    'googletagmanager_com': 'googletagmanager.com',
    'googlesyndication_com': 'googlesyndication.com',
    'hotjar_com': 'hotjar.com',
    'youtube_com': 'youtube.com',
    'adobedtm_com': 'adobedtm.com',
    'demdex_net': 'demdex.net',
    'everesttech_net': 'everesttech.net',
    'omtrdc_net': 'omtrdc.net',
    'azure_com': 'azure.com',
    'addthis_com': 'addthis.com'
}


if __name__ == "__main__":
    move_files_based_on_string_match(input_directory, string_map)

