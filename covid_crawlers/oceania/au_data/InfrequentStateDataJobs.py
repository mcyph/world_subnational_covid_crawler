class InfrequentStateDataJobs:
    def __init__(self):
        self._status = {}

    def run_all(self):
        self.update_act_powerbi()
        self.update_sa_regions()
        # Note Vic PowerBI has been retired
        self.update_vic_tableau()
        self.update_wa_regions()

    def get_status(self):
        return self._status

    def update_vic_tableau(self):
        from covid_crawlers.oceania.au_data.vic.deprecated.VicTableau import \
            run_vic_tableau
        try:
            run_vic_tableau()
            self._status['vic_tableau'] = {
                'status': 'OK',
                'message': None
            }
        except:
            print("Error occurred using VicTableau!")
            import traceback
            traceback.print_exc()
            self._status['vic_tableau'] = {
                'status': 'ERROR',
                'message': traceback.format_exc()
            }

    def update_act_powerbi(self):
        from covid_crawlers.oceania.au_data.act.ACTPowerBI import \
            ACTPowerBI
        try:
            ACTPowerBI().run_powerbi_grabber()
            self._status['act_powerbi'] = {
                'status': 'OK',
                'message': None
            }
        except:
            print("Error occurred using ACTPowerBI!")
            import traceback
            traceback.print_exc()
            self._status['act_powerbi'] = {
                'status': 'ERROR',
                'message': traceback.format_exc()
            }

    def update_wa_regions(self):
        from covid_crawlers.oceania.au_data.wa.WADash import \
            run_wa_dash
        try:
            run_wa_dash()
            self._status['wa_regions'] = {
                'status': 'OK',
                'message': None
            }
        except:
            print("Error occurred using WA regions!")
            import traceback
            traceback.print_exc()
            self._status['wa_regions'] = {
                'status': 'ERROR',
                'message': traceback.format_exc()
            }

    def update_sa_regions(self):
        from covid_crawlers.oceania.au_data.sa.SARegions import run_sa_regions

        try:
            run_sa_regions()
            self._status['sa_regions'] = {
                'status': 'OK',
                'message': None
            }
        except:
            print("Error occurred using SA regions!")
            import traceback

            traceback.print_exc()
            self._status['sa_regions'] = {
                'status': 'ERROR',
                'message': traceback.format_exc()
            }
