from flask_security import RoleMixin, UserMixin, AsaList
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.mutable import MutableList
from .db import db
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.user_id'))
    role_id = Column('role_id', Integer(), ForeignKey('roles.role_id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    role_id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))
    permissions = Column(MutableList.as_mutable(AsaList()), nullable=True)

    def get_id(self):
        return str(self.role_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=True)
    password = Column(String(80), nullable=True)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(64), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    # jobs = relationship('Job', backref='user', lazy=True)

    def get_id(self):
        return str(self.user_id)


# class Job(db.Model):
#     __tablename__ = 'jobs'
#     job_id = Column(Integer, primary_key=True)
#     status = Column(Enum('Applied', 'Interviewing',
#                          'Offered', 'Failed'), nullable=True)
#     company_name = Column(String(80), nullable=True)
#     role = Column(String(80), nullable=True)
#     apply_date = Column(DateTime, nullable=True)
#     last_updated_date = Column(DateTime, nullable=False)
#     important_info = Column(String(500), nullable=False)
#     url = Column(String(255), nullable=True)
#     salary_expectation = Column(Integer, nullable=False)
#     user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
