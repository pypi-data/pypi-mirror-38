from eulfedora.server import Repository
from pydial.model import DialArticleObject
from pprint import pprint
import datetime
debug_mode = True

fc_repo = Repository("http://localhost/fedora", username='*******', password='*****')
fc_obj = fc_repo.get_object(type=DialArticleObject)
fc_obj.save() # need to be call to create the pid for this object
print fc_obj.pid

# Call Handle WebService here to create the handle
if not debug_mode:
    handle = call_handle_ws(authority='2078.1', pid=fc_obj.pid)
    fc_obj.handle_url = "https://hdl.handle.net/{suffix}".format(suffix=handle)

# Now create the MARCXML. Don't forget to add the HANDLE into a 856 tag !
fc_obj.marcxml.content = "<Person><name>Toto</name></Person>"
fc_obj.save()
