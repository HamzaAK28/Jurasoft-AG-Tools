import re
import os

# Updated regex patterns to handle variations
generic_patterns = [
    r'\b(?:[A-Za-z]{3})?[A-WYZ]{0,2}\d*[A-WYZ]*X[A-WYZ]*\d*(?:X[A-WYZ]*\d*)*X+[A-WYZ]*\d*(?:-\d+)?\b',
    r'\b([A-Za-z]{1}[A-Z]*)-([\w]+)\b',
]

# Function to find and replace generic patterns in a given text
def find_generic_patterns(text):
    generic_patterns_result = []
    for pattern in generic_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            matched_text = match.group()
            # Add "|" before and after the matched pattern
            text = text.replace(matched_text, f"|{matched_text}|")
            generic_patterns_result.append(f"|{matched_text}|")

    return generic_patterns_result, text

# Function to count generic patterns in a given text
def count_generic_pattern(text):
    generic_counts = sum(len(re.findall(pattern, text)) for pattern in generic_patterns)
    return generic_counts

def calculate_percentage_similarity(count1, count2):
    if count1 == count2:
        return 100.0
    return min(count1, count2) / max(count1, count2) * 100.0

def compare_patterns(manual_results, trained_results):
    missing_patterns_dict = {}

    # Compare patterns and find the missing ones in trained results
    missing_in_trained = [pattern for pattern in manual_results if pattern not in trained_results]
    if missing_in_trained:
        missing_patterns_dict['missing_in_trained'] = missing_in_trained

    # Compare patterns and find the missing ones in manual results
    missing_in_manual = [pattern for pattern in trained_results if pattern not in manual_results]
    if missing_in_manual:
        missing_patterns_dict['missing_in_manual'] = missing_in_manual

    return missing_in_manual, missing_in_trained

def process_folders(manual_text_folder, trained_text_folder, missing_patterns_manual_text, missing_patterns_trained_text):
    manual_files = os.listdir(manual_text_folder)
    trained_files = os.listdir(trained_text_folder)

    manual_results = []  # Store manual results
    trained_results = []  # Store trained results
    summary_text = []  # Store the summary text

    missing_patterns_dict = {}  # Store missing patterns

    all_manual_texts = ""  # Variable to store all manual texts
    all_trained_texts = ""  # Variable to store all trained texts

    for i, (manual_file, trained_file) in enumerate(zip(manual_files, trained_files)):
        with open(os.path.join(manual_text_folder, manual_file), 'r', encoding='utf-8-sig') as manual_f:
            manual_text = manual_f.read()
        with open(os.path.join(trained_text_folder, trained_file), 'r', encoding='utf-8-sig') as trained_f:
            trained_text = trained_f.read()

        # Find and replace generic patterns in manual text
        manual_generic_patterns, updated_manual_text = find_generic_patterns(manual_text)
        manual_generic_count = len(manual_generic_patterns)
        manual_results.append(f"File {i + 1} (Manual Text): {manual_file}")
        manual_results.append(f"Count of Generic Patterns: {manual_generic_count}")
        manual_results.extend(manual_generic_patterns)
        manual_results.append("---------")
        all_manual_texts += updated_manual_text  # Add the updated text to the variable

        # Find and replace generic patterns in trained text
        trained_generic_patterns, updated_trained_text = find_generic_patterns(trained_text)
        trained_generic_count = len(trained_generic_patterns)
        trained_results.append(f"File {i + 1} (Trained Text): {trained_file}")
        trained_results.append(f"Count of Generic Patterns: {trained_generic_count}")
        trained_results.extend(trained_generic_patterns)
        trained_results.append("---------")
        all_trained_texts += updated_trained_text  # Add the updated text to the variable

        # Calculate the percentage similarity
        percentage_similarity = calculate_percentage_similarity(manual_generic_count, trained_generic_count)

        # Add percentage similarity to the summary_text
        summary_text.append(f"File Pair {i + 1} - {manual_file} vs {trained_file}: {percentage_similarity}%")

        # Compare patterns and find the missing ones
        missing_patterns = compare_patterns(manual_generic_patterns, trained_generic_patterns)
        if missing_patterns:
            missing_patterns_dict[f"File Pair {i + 1} - {manual_file} vs {trained_file}"] = missing_patterns

    return manual_results, trained_results, summary_text, missing_patterns_dict, all_manual_texts, all_trained_texts
