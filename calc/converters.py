from .models import Day


class IsoToDayConverter:
    regex = r'\d\d\d\d-\d\d-\d\d'

    def to_python(self, value: str) -> Day:
        return Day.fromisoformat(value)

    def to_url(self, value: Day) -> str:
        return value.isoformat()
