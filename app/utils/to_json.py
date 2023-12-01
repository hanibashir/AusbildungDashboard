from flask import jsonify


def row_to_json(row):
    print(row.to_dict())
    return jsonify(row.to_dict())


def rows_to_json(rows):
    rows_list = [row.to_dict() for row in rows]
    return jsonify(rows_list)


def message_to_json(msg, status):
    return jsonify(
        {
            "message": msg,
            "status": status
        }
    )
