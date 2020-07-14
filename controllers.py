"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner

from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url
from . models import get_user_email, get_time

url_signer = URLSigner(session)

# The auth.user below forces login.
@action('index')
@action.uses(url_signer, auth.user, 'index.html')
def index():
    return dict(
        # This is an example of a signed URL for the callback.
        # See the index.html template for how this is passed to the javascript.
        #callback_url = URL('callback', signer=url_signer),
        get_notes_url = URL('get_notes', signer=url_signer),
        add_note_url = URL('add_note', signer=url_signer),
        delete_note_url = URL('delete_note', signer=url_signer),
        get_star_url = URL('get_star', signer=url_signer),
        set_star_url = URL('set_star', signer=url_signer),
        get_color_url = URL('get_color', signer=url_signer),
        set_color_url = URL('set_color', signer=url_signer),
        user_email = get_user_email(),
    )

@action('get_notes')
@action.uses(url_signer.verify(), auth.user, db)
def get_posts():
    # Complete.
    star_notes = db((db.note.user_email == auth.current_user.get('email')) & (db.note.important == 1)).select(orderby=~db.note.ts).as_list() # Just to keep code from breaking.
    non_star_notes = db((db.note.user_email == auth.current_user.get('email')) & (db.note.important == 0)).select(orderby=~db.note.ts).as_list()
    notes = star_notes + non_star_notes
    return dict(notes=notes)

@action('add_note', method="POST")
@action.uses(url_signer.verify(), db)
def add_post():
    # Complete.
    note_id = db.note.insert(
        note_title = request.json.get('note_title'), 
        note_text = request.json.get('note_text')
    )
    return dict(note_id=note_id) # You need to fill this in.

@action('delete_note', method="POST")
@action.uses(url_signer.verify(), db)
def delete_post():
    id = request.json.get('id')
    if id is not None:
        db(db.note.id == id).delete()


@action('get_star')
@action.uses(url_signer.verify(), db, auth.user)
def get_star():
    note_id = request.params.get('note_id')
    assert note_id is not None
    important_entry = db(db.note.id == note_id).select().first()
    important = important_entry.rating if important_entry is not None else 0
    return dict(important=important)


@action('set_star', method='POST')
@action.uses(url_signer.verify(), db, auth.user)
def set_star():
    note_id = request.json.get('note_id')
    important = request.json.get('important')
    
    assert note_id is not None and important is not None
    db.note.update_or_insert(
        (db.note.id == note_id),
        important=important,
        ts=get_time()
    )

@action('set_color', method='POST')
@action.uses(url_signer.verify(), db, auth.user)
def set_color():
    note_id = request.json.get('note_id')
    color = request.json.get('color')
    
    assert note_id is not None and color is not None
    db.note.update_or_insert(
        (db.note.id == note_id),
        color=color,
    )

@action('get_notes', method="POST")
@action.uses(db, auth.user)  # etc.  Put here what you need.
def save_note():
    id = request.json.get('note_id')
    note_title = request.json.get('note_title')
    note_text = request.json.get('note_text')
    db(db.note.id == id).update(note_title=note_title, note_text=note_text, ts=get_time())
    return dict(note_title=note_title, note_text=note_text, id=id)