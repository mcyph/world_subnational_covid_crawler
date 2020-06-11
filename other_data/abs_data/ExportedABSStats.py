class ExportedABSStats:
    def get_latest_abs_stats(self):
        """
        {
           measure initial:
               {(state, lga name, stat name): (year, value), ...},
           ...
        }
        """
        r = {}

        for path in glob(f'{BASE_PATH}/*.csv'):
            if not 'SEIFA' in path:
                # Better to use the excel reader for non-SEIFA stats!
                continue

            with open(path, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row['Value']:
                        continue

                    self._row_processed(row)
        return r

    def _row_processed(self, row):
        # SEIFA data includes percentile, decile, ranks within area
        # I'm only going to get the national percentile values
        if 'Measure' in row and row['Measure'] != 'Rank within Australia - Percentile':
            return
        elif 'Measure' in row:
            row['Index Type'] += ' (%)'

        # Map the LGA id to the state/locality name
        lga_id = int(row.get('LGA_2018') or row['LGA_2011'])
        try:
            state, lga_name = lga_dict[lga_id]
        except KeyError:
            print("Warning: LGA ID not found", row)
            return

        if True:
            # This is often more useful, as it doesn't include ..council etc!!!
            lga_name = (row.get('Region') or row['Local Government Areas - 2011']).split('(')[0].strip()
            lga_name = normalize_locality_name(lga_name)

        stat_name = row.get('Data item') or row['Index Type']
        year = int(row['Time'])

        # Parse value to float if there's a decimal
        if '.' in row['Value']:
            value = float(row['Value'])
        else:
            value = int(row['Value'])

        # If it's a percentile value and it's
        # over 100%, there's something wrong!
        if stat_name.endswith('(%)'):
            if value >= 100.0:
                print("PC VAL > 100: ", row)
                value = 100.0  # WTF??!

        MEASURE_key = (
            row['MEASURE'].rpartition('_')[0]
            if '_' in row['MEASURE']
            else row['MEASURE']
        )
        if not MEASURE_key in r:
            r[MEASURE_key] = {}

        key = (state, lga_name, stat_name)
        if key in r[MEASURE_key] and r[MEASURE_key][key][0] > year:
            return
        r[MEASURE_key][key] = (year, value)
