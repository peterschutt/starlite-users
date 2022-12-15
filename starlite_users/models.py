from typing import TypeVar
from uuid import uuid4, UUID

from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.orm import Mapped, declarative_mixin, declared_attr, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID


@declarative_mixin
class SQLAlchemyUserModel:
    __tablename__ = 'user'

    id: Mapped[UUID] = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    email: Mapped[str] = Column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = Column(String(1024))
    is_active: Mapped[bool] = Column(Boolean(), nullable=False, default=False)
    is_verified: Mapped[bool] = Column(Boolean(), nullable=False, default=False)

    @declared_attr
    def roles(self):
        return relationship('Role', secondary='user_roles', lazy='joined')


@declarative_mixin
class SQLAlchemyRoleModel:
    __tablename__ = 'role'

    id: Mapped[UUID] = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name: Mapped[str] = Column(String(255), nullable=False, unique=True)
    description: Mapped[str] = Column(String(255), nullable=True)


@declarative_mixin
class UserRoleAssociation:
    __tablename__ = 'user_roles'

    @declared_attr
    def role_id(self):
        return Column(PGUUID(as_uuid=True), ForeignKey('role.id'), nullable=False)

    @declared_attr
    def user_id(self):
        return Column(PGUUID(as_uuid=True), ForeignKey('user.id'), nullable=False)


UserModelType = TypeVar('UserModelType', bound=SQLAlchemyUserModel)
