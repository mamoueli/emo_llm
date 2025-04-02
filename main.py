def main(testing = False, testing_num = 3):
    # Load JSON data
    with open('modified_json_file.json', 'r') as file:
        data = json.load(file)
    # Process each top-level structure in the JSON
    # Determine the items to iterate over based on the testing flag
    items_to_process = list(data.items())[:testing_num] if testing else data.items()

    for conversation_id, conversation_data in items_to_process:
        if "dialog" in conversation_data:
            process_conversation(conversation_id, conversation_data)
    # Save the updated data back to JSON
    with open('final_results_v3_gpt.json', 'w') as file:
        json.dump(data, file, indent=4)


#testing=True to run
