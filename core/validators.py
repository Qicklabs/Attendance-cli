import re

from config.typedef import CONFIG


class Validator:
    @staticmethod
    def validate_domain_name(domain_name: str):
        return re.match(CONFIG.DOMAIN_PATTERN, domain_name) is not None

    @staticmethod
    def validate_email(email: str):
        return re.match(CONFIG.EMAIL_PATTERN, email)

    @staticmethod
    def validate_int_choice(choice, limit):
        return choice.isdigit() and 1 > int(choice) > limit

