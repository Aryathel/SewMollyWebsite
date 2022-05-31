from wtforms import ValidationError

from db.models import User


def user(*, exists: bool = True):
    if exists:
        error = "That {} is not recognized."
    else:
        error = "That {} is already taken."

    def check_user(form, field):
        name_or_email = field.data

        user_from_name = User.get_by_name(name_or_email)
        user_from_email = User.get_by_email(name_or_email)

        if not exists:
            if user_from_name is not None:
                raise ValidationError(error.format("username"))
            elif user_from_email is not None:
                raise ValidationError(error.format("email"))

        else:
            if not user_from_name and not user_from_email:
                raise ValidationError(error.format("username or email"))

        return True

    return check_user


def user_password(form, field):
    if form.user:
        if form.user.check_password(field.data):
            return
        raise ValidationError("That password is incorrect.")
