from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(401)
def error_401(error):
    context = {
        'code': 401,
        'description': 'Вы не в системе! Авторизуйтесь или пройдите регистрацию.'
    }
    return render_template('errors/error.html', error=context), 401


@errors.app_errorhandler(404)
def error_404(error):
    context = {
        'code': 404,
        'description': 'Извините, но такая страница не найдена :('
    }
    return render_template('errors/error.html', error=context), 404


@errors.app_errorhandler(403)
def error_403(error):
    context = {
        'code': 403,
        'description': 'У Вас нет прав доступа. Пожалуйста, проверьте свой аккаунт и повторите попытку'
    }
    return render_template('errors/403.html', error=context), 403


@errors.app_errorhandler(500)
def error_500(error):
    context = {
        'code': 500,
        'description': 'Что-то пошло не так. Попробуйте позже. Приносим извинения.'
    }
    return render_template('errors/500.html', error=context), 500
