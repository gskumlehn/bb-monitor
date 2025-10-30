from app.interfaces.enum_interface import EnumInterface

class SocialMediaSource(EnumInterface):
    MICRO_INFLUENCER = "Micro-Influenciador (> 10mil seguidores)"
    MACRO_INFLUENCER = "Macro-Influenciador (>100 mil seguidores)"
    MEGA_INFLUENCER = "Mega-Influenciador (> de 1 milhão de seguidores)"
    RELEVANT_PROFILE_TOP_VOICE = "Perfil Relevante/ Top Voice"
    BB_IMAGE_OR_VIDEO = "Imagem/Vídeo do BB"
    NICHE_PUBLISHER = "Publicador de Nicho"
