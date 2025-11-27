from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text, String, ARRAY
from app.enums.mention_category_parent_name import MentionCategoryParentName
from app.enums.mention_category_name import MentionCategoryName

Base = declarative_base()

class Mention(Base):
    __tablename__ = "mention"
    __table_args__ = {"schema": "bb_monitor"}

    url = Column(Text, primary_key=True, nullable=False)
    _category_parent_names = Column("category_parent_names", ARRAY(String), nullable=True)
    _category_names = Column("category_names", ARRAY(String), nullable=True)

    @property
    def category_parent_names(self) -> list[MentionCategoryParentName]:
        return [MentionCategoryParentName.from_name(name) for name in self._category_parent_names or []]

    @category_parent_names.setter
    def category_parent_names(self, parents: list[MentionCategoryParentName]):
        self._category_parent_names = [parent.name for parent in parents] if parents else []

    @property
    def category_names(self) -> list[MentionCategoryName]:
        return [MentionCategoryName.from_name(name) for name in self._category_names or []]

    @category_names.setter
    def category_names(self, names: list[MentionCategoryName]):
        self._category_names = [name.name for name in names] if names else []
