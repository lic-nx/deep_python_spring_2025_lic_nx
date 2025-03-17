def filtered_file_reader(filename, find_words, stop_words):
    find_words = set(word.lower() for word in find_words)
    stop_words = set(word.lower() for word in stop_words)

    with open(filename, 'r') as file:
        line = file.readline()
        line_words = set(line.lower().split())
        if find_words & line_words and not (stop_words & line_words):
            yield line