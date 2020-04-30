class CSVDataRevisions:
    def __get_revisions(self):
        # Return [[rev_date, rev_subid, rev_time], ...]
        r = []

        for fnam in listdir(OUTPUT_DIR):
            if not fnam.endswith('.tsv'):
                continue
            rev_date, rev_subid = fnam[:-4].split('-')
            rev_time = getctime(f'{OUTPUT_DIR}/{fnam}')
            dt = str(datetime.datetime.fromtimestamp(rev_time) \
                     .astimezone(timezone('Australia/Melbourne'))).split('.')[0]
            r.append((rev_date, int(rev_subid), dt))

        r.sort(reverse=True, key=lambda x: (x[0], x[1], x[2]))
        return r

