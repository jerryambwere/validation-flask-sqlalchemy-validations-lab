from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10),nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('phone_number')
    def validate_phone_number(self,key,phone_number):
        if not phone_number.isdigit() or len(phone_number) !=10:
            raise ValueError(
                "Phone number must be exactly 10 digits"
            )
        return phone_number
    
    @validates('name')
    def validate_name(self,jey,name):
        if not name:
            raise ValueError("Name can't be empty")
        if db.session.query(Author).filter_by(name=name).first():
            raise ValueError(f"Author with '{name}' already exists")
        return name
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String(250))
    summary = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self,key,content):
        if len(content) < 250:
            raise ValueError(" Content must be atleast 250 characters long")
        return content
    
    @validates('summary')
    def validate_summary(self,key,summary):
        if len(summary)>250:
            raise ValueError("Summary must not exceed 250 characters")
        return summary
    
    @validates('category')
    def validate_category(self,key,category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'")
        return category
    
    @validates('title')
    def validate_title(self,key,title):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in title for keyword in clickbait_keywords):
            raise ValueError("Title must be clickbait -y ")
        return title
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
