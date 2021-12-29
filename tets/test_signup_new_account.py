from data.project import random_string


def test_signup_new_account(app):
    username = random_string("user_", 10)
    password = "test"
    email = username + "@localhost"
    app.james.ensure_user_exist(username, password)
    app.signup.new_user(username, email, password)
    app.session.login(username, password)
    assert app.session.is_loggined_in_as(username)
