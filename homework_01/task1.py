class SomeModel:
    def predict(self, message: str) -> float:
        if message == "Чапаев и пустота":
            return 9.9
        return 0.0

    def empty_func(self, a: int):
        return a


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    model = SomeModel()
    if not 0 <= bad_thresholds <= good_thresholds <= 1:
        raise ValueError("Err")
    accuracy_prediction = model.predict(message)
    if good_thresholds <= accuracy_prediction <= 1:
        return "отл"
    if 0 <= accuracy_prediction < bad_thresholds:
        return "неуд"
    if bad_thresholds <= accuracy_prediction <= good_thresholds:
        return "норм"
    raise ValueError("value err")

