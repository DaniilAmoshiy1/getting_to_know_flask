from data.datamodel.model_base import SqlAlchemyBase
from .session import CafeSession


def reset_db():
    SqlAlchemyBase.metadata.drop_all(CafeSession.engine)


def setup_db():
    SqlAlchemyBase.metadata.create_all(CafeSession.engine)
