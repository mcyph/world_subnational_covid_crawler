class InfrequentStateDataJobs:
    def __init__(self):
        self._status = {}

    def run_all(self):
        self.update_act_powerbi()
        self.update_sa_regions()
        self.update_vic_powerbi()
        self.update_wa_regions()

    def get_status(self):
        return self._status

    def update_vic_powerbi(self):
        from covid_19_au_grab.state_news_releases.vic.VicPowerBI import \
            VicPowerBI
        try:
            VicPowerBI().run_powerbi_grabber()
            self._status['vic_powerbi'] = ('OK', None)
        except:
            print("Error occurred using VicPowerBI!")
            import traceback
            traceback.print_exc()
            self._status['vic_powerbi'] = (
                'ERROR', traceback.format_exc()
            )

    def update_act_powerbi(self):
        from covid_19_au_grab.state_news_releases.act.ACTPowerBI import \
            ACTPowerBI
        try:
            ACTPowerBI().run_powerbi_grabber()
            self._status['act_powerbi'] = ('OK', None)
        except:
            print("Error occurred using ACTPowerBI!")
            import traceback
            traceback.print_exc()
            self._status['act_powerbi'] = (
                'ERROR', traceback.format_exc()
            )

    def update_wa_regions(self):
        from covid_19_au_grab.state_news_releases.wa.WADash import \
            run_wa_dash
        try:
            run_wa_dash()
            self._status['wa_regions'] = ('OK', None)
        except:
            print("Error occurred using WA regions!")
            import traceback
            traceback.print_exc()
            self._status['wa_regions'] = (
                'ERROR', traceback.format_exc()
            )

    def update_sa_regions(self):
        from covid_19_au_grab.state_news_releases.sa.SARegions import run_sa_regions

        try:
            run_sa_regions()
            self._status['sa_regions'] = ('OK', None)
        except:
            print("Error occurred using SA regions!")
            import traceback

            traceback.print_exc()
            self._status['sa_regions'] = (
                'ERROR', traceback.format_exc()
            )
