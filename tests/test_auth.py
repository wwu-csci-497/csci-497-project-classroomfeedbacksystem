# test_auth.py
@pytest.mark.parametrize(('username', 'password', 'message'), (
  ('', '', b'Username is required.'),
  ('a@c.com', '', b'Password is required.'),
  ('a@b.com', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
  response = client.post(
    '/register',
    data={'username': username, 'password': password}
  )
  assert message in response.data