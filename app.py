import flask
from flask import Flask
from flask import request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask.views import MethodView


app = Flask('app')
Base = declarative_base()
engine = create_engine('postgresql://app:1234@127.0.0.1:5431/ads_website')
Session = sessionmaker(bind=engine)


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(er: HttpError):
    response = flask.jsonify({
        'status': 'error',
        'message': er.message
    })
    response.status_code = er.status_code
    return response


class Ad(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(String(64), nullable=False)


Base.metadata.create_all(engine)


def get_ad(session, ad_id):
    ad = session.query(Ad).get(ad_id)
    if ad is None:
        raise HttpError(404, 'ad does not exist')
    return ad


class UserView(MethodView):

    def get(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
            return flask.jsonify({
                'name': ad.name,
                'creation_time': ad.creation_time.isoformat(),
                'owner': ad.owner
            })

    def post(self):
        ad_data = request.json
        with Session() as session:
            new_ad = Ad(
                name=ad_data['name'],
                description=ad_data['description'],
                owner=ad_data['owner']
            )
            session.add(new_ad)
            session.commit()
            return flask.jsonify({'status': 'ok', 'id': new_ad.id})

    def patch(self, ad_id):
        ad_data = request.json
        with Session() as session:
            ad = get_ad(session, ad_id)
            for key, value in ad_data.items():
                setattr(ad, key, value)
            session.commit()
            return flask.jsonify({'status': 'ok', 'name': ad.name})

    def delete(self, ad_id):
        with Session() as session:
            ad = get_ad(session, ad_id)
            session.delete(ad)
            session.commit()
            return flask.jsonify({'status': 'ok'})


# @app.route('/test', methods=['POST'])
# def hello_world():
#     headers = request.headers
#     json_data = request.json
#     qs = request.args
#     response = flask.jsonify({'Hello': 'World', 'headers': dict(headers),
#                               'json_data': json_data, 'qs': qs})
#     return response

app.add_url_rule('/ads', view_func=UserView.as_view('ads'), methods=['POST'])
app.add_url_rule('/ads/<int:ad_id>', view_func=UserView.as_view('get_ad'), methods=['GET', 'PATCH', 'DELETE'])
app.run()

