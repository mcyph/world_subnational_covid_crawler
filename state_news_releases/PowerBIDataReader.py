import json
import glob
from os import listdir


class PowerBIDataReader:
    def __init__(self, base_dir, globals_dict):
        self.base_dir = base_dir
        # base_dir -> PATH_PREFIX
        self.globals_dict = globals_dict

    def _iter_all_dates(self):
        for sub_dir in listdir(self.base_dir):
            date, subid = sub_dir.split('-')
            yield date, int(subid), self._match_grabbed_with_types(
                f'{self.base_dir}/{sub_dir}'
            )

    def _match_grabbed_with_types(self, dir_):
        """
        Return a dict, with requests matched with
        responses and assigned to specific keys.
        e.g. "age_groups" or "gender_balance"
        """
        r = {}

        for request_data, response_data in self._iter_json_data(dir_):

            if isinstance(request_data, str):
                # The old format, without a specific request!
                match = request_data
            else:
                #print(request_data)
                j_post_data = json.dumps(request_data, sort_keys=True)

                match = None

                for k, v in self.globals_dict.items():
                    if k.endswith('_req'):
                        v = json.dumps(v, sort_keys=True)
                        if j_post_data == v:
                            match = k[:-4]
                            break

            if match:
                r[match] = (request_data, response_data)
            else:
                print("WARNING - no match:", json.dumps(request_data, indent=4))
                print(json.dumps(response_data, indent=4))

        return r

    def _iter_json_data(self, dir_):
        for json_path in glob.glob(f'{dir_}/*.json'):
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())

                if isinstance(data, (list, tuple)):
                    for x, request in enumerate(data[0]['queries']):
                        # It seems the returned job ids can be out of order??
                        # I'm think the queries could be done asynchronously
                        # and have to be reordered based on these jobIds ==============================================
                        job_id = data[1]['jobIds'][x]
                        yield request, [i for i in data[1]['results'] if i['jobId'] == job_id][0]
                else:
                    # TODO: Support the old format, which didn't
                    #  match the request with the response!
                    #print(json.dumps(data, indent=4))
                    yield json_path.replace('.json', '').split('/')[-1], data['results'][0]
