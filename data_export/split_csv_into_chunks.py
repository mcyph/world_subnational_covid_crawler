from pathlib import Path


TEN_MB = 10000000
FIVE_MB = 5000000


def split_csv_into_chunks(path, chunk_size=TEN_MB):
    path = str(path)
    output_prefix = path.rpartition('.')[0]
    output_ext = path.rpartition('.')[-1]

    with open(path, 'rb') as f:
        seek_positions = []
        for x, line in enumerate(f):
            if not x:
                header = line
            seek_positions.append(f.tell())

        part = 0
        last_seek_pos = seek_positions[-1]
        for seek_pos in reversed(seek_positions):
            if last_seek_pos-seek_pos >= chunk_size:
                with open(f'{output_prefix}.arch.{part}.{output_ext}', 'wb') as f_out:
                    f.seek(seek_pos)
                    f_out.write(header)
                    f_out.write(f.read(last_seek_pos-seek_pos))

                last_seek_pos = seek_pos
                part += 1

        with open(f'{output_prefix}.arch.{part}.{output_ext}', 'wb') as f_out:
            f.seek(0)
            f_out.write(f.read(last_seek_pos))

    Path(path).rename(path+'~')
    Path(f'{output_prefix}.arch.0.{output_ext}').rename(path)
    Path(path+'~').unlink()


#if __name__ == '__main__':
    #split_file_into_chunks(
    #    '../../global_subnational_covid_data/casedata/world/world.admin_1.covid19datahub.total.txt'
    #)
