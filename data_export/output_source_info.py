from _utility.get_package_dir import get_global_subnational_covid_data_dir


def output_source_info(source_info):
    """
    Output source info into both machine-readable .tsv and human-readable .md file
    """

    # Output the source info into a .tsv (tab-separated) file
    with open(get_global_subnational_covid_data_dir() / 'source_info_table.tsv', 'w', encoding='utf-8') as f:
        f.write('source_id\tsource_url\tsource_desc\n')
        for source_id, source_url, source_desc in sorted(source_info):
            f.write(f'{source_id}\t{source_url}\t{source_desc}\n')

    # Output the source info into a .md (markdown) file
    with open(get_global_subnational_covid_data_dir() / 'source_info_table.md', 'w', encoding='utf-8') as f:
        f.write('| source_id | source_url | source_desc |\n')
        f.write('| --- | --- | --- |\n')
        for source_id, source_url, source_desc in sorted(source_info):
            f.write(f'| {source_id} | {source_url} | {source_desc} |\n')

