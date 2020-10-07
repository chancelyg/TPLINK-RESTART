import requests
import json
import os
import yaml
import logging
import logging.config

_ROUTE_URL = '192.168.11.1'
_PASSS_WD = 'QpQLBVBKg44fbwK'

# 获取本地配置文件
logging_yaml_path = os.path.dirname(os.path.abspath(__file__)) + '/logging.yaml'
logs_path = os.path.dirname(os.path.abspath(__file__)) + '/logs'

# 日志配置
if not os.path.exists(logs_path):
    os.mkdir(logs_path)
with open(logging_yaml_path, 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
logger = logging.getLogger('main.common')

def restart():
    ''' Restart TP-Link Route
    '''
    url = 'http://%s/' % _ROUTE_URL
    headers = {'Accept':'application/json, text/javascript, */*; q=0.01'}
    login_dict = {
        'method':'do',
        'login':{
            'password':_PASSS_WD
        }
    }
    stok = None
    logger.info('Login route url->%s，Login args->%s' % (url,json.dumps(login_dict)))
    response = requests.post(url=url,headers=headers,json=login_dict)
    if response.ok:
        logger.info('Login return response http code is 200, Response text->%s' % response.text)
        response_result = json.loads(response.text)
        stok = response_result['stok']

    if not stok:
        logger.warn('Login is success. But not get stok!!')
        return

    url = 'http://%s/stok=%s/ds' % (_ROUTE_URL,stok)
    restart_dict = {
        'method':'do',
        'hyfi':{
            'reboot_all':None
        }
    }
    logger.info('Post restart route. Post info->%s. Post args->%s' % (url,json.dumps(restart_dict)))
    response = requests.post(url=url,headers=headers,json=restart_dict)
    if response.ok:
        logger.info('Restart is success.')

if __name__ == '__main__':
    logger.info('Start running. Route url is %s' % _ROUTE_URL)
    restart()
    logger.info('Running end')
    

