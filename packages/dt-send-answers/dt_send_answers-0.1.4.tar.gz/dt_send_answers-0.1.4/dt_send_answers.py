import requests, json
from docassemble.base.functions import get_config, all_variables, user_info, user_logged_in
from docassemble.base.core import DAFileList, DAFile, DADict

def send_answers(variables_to_reject = []):
  '''
  Sends your Docassemble user's serialized answers to your Community.lawyer account

  :param list variables_to_reject: A list of variables to exclude from sending to the server, defaults to none
  '''
  docassemble_api_key = get_config("docassemble api key")
  answers = all_variables(simplify=False)
  endpoint = "https://community.lawyer/docassemble_answers/new/"

  if len(variables_to_reject):
    answers = {k:v for k, v in answers.iteritems() if k not in variables_to_reject}

  for q, a in answers.items():
    if isinstance(a, DAFileList) or isinstance(a, DAFile):
      s3_config = get_config('s3')
      local_path = a.path().replace("/tmp/", "")
      if bool(s3_config):
        bucket_name = s3_config['bucket']
        answers[q] = "s3://%s/%s" % (bucket_name, local_path)
      else:
        answers[q] = local_path
  for q, a in answers.items():
    if isinstance(a, DADict) and type(a.values()[0]) is bool:
      checked_boxes = []
      for box_name, box_value in a.items():
        if box_value is True:
          checked_boxes.append(box_name)
      answers[q] = checked_boxes
  for q, a in answers.items():
    try:
      json.dumps(a)
    except:
      answers[q] = str(a)

  answers = json.dumps(answers, default=lambda x: str(x))
  metadata = json.dumps(all_variables(special='metadata'), default=lambda x: str(x))
  logged_in_user = json.dumps(get_user_info_hash())

  return requests.post(endpoint, data={'docassemble_api_key': docassemble_api_key, 'answers': answers, 'metadata': metadata, 'respondent': logged_in_user})

def get_user_info_hash():
  '''
  Returns a dict of the logged in Docassemble user's credentials
  '''
  user_hash = {}
  if user_logged_in():
    user_attributes = ['first_name', 'last_name', 'email', 'country', 'subdivision_first', 'subdivision_second', 'subdivision_third', 'organization']
    user = user_info()
    for attribute in user_attributes:
      value = getattr(user, attribute)
      if value:
        user_hash[attribute] = value
  return user_hash
