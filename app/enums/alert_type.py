from app.interfaces.enum_interface import EnumInterface

class AlertType(EnumInterface):
    PRESS = "Imprensa"
    SOCIAL_MEDIA = "Rede Social"

    @classmethod
    def csv_to_type_list_by_values(cls, csv: str):
        return [cls(value) for value in csv.split(",") if value]

    @classmethod
    def csv_to_type_list_by_names(cls, csv: str):
        return [cls.from_name(name) for name in csv.split(",") if name]

    @classmethod
    def type_list_to_csv_by_values(cls, types: list):
        return ",".join([type_.value for type_ in types])
