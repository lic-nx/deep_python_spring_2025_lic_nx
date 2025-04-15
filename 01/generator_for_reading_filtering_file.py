import re


def find_any_match(s, elements):
    if len(elements) < 1:
        return False
    # Создаем регулярное выражение для поиска целых слов
    pattern = (
        r"(?:\b|^)(?:"
        + "|".join(re.escape(element) for element in elements)
        + r")(?:\b|$)"
    )
    # Ищем первое вхождение в строке
    return bool(re.search(pattern, s))


def filtered_file_reader(filename, find_words, stop_words):
    find_words = set(item.lower().strip() for item in find_words)
    stop_words = set(item.lower().strip() for item in stop_words)

    def process_lines(lines):
        for line in lines:
            line_lower = line.lower()
            if not find_any_match(line_lower, stop_words) and find_any_match(
                line_lower, find_words
            ):
                yield line.strip()

    if isinstance(filename, str):
        with open(filename, "r", encoding="utf-8") as file:
            yield from process_lines(file)
    elif hasattr(filename, "read"):
        yield from process_lines(filename)
    else:
        raise ValueError(
            "Аргумент должен быть либо" "именем файла, либо файловым объектом"
        )
