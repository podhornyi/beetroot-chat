from flask import Flask

from .views import chat, save_message, login, logout


def register_views(app: Flask):

    app.add_url_rule(
        rule='/chat',
        endpoint='chat',
        view_func=chat,
        methods=['GET', 'POST']
    )

    app.add_url_rule(
        rule='/save_message',
        endpoint='save_message',
        view_func=save_message,
        methods=['POST']
    )

    app.add_url_rule(
        rule='/login',
        endpoint='login',
        view_func=login,
        methods=['GET', 'POST']
    )

    app.add_url_rule(
        rule='/logout',
        endpoint='logout',
        view_func=logout,
        methods=['GET']
    )
