def line_column_threshold(dynamic, static, line_threshold=0, column_threshold=0):
    result = (abs(int(static['line']) - int(dynamic['Line'])) <= line_threshold) \
             and (abs(int(static['column']) - int(dynamic['Column'])) <= column_threshold)

    return result


def static_name_in_dynamic(dynamic, static, line_threshold=0, column_threshold=0):
    """
    dynamic: 64.   | SendStream.prototype.error     | lib.send.SendStream.prototype.error    | 364     | 29  | 4    | 3
    static:  9.    | <anonymous>.error              | index.error                            | 235     | 29  | 3    | 1
    """

    # no threshold
    if line_threshold == 0 and column_threshold == 0:
        return static['name'].lower().split('.')[-1] in dynamic['Name'].lower()

    # with threshold
    result = static['name'].lower().split('.')[-1] in dynamic['Name'].lower() and abs(
        int(static['line']) - int(dynamic['Line'])) <= line_threshold and abs(
        int(static['column']) - int(dynamic['Column'])) <= column_threshold

    return result