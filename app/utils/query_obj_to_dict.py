

def row_to_dict(row):
    return row.to_dict()


def rows_to_dict(rows):
    rows_list = [row.to_dict() for row in rows]
    return rows_list
