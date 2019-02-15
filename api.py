import datetime

import flask

import cache

app = flask.Flask(__name__)


@app.route('/')
def get_day():
    date_string = flask.request.args.get('d')

    if date_string:
        try:
            date = datetime.date.fromisoformat(date_string)
        except ValueError:
            return flask.abort(
                400, "Incorrect date format, expected YYYY-MM-DD")
    else:
        date = datetime.date.today()

    obj = cache.read_menu(date)

    if not obj:
        return flask.abort(404)

    return flask.jsonify(obj)


@app.route('/cake')
def get_cake():
    today = datetime.date.today()

    week = flask.request.args.get('w') or today.isocalendar()[1]
    year = flask.request.args.get('y') or today.isocalendar()[0]

    kage = cache.read_cake(week, year)

    if not kage:
        return flask.abort(404)

    return flask.jsonify(kage)


if __name__ == '__main__':
    app.run()
