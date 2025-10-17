from app.repositories.last_consumed_row_repository import LastConsumedRowRepository

class LastConsumedRowService:

    def get_last_consumed_row_value(self) -> int:
        repository = LastConsumedRowRepository()
        return repository.load_value()

    def update_last_consumed_row(self, new_value: int):
        repository = LastConsumedRowRepository()
        current_value = repository.load_value()

        if new_value < current_value:
            raise ValueError(f"O novo valor ({new_value}) não pode ser menor que o valor atual ({current_value}).")

        repository.update(new_value)
