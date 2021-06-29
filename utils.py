import requests
import hashlib
import hmac
import json


def get_token(login, secret):
    data = {"login": login, "security_key": secret}
    url = "https://api.pyrus.com/v4/auth"
    response = requests.post(
        url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print(response.text)


def get_form(form_id, token):
    url = f"https://api.pyrus.com/v4/forms/{form_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        form = response.json()
        return form
    else:
        print(response.text)


def get_task(task_id, token):
    url = f"https://api.pyrus.com/v4/tasks/{task_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        task = response.json()
        return task["task"]
    else:
        print(response.text)


def send_comment(task_id, token, comment):
    url = f"https://api.pyrus.com/v4/tasks/{task_id}/comments"
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        data=json.dumps(comment)
    )
    if not response.status_code == 200:
        return response


def get_flat_fields(fields, is_form=True):
    res = []
    if not fields:
        return res
    for field in fields:
        res.append(field)
        prop_name = "info" if is_form else "value"

        if field["type"] == "table" and is_form:
            res.extend(field[prop_name]["columns"])
        if field["type"] == "title":
            res.extend(field[prop_name]["fields"])
    return res


def get_field_by_id(fields: list, _id: int):
    field = [field for field in fields if field["id"] == _id]
    if field:
        return field[0]


def get_field_id_by_code(form, code, source_task_id, token):
    flat_fields = [field for field in get_flat_fields(form["fields"]) if "info" in field]
    fields_with_code = list(filter(lambda x: "code" in x["info"], flat_fields))

    field_id = [field["id"] for field in fields_with_code if field["info"]["code"] == code]
    if field_id:
        return field_id[0]

    comment = {"text": f"Не найдено поле по коду {code}, проверьте правильно ли вы ввели код поля"}
    send_comment(source_task_id, token, comment)


def get_field_ids(form, codes, source_task_id, token):
    field_ids = {}
    for code in codes:
        field_ids[code] = get_field_id_by_code(form, code, source_task_id, token)
    return field_ids


def get_field_value_by_id(fields, field_id):
    filtered_fields = [field for field in fields if field["id"] == field_id]
    if filtered_fields:
        field = filtered_fields[0]
        if "value" in field:
            field_value = field["value"]
            if field["type"] == "multiple_choice":
                return field_value["choice_names"][0]

            return field_value


def _is_signature_correct(message, secret, signature):
    secret = str.encode(secret)
    digest = hmac.new(secret, msg=message, digestmod=hashlib.sha1).hexdigest()
    return hmac.compare_digest(digest, signature.lower())
