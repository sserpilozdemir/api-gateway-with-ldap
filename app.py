from flask import Flask, request, jsonify
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime
import requests
from flask_ldap3_login import LDAP3LoginManager, AuthenticationResponseStatus


# Local module
from config_mng import Config

app = Flask(__name__)
config = Config('config.yaml')


# loading LDAP config to Flask app's config
app.config['LDAP_HOST'] = config.get('ldap.host')
app.config['LDAP_BASE_DN'] = config.get('ldap.base_dn')
app.config['LDAP_USER_DN'] = config.get('ldap.user_dn')
app.config['LDAP_GROUP_DN'] = config.get('ldap.group_dn')
app.config['LDAP_USER_LOGIN_ATTR'] = config.get('ldap.user_login_attr')
app.config['LDAP_BIND_USER_DN'] = config.get('ldap.bind_user_dn')
app.config['LDAP_BIND_USER_PASSWORD'] = config.get('ldap.bind_user_password')
app.config['LDAP_USER_SEARCH_SCOPE'] = config.get('ldap.user_search_scope')
app.config['LDAP_SEARCH_FOR_GROUPS'] = config.get('ldap.search_for_groups')

ldap_manager = LDAP3LoginManager(app)
ldap_manager.init_app(app) 


def authenticate(username, password):
    response = ldap_manager.authenticate(username, password)
    if response.status == AuthenticationResponseStatus.success:
        return True
    return False

##pulling cache and throttle configs from yaml
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': config.get('redis.url')})
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=config.get('rate_limit.default'), 
    storage_uri=config.get('rate_limit.storage_uri')
    )


@app.route('/<service>/<path:path>', methods=['GET'])
@limiter.limit(config.get('rate_limit.default'))
@cache.cached(timeout=config.get('cache.timeout'), query_string=True)
def gateway(service, path):
    
    username = request.args.get('username')
    password = request.args.get('password')

    if not authenticate(username, password):
        return jsonify({'message': 'Invalid credentials'}), 403

    request_time = datetime.now()


    if service not in config.get('services'):
        return jsonify({
            'error': 'Service not found',
            'request_time': request_time.isoformat()
        }), 404

    url = f"{config.get('services')[service]}/{path}"
    response = requests.get(url, params=request.args)


    return jsonify({
        'data': response.json(),
        'request_time': request_time.isoformat(),
        'response_time': datetime.now().isoformat()
    }), response.status_code



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
