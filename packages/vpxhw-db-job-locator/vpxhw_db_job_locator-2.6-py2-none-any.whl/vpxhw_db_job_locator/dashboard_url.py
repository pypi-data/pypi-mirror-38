from jinja2 import Template
import requests
from os.path import basename
import urllib
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


url_template = """http://go/vpxhw-quality?{{jobIds}}

{% if encoder %}
  Choose {% for e in encoder %}
  {{ e }}{% endfor %}
  in encoder selection box (top one on the left)
{% endif %}
{% if model_name %}
  Pick '{{model_name}}' in tags filter (second one from the top)
{% endif %}
"""

logger = logging.getLogger(__name__)

class DashboardUrl(object):

  @staticmethod
  def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

  def __init__(self):
    super(DashboardUrl, self).__init__()

    self._encoder = []
    self._model_name = None
    self._jobIds = []

  def _post(self, url, data):
    logger.debug("making post request to "+url+" with data:\n"+str(data))
    r = self.requests_retry_session().post(url,
        data=data)

    if r.status_code == requests.codes.ok:
      logger.debug("post request returned successfully")
      self._jobIds.append(r.text)
    else:
      logger.warning("error code "+str(r.status_code)+" is returned")
      logger.warning(r.text)

  def add_single_job(self, commit, encoder, usecase, test_suite, model_name):
    self._encoder.append(' '.join((
        encoder,
        usecase,
    )))
    self._model_name = model_name

    post_data={
            'commit': commit,
            'encoder': encoder,
            'usecase': usecase,
            'test_suite': basename(test_suite),
            'model_name': model_name,
            'FPGA': '0',
        }

    self._post(
        'http://35.186.209.225/be/locate/single',
        data=post_data)

  def add_latest_job(self, encoder, usecase, test_suite, model_name=None):
    self._encoder.append(' '.join((
        encoder,
        usecase,
    )))

    post_data = {
        'encoder': encoder,
        'usecase': usecase,
        'test_suite': basename(test_suite),
        'FPGA': '0',
    }

    if model_name:
      post_data['model_name'] = model_name


    self._post('http://35.186.209.225/be/locate/latest', data=post_data)

  def get_dashboard_url(self):
    template = Template(url_template)

    jobIdsString = '&'.join(
        ['job=' + urllib.quote_plus(id) for id in self._jobIds])
    return template.render({
        'jobIds': jobIdsString,
        'encoder': self._encoder,
        'model_name': self._model_name
    })
