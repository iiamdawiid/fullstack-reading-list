from . import reading_list_blueprint as r
from flask import request
from flask_jwt_extended import jwt_required, current_user
from ..models import ReadingList, Book
from ..utils import bad_request_if_none

@r.post('/new_reading_list')
@jwt_required()
def handle_create_rl():
    body = request.json

    if body is None:
        response = {
            'message': 'invalid request'
        }
        return response, 400
    
    name = body.get('name')
    if name is None or name == '':
        response = {
            'message': 'invalid response'
        }
        return response, 400
    
    description = body.get('description')

    reading_list = ReadingList(name=name, description=description, created_by=current_user.id)
    reading_list.create()

    response = {
        'message': 'successfully created reading list',
        'reading_list': reading_list.to_response()
    }
    return response, 201

@r.get('/all_reading_lists')
@jwt_required()
def handle_get_rl():
    reading_lists = ReadingList.query.all()
    response = {
        'message': 'reading lists retrieved',
        'reading_lists': [rl.to_response() for rl in reading_lists]
    }
    return response, 200

@r.get('/<rl_id>')
@jwt_required()
def handle_get_one_rl(rl_id):
    reading_list = ReadingList.query.filter_by(id=rl_id).one_or_none()
    if reading_list is None:
        response = {
            'message': 'reading list does not exist'
        }
        return response, 404
    
    response = {
        'message': 'reading list found',
        'reading_list': reading_list.to_response()
    }
    return response, 200

@r.delete('/rl_delete/<rl_id>')
@jwt_required()
def handle_delete_rl(rl_id):
    reading_list = ReadingList.query.filter_by(id=rl_id).one_or_none()
    if reading_list is None:
        response = {
            'message': 'reading list does not exist'
        }
        return response, 404
    
    if reading_list.created_by != current_user.id:
        response = {
            'message': "can not delete another user's reading list"
        }
        return response, 401
    
    reading_list.delete()

    response = {
        'message': 'reading list successfully deleted'
    }
    return response, 200

@r.post('/<rl_id>/add_book')
@jwt_required()
def handle_add_book(rl_id):
    body = request.json

    if body is None:
        response = {
            'message': 'invalid request'
        }
        return response, 400
    
    reading_list = ReadingList.query.filter_by(id=rl_id).one_or_none()
    if reading_list is None:
        response = {
            'message': 'reading list not found'
        }
        return response, 404
    
    if reading_list.created_by != current_user.id:
        response = {
            'message': "can not add books to reading list's that are not yours"
        }
        return response, 401
    
    book_name = body.get('book_name')
    genre = body.get('genre')
    desc = body.get('desc')

    if book_name is None:
        response = {
            'message': 'book name is required'
        }
        return response, 400
    
    book = Book(book_name=book_name, genre=genre, desc=desc, reading_list_id=reading_list.id, added_by=current_user.id)
    book.create()

    reading_list.books.append(book)
    reading_list.update()

    response = {
        'message': 'book added to reading list',
        'reading_list': reading_list.to_response()
    }
    return response, 201

@r.delete('/book_delete/<book_id>')
@jwt_required()
def handle_book_delete(book_id):
    book = Book.query.filter_by(id=book_id).one_or_none()
    if book is None:
        response = {
            'message': 'book does not exist'
        }
        return response, 404
    
    if book.added_by != current_user.id:
        response = {
            'message': "can not delete another user's book"
        }
        return response, 401
    
    book.delete()

    response = {
        'message': 'book successfully deleted'
    }
    return response, 200


# add update book and update reading list
@r.put('/update/book/<book_id>')
@jwt_required()
def handle_book_update(book_id):
    body = request.json

    book = Book.query.filter_by(id=book_id).one_or_none()

    if book is None:
        response = {
            'message': 'book not found'
        }
        return response, 404
    
    if book.added_by != current_user.id:
        response = {
            'message': 'can not update a book that belongs to another user'
        }
        return response, 401
    
    book.book_name = body.get('book_name', book.book_name)
    book.genre = body.get('genre', book.genre)
    book.desc = body.get('desc', book.desc)

    book.update()

    response = {
        'message': 'book successfully updated'
    }
    return response, 200


@r.put('/update/reading_list/<rl_id>')
@jwt_required()
def handle_rl_update(rl_id):
    body = request.json

    reading_list = ReadingList.query.filter_by(id=rl_id).one_or_none()

    if reading_list is None:
        response = {
            'message': 'reading list not found'
        }
        return response, 404
    
    if reading_list.created_by != current_user.id:
        response = {
            'message': 'can not update a reading list that belongs to another user'
        }
        return response, 401
    
    reading_list.name = body.get('name', reading_list.name)
    reading_list.description = body.get('description', reading_list.description)

    reading_list.update()

    response = {
        'message': 'reading list successfully updated'
    }
    return response, 200