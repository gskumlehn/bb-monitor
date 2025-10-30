from app.interfaces.enum_interface import EnumInterface

class PressSource(EnumInterface):
    ONE_RELEVANT_VEHICLE = ">= 1 Veículo Relevante"
    THREE_RELEVANT_VEHICLES = "+3 Veículos Relevantes"
    GROUP_B = "Grupo B (15 à 50 milhões de acesso/mês)"
    GROUP_A = "Grupo A (acima de 50 milhões de acesso/mês"
    MENTIONS_BB_IN_TITLE = "Cita BB no título"
    MENTIONS_BB_IN_SUBTITLE = "Cita BB no subtítulo"
    BB_IMAGE_OR_VIDEO = "Imagem/ Vídeo do BB"
    NICHE_PUBLISHER = "Publicador de Nicho"
