from app.interfaces.enum_interface import EnumInterface

class AlertType(EnumInterface):
    PRESS = "Imprensa"
    SOCIAL_MEDIA = "Rede Social"

    @staticmethod
    def values_csv_to_type_list(csv: str):
        return [AlertType(value.strip()) for value in csv.split(",") if value.strip()]
