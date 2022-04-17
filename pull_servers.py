from api.worker.master import _update_list

from api.worker.server_info import update_all

update_all.delay()

_update_list()

update_all.delay()

