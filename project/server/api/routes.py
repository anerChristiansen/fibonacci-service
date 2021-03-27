from flask import Blueprint, jsonify, request
from flask import current_app as app

main_blueprint = Blueprint('api', __name__,)


remove_from_blacklist_errstr = 'Index not blacklisted'


def get_fibonachi_sequence(index, page=0, pagesize=100):
    indexes = list(range(index+1))
    fibonachi_sequence = [0] * (index + 1)
    fibonachi_sequence[1] = 1

    for i in range(2, index+1):
        fibonachi_sequence[i] = fibonachi_sequence[i-1] + fibonachi_sequence[i-2]
    
    for i in sorted(app.config['BLACKLIST'], reverse=True):
        indexes.pop(i)
        fibonachi_sequence.pop(i)
    
    start_idx = page*pagesize
    end_idx = (page + 1)*pagesize
    if start_idx > len(indexes):
        fibonachi_sequence, indexes = [], []
    else:
        if end_idx > len(indexes):
            fibonachi_sequence, indexes = fibonachi_sequence[start_idx:], indexes[start_idx:]
        else:
            fibonachi_sequence, indexes = fibonachi_sequence[start_idx:end_idx], indexes[start_idx:end_idx]

    return fibonachi_sequence, indexes


@main_blueprint.route('/clear_blacklist', methods=['GET', 'POST'])
def clear_blacklist():
    app.config['BLACKLIST'] = set()
    return jsonify(True)


@main_blueprint.route('/task_1_endpoint', methods=['GET', 'POST'])
def task_1_endpoint():
    fibonachi_sequence, _ = get_fibonachi_sequence(**request.get_json())
    fibonachi_number = fibonachi_sequence[-1]
    return jsonify(fibonachi_number)


@main_blueprint.route('/task_2_endpoint', methods=['GET', 'POST'])
def task_2_endpoint():
    fibonachi_sequence, indexes = get_fibonachi_sequence(**request.get_json())

    response = {'indexes': indexes,
                'numbers': fibonachi_sequence}
    return jsonify(response)


@main_blueprint.route('/task_3_endpoint', methods=['GET', 'POST'])
def task_3_endpoint():
    index = request.get_json()['index']
    app.config['BLACKLIST'].add(index)
    return jsonify(list(sorted(app.config['BLACKLIST'])))


@main_blueprint.route('/task_4_endpoint', methods=['GET', 'POST'])
def task_4_endpoint():
    index = request.get_json()['index']
    try:
        app.config['BLACKLIST'].remove(index)
        response = jsonify(list(sorted(app.config['BLACKLIST'])))
    except KeyError:
        response = jsonify(remove_from_blacklist_errstr)
    
    return response