from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    @validates("name")
    def validate_name(self, key, name):
        names = db.session.query(Author.name).all()
        if not name:
            raise ValueError("Name field is required.")
        elif name in names:
            raise ValueError("Name must be unique.")
        return name
    
    @validates("phone_number")
    def validate_phone_number(self, key, number):
        if len(number) != 10:
            raise ValueError("Number must be 10 digits.")
        return number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    @validates("content", "summary")
    def validate_length(self, key, string):
        if(key == 'content'):
            if len(string) <= 250:
                raise ValueError("Post content must be greater that 250 characters.")
        if(key == 'summary'):
            if len(string) >= 250:
                raise ValueError("Post summary must be less or equal to 250 characters.")
        return string

    @validates('category')
    def validate_category(self, key, category):
        if (category != 'Fiction' and category != 'Non-Fiction'):
            raise ValueError("Category must be Fiction or Non-Fiction.")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(string in title for string in clickbait):
            raise ValueError("Not clickbait-y enough. Make it better.")
        return title
    
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
