from wtforms import ValidationError

from db.models import User


def user(*, exists: bool = True):
    if exists:
        error = "That {} is not recognized."
    else:
        error = "That {} is already taken."

    def check_user(form, field):
        name_or_email = field.data

        user_from_name = User.query.filter_by(username=name_or_email).first()
        if not exists and user_from_name is not None:
            raise ValidationError(error.format("username"))

        user_from_email = User.query.filter_by(email=name_or_email).first()
        if not exists and user_from_email is not None:
            raise ValidationError(error.format("email"))

        if exists and not user_from_name and not user_from_email:
            raise ValidationError(error.format("username or email"))

        return True

    return check_user


def user_password(form, field):
    if form.user:
        if form.user.check_password(field.data):
            return
        raise ValidationError("That password is incorrect.")
