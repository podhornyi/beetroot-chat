import json
from flask import (
    render_template, current_app, request, session, redirect, url_for
)

from .db.models import Message


def chat():
    if 'username' not in session:
        return redirect(url_for('login_bla'))

    if request.method == 'POST':
        message = request.form['message']
        if message == '':
            pass
        else:
            current_app.storage.save_message(
                user_name=session['username'],
                message_text=message
            )

    return render_template('chat.html', data=current_app.storage.get_data())


def save_message():
    data = json.loads(request.data.decode())
    message = Message(
        data['name'],
        data['message']
    )
    current_app.storage.save(message)
    return '', 200


def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('chat'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

