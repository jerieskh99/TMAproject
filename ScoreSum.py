import os

# Function to search for specific strings in a file and calculate the score
def search_strings_in_file(file_path, search_strings, string_scores):
    score = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        if "score_file" in file_path:
            return 'NA'
        if  len(content) == 0:
            return 'NA'
        if "The server refused the connection" in content:
            return 'NA'
        if "The page timed out while trying to load the URL" in content:
            return 'NA'
        if "There was an unexpected error" in content:
            return 'NA'
        if "This site cannot be reached" in content:
            return 'NA'
        



        for string, string_score in zip(search_strings, string_scores):
            if string not in content:
                score += string_score
    return score

# Function to process each subdirectory and calculate scores for each file
def process_directory(directory_path):
    search_strings = ['No ad trackers found on this site.', 'No third-party cookies found.',
                       'Session recording services not found on this website.', 'Tracking that evades cookie blockers wasn\'t found.', 'We did not find this website capturing keystrokes.',
                       'Facebook Pixel not found on this website.', 'Google Analytics\' "remarketing audiences" feature not found.' ]
    string_scores = [2, 2, 4, 3, 4, 1, 1]

    scores = []

    for subdir, dirs, files in os.walk(directory_path):
        subdir_scores = []
        for file in files:
            file_path = os.path.join(subdir, file)
            file_score = search_strings_in_file(file_path, search_strings, string_scores)
            subdir_scores.append(file_score)
        
        scores.append((subdir, subdir_scores))

    return scores

# Function to calculate the average score
def calculate_average(scores):
    filtered_scores = [score for score in scores if score != 'NA']
    return sum(filtered_scores) / len(filtered_scores) if filtered_scores else 0

# Function to save the scores and their average in a file for each subdirectory
def save_scores(scores):
    for subdir, subdir_scores in scores:
        score_file_path = os.path.join(subdir, 'score_file.txt')
        with open(score_file_path, 'w', encoding='utf-8') as score_file:
            # Write individual scores
            score_file.write(' '.join(map(str, subdir_scores)) + '\n')
            # Calculate and write the average score
            average_score = calculate_average(subdir_scores)
            score_file.write(str(average_score))
            score_file.write('\n'+str(len(subdir_scores)))

# Main execution
directory_path = r'C:\Users\fiore\Desktop\All gov websites' 
scores = process_directory(directory_path)
save_scores(scores)
