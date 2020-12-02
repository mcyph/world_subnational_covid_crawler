from covid_19_au_grab.covid_db.datatypes.enums import Schemas, DataTypes


class CITY:
    pass  # Just for by reference


class UNKNOWN_GENDER:
    pass  # TODO!


stats_map = {
    '総数': (DataTypes.NEW, None),
    '濃厚接触者※１': (DataTypes.SOURCE_CONFIRMED, None),
    '海外渡航歴': (DataTypes.SOURCE_OVERSEAS, None),
    '調査中': (DataTypes.SOURCE_UNDER_INVESTIGATION, None),
    #'うち重症者': (DataTypes.STATUS_ICU, None),  # CHECK ME! =========================

    '10歳未満': (DataTypes.TOTAL, '0-9'),
    '10代': (DataTypes.TOTAL, '10-19'),
    '20代': (DataTypes.TOTAL, '20-29'),
    '30代': (DataTypes.TOTAL, '30-39'),
    '40代': (DataTypes.TOTAL, '40-49'),
    '50代': (DataTypes.TOTAL, '50-59'),
    '60代': (DataTypes.TOTAL, '60-69'),
    '70代': (DataTypes.TOTAL, '70-79'),
    '80代': (DataTypes.TOTAL, '80-89'),
    '90代': (DataTypes.TOTAL, '90-99'),
    '100歳以上': (DataTypes.TOTAL, '100+'),
    '不明_1': (DataTypes.TOTAL, 'Unknown'),  # FIXME!!! ===============================================

    '男性': (DataTypes.TOTAL_MALE, None),
    '女性': (DataTypes.TOTAL_FEMALE, None),
    '不明_2': UNKNOWN_GENDER,  # FIXME!!! ===============================================

    '総数（累計）': (DataTypes.TOTAL, None),
    '重症者': (DataTypes.STATUS_ICU, None),
    '死亡（累計）': (DataTypes.STATUS_DEATHS, None),
    #'退院（累計）': (DataTypes.STATUS_RELEASED),

    '千代田': CITY,
    '中央': CITY,
    '港': CITY,
    '新宿': CITY,
    '文京': CITY,
    '台東': CITY,
    '墨田': CITY,
    '江東': CITY,
    '品川': CITY,
    '目黒': CITY,
    '大田': CITY,
    '世田谷': CITY,
    '渋谷': CITY,
    '中野': CITY,
    '杉並': CITY,
    '豊島': CITY,
    '北': CITY,
    '荒川': CITY,
    '板橋': CITY,
    '練馬': CITY,
    '足立': CITY,
    '葛飾': CITY,
    '江戸川': CITY,
    '八王子': CITY,
    '立川': CITY,
    '武蔵野': CITY,
    '三鷹': CITY,
    '青梅': CITY,
    '府中': CITY,
    '昭島': CITY,
    '調布': CITY,
    '町田': CITY,
    '小金井': CITY,
    '小平': CITY,
    '日野': CITY,
    '東村山': CITY,
    '国分寺': CITY,
    '国立': CITY,
    '福生': CITY,
    '狛江': CITY,
    '東大和': CITY,
    '清瀬': CITY,
    '東久留米': CITY,
    '武蔵村山': CITY,
    '多摩': CITY,
    '稲城': CITY,
    '羽村': CITY,
    'あきる野': CITY,
    '西東京': CITY,
    '瑞穂': CITY,
    '日の出': CITY,
    '檜原': CITY,
    '奥多摩': CITY,
    '大島': CITY,
    '利島': CITY,
    '新島': CITY,
    '神津島': CITY,
    '三宅': CITY,
    '御蔵島': CITY,
    '八丈': CITY,
    '青ヶ島': CITY,
    '小笠原': CITY,

    '都外': CITY,
    '調査中※': CITY,
}
