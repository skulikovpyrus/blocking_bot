from utils import get_token, get_form, get_field_id_by_code, get_flat_fields, get_field_value_by_id


class BlockingBot:
    def __init__(self, task, settings):
        self.task = task
        self.task_fields = get_flat_fields(self.task["fields"], is_form=False)
        self.settings = settings
        self.login = self.settings["login"]
        self.secret = self.settings["secret"]
        self.token = get_token(self.login, self.secret)

        self.form = get_form(self.task["form_id"], self.token)
        self.field_pairs = self.settings["field_pairs"]

    def check_fields(self):
        for date, checkmark in self.field_pairs:
            date_field_id = get_field_id_by_code(date, self.form, self.task["id"], self.token)
            checkmark_field_id = get_field_id_by_code(checkmark, self.form, self.task["id"], self.token)

            date_value = get_field_value_by_id(self.task_fields, date_field_id)
            print(date_value)

    def main(self):
        pass
