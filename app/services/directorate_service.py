from app.constants.mailing_constants import MailingConstants
from app.enums.directorate_codes import DirectorateCode

class DirectorateService:

    def get_directorates_by_subcategories(self, subcategories: list[str]) -> list[str]:
        subcategory_to_directorate_map = MailingConstants.SUBCATEGORY_TO_DIRECTORATE_MAP
        directorates = {DirectorateCode.DIRIS, DirectorateCode.DICOI, DirectorateCode.OUVIDORIA}

        for subcategory in subcategories:
            directorate_list = subcategory_to_directorate_map.get(subcategory)
            if directorate_list:
                for directorate in directorate_list:
                    directorates.add(directorate)

        return [directorate.name for directorate in list(directorates)]
