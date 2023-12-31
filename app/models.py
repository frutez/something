from __future__ import annotations
from flask_admin.contrib.sqla import ModelView
from .extentions import db, admin


class DatabaseMethod:
    @classmethod
    def get_paginate(cls, page, per_page):
        product = cls.query.paginate(page=page, per_page=per_page)
        return product


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(100))


class Category(db.Model, DatabaseMethod):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug_name = db.Column(db.String(100), unique=True)
    image_url = db.Column(db.String(255))
    subcategories = db.relationship('Subcategory', back_populates='category')

    def __repr__(self):
        return self.name


class Subcategory(db.Model, DatabaseMethod):
    __tablename__ = 'subcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug_name = db.Column(db.String(100), unique=True)
    image_url = db.Column(db.String(255))
    category_id = db.Column(db.ForeignKey('category.id'), nullable=False)

    category = db.relationship("Category", back_populates='subcategories')
    product = db.relationship('Products', back_populates='subcategory')

    def __repr__(self):
        return self.name


class Products(db.Model, DatabaseMethod):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug_name = db.Column(db.String(100), unique=True)
    image_small = db.Column(db.String(255))
    image_medium = db.Column(db.String(255))
    image_large = db.Column(db.String(255))
    price = db.Column(db.Integer)
    subcategory_id = db.Column(db.ForeignKey('subcategory.id'), nullable=False)
    subcategory = db.relationship('Subcategory', back_populates='product')

    def __repr__(self):
        return self.name


class SubcategoryPost(ModelView):
    form_columns = ['name', 'slug_name', 'image_url', 'category']
    column_list = ['name', 'slug_name', 'image_url', 'category']


class ProductPost(ModelView):
    form_columns = ['name', 'slug_name', 'image_small', 'image_medium',
                    'image_large', 'price', 'subcategory']
    column_list = ['name', 'slug_name', 'image_small', 'image_medium',
                   'image_large', 'price', 'subcategory']


admin.add_views(ModelView(Category, db.session),
                SubcategoryPost(Subcategory, db.session),
                ProductPost(Products, db.session))
