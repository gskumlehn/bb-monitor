from app.infra.database import db
from sqlalchemy.ext.hybrid import hybrid_property
from app.enums.directorate_codes import DirectorateCode

class Mailing(db.Model):
    __tablename__ = "mailing"
    __table_args__ = {"schema": "bb_monitor"}

    email = db.Column(db.String, primary_key=True)
    _directorate_code = db.Column("directorate_code", db.String, primary_key=True)

    @hybrid_property
    def directorate_code(self) -> DirectorateCode:
        return DirectorateCode.from_name(self._directorate_code)

    @directorate_code.setter
    def directorate_code(self, code: DirectorateCode):
        self._directorate_code = code.name

    @directorate_code.expression
    def directorate_code(cls):
        return cls._directorate_code
