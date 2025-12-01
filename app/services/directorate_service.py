from app.repositories.mention_repository import MentionRepository
from app.constants.mailing_constants import MailingConstants
from app.enums.directorate_codes import DirectorateCode

class DirectorateService:

    def list_categories_for_urls(self, alert):
        category_names = MentionRepository.list_categories_for_urls(alert.urls)
        return self.get_directorates_by_categories(category_names)

    def get_directorates_by_categories(self, category_names: list[str]) -> list[str]:
        category_to_directorate_map = MailingConstants.CATEGORY_TO_DIRECTORATE_MAP
        directorates = {DirectorateCode.DIRIS, DirectorateCode.DICOI, DirectorateCode.OUVIDORIA}

        for category in category_names:
            directorate_list = category_to_directorate_map.get(category)
            if directorate_list:
                for directorate in directorate_list:
                    directorates.add(directorate)

        return [directorate.name for directorate in list(directorates)]
