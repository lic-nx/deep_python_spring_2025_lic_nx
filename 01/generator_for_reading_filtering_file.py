import re


def find_any_match(s, elements):
    if not elements:
        return False
    # Создаем регулярное выражение для поиска целых слов
    pattern = (
        r"(?:\b|^)(?:"
        + "|".join(re.escape(element) for element in elements)
        + r")(?:\b|$)"
    )
    # Ищем первое вхождение в строке
    return bool(re.search(pattern, s))


def process_lines(lines, stop_words, find_words):
    for line in lines:
        line_lower = line.lower()
        if not find_any_match(line_lower, stop_words):
            if find_any_match(line_lower, find_words):
                yield line.strip()


def filtered_file_reader(filename, find_line, stop_line):
    find_words = set(item.lower().strip() for item in find_line)
    stop_words = set(item.lower().strip() for item in stop_line)
    if isinstance(filename, str):
        with open(filename, "r", encoding="utf-8") as file:
            yield from process_lines(file, stop_words, find_words)
    elif hasattr(filename, "read"):
        yield from process_lines(filename, stop_words, find_words)
    else:
        raise ValueError(
            "Аргумент должен быть либо именем файла, либо файловым объектом"
        )
