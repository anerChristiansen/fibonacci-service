from flask import Blueprint, jsonify, request
from flask import current_app as app

main_blueprint = Blueprint('api', __name__,)


invalid_input_errstr = 'All inputs must be positive integers'
remove_from_blacklist_errstr = 'Index not blacklisted'


def _is_positive_integer(inp):
    return abs(inp)==inp and type(inp)==int


def _get_fibonachi_sequence(index, page=0, pagesize=100):
    # validate inputs
    for inp in (index, page, pagesize):
        if not _is_positive_integer(inp):
            return BaseException(invalid_input_errstr)

    # construct fibonachi sequence up to index
    indexes = list(range(index+1))
    fibonachi_sequence = [0] * (index + 1)
    fibonachi_sequence[1] = 1
    for i in range(2, index+1):
        fibonachi_sequence[i] = fibonachi_sequence[i-1] + fibonachi_sequence[i-2]
    
    # remove blacklsited indexes and fibonachi numbers
    for i in sorted(app.config['BLACKLIST'], reverse=True):
        indexes.pop(i)
        fibonachi_sequence.pop(i)
    
    # perform pagination
    start_idx = page*pagesize
    end_idx = (page + 1)*pagesize
    if start_idx > len(indexes):
        fibonachi_sequence, indexes = [], []
    else:
        if end_idx > len(indexes):
            fibonachi_sequence, indexes = fibonachi_sequence[start_idx:], indexes[start_idx:]
        else:
            fibonachi_sequence, indexes = fibonachi_sequence[start_idx:end_idx], indexes[start_idx:end_idx]

    return indexes, fibonachi_sequence


@main_blueprint.route('/task_1_endpoint', methods=['GET', 'POST'])
def task_1_endpoint():
    """
    Returns the fibonachi number at the given `index`.

    **Parameters**

    `index` [int, positive]: Index in the fibonachi sequence

    **Returns**

    Fibonachi number
    """
    fibonachi_sequence = _get_fibonachi_sequence(**request.get_json())
    if type(fibonachi_sequence)==BaseException:
        return jsonify(str(fibonachi_sequence))
    
    # Does not handle blacklisted numbers
    fibonachi_number = fibonachi_sequence[1][-1]
    return jsonify(fibonachi_number)


@main_blueprint.route('/task_2_endpoint', methods=['GET', 'POST'])
def task_2_endpoint():
    """
    Returns the fibonachi `numbers` and `indexes` up the given `index`. Supports pagination
    through the `page` and `pagesize` parameters.

    **Parameters**

    `index` [int, positive]: Index in the fibonachi sequence

    `page` [int, positive]: Page in the requested fibonachi sequence

    `pagesize` [int, positive]: Size of the page pagination of the fibonachi sequence

    **Returns**

    `indexes` [list(int), positive]: List of indexes to the `numbers` list

    `numbers` [list(int), positive]: List of fibonachi numbers
    """
    fibonachi_sequence = _get_fibonachi_sequence(**request.get_json())
    if type(fibonachi_sequence)==BaseException:
        return jsonify(str(fibonachi_sequence))

    response = {'indexes': fibonachi_sequence[0],
                'numbers': fibonachi_sequence[1]}
    return jsonify(response)


@main_blueprint.route('/task_3_endpoint', methods=['GET', 'POST'])
def task_3_endpoint():
    """
    Blacklists the fibonachi number at the given `index`.

    **Parameters**

    `index` [int, positive]: Index in the fibonachi sequence

    **Returns**

    A sorted list of blacklisted indexes
    """
    index = request.get_json()['index']
    if not _is_positive_integer(index):
        return jsonify(str(BaseException(invalid_input_errstr)))

    app.config['BLACKLIST'].add(index)
    return jsonify(list(sorted(app.config['BLACKLIST'])))


@main_blueprint.route('/task_4_endpoint', methods=['GET', 'POST'])
def task_4_endpoint():
    """
    Removes a `index` from the blacklist.

    **Parameters**

    `index` [int, positive]: Index in the fibonachi sequence

    **Returns**

    A sorted list of blacklisted indexes
    """
    index = request.get_json()['index']
    if not _is_positive_integer(index):
        return jsonify(str(BaseException(invalid_input_errstr)))

    try:
        app.config['BLACKLIST'].remove(index)
        response = jsonify(list(sorted(app.config['BLACKLIST'])))
    except KeyError:
        response = jsonify(remove_from_blacklist_errstr)
    
    return response


@main_blueprint.route('/clear_blacklist', methods=['GET', 'POST'])
def _clear_blacklist():
    app.config['BLACKLIST'] = set()
    return jsonify(True)