from app.models import User, Notebook, Note


def fill(db):
    user = User(name='user', email='user@mail.com')
    user.set_password('pass')

    notebook = Notebook(name='First notebook')
    notebook.user = user
    notebook.user_id = user.id

    note = Note(name='First note', description='Note\'s description')
    note.notebook = notebook
    note.notebook_id = notebook.id
    note.user = user
    note.user_id = user.id

    db.session.add(user)
    db.session.add(note)
    db.session.add(notebook)
    db.session.commit()
