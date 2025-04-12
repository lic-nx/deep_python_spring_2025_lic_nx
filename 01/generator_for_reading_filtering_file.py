def filtered_file_reader(filename, find_words, stop_words):
    find_words = set(word.lower()
                    for item in find_words for word in item.split())
    stop_words = set(word.lower()
                    for item in stop_words for word in item.split())
    if isinstance(filename, str):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line_words = set(line.lower().split())
                if find_words & line_words and not stop_words & line_words:
                    yield line.strip()
    elif hasattr(filename, "read"):
        for line in filename:
            line_words = set(line.lower().split())
            if find_words & line_words and not stop_words & line_words:
                yield line.strip()
    else:
        raise ValueError(
            "Аргумент должен быть либо именем файла, "
            "либо файловым объектом"
        )
