from app.interfaces.enum_interface import EnumInterface

class AlertType(EnumInterface):
    PRESS = "Imprensa"
    SOCIAL_MEDIA = "Rede Social"

    @staticmethod
    def values_csv_to_type_list(csv: str):
        return [AlertType(value) for value in csv.split(",") if value]

    @staticmethod
    def names_csv_to_type_list(csv: str):
        return [AlertType.from_name(name) for name in csv.split(",") if name]

    @staticmethod
    def type_list_to_values_csv(types: list):
        return ",".join([type_.value for type_ in types])

