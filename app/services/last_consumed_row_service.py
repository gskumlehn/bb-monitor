from app.repositories.last_consumed_row_repository import LastConsumedRowRepository

class LastConsumedRowService:

    def get_value(self) -> int:
        return LastConsumedRowRepository.load_value()

    def update_value(self, new_value: int):
        current_value = LastConsumedRowRepository.load_value()
        if new_value < current_value:
            raise ValueError(
                f"O novo valor ({new_value}) não pode ser menor que o valor atual ({current_value})."
            )
        LastConsumedRowRepository.update_value(new_value)
