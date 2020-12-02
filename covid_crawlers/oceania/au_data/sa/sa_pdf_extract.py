import cv2
import numpy as np
import pdf2image
from _utility.get_package_dir import get_package_dir


PDFS_DIR = get_package_dir() / 'covid_crawlers' / 'oceania' / 'au_data' / 'sa' / 'pdfs'
OUTPUT_DIR = get_package_dir() / 'covid_crawlers' / 'oceania' / 'au_data' / 'sa' / 'output'


LINKS = [
    'https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/resources/map+1+number+of+positive+covid-19+cases+in+south+australia+metropolitan+adelaide',
    'https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/resources/map+2+number+of+positive+covid-19+cases+in+south+australia+whole+of+sa',
    'https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/resources/map+1+number+of+active+covid-19+cases+in+south+australia+metropolitan+adelaide',
    'https://www.sahealth.sa.gov.au/wps/wcm/connect/public+content/sa+health+internet/resources/map+2+number+of+active+covid-19+cases+in+south+australia+whole+of+sa'
]

color_map = {
    (253, 126, 126): (33, 37),
    (252, 161, 127): (24, 32),
    (251, 192, 127): (14, 23),
    (246, 221, 125): (9, 13),
    (241, 251, 124): (7, 8),
    (207, 228, 150): (5, 6),
    (170, 205, 171): (3, 4),
    (126, 182, 189): (2, 2),
    (55, 160, 207): (1, 1),
    (239, 239, 239): (0, 0)
}

wholesa_relative_to = (347, 561)
wholesa_match = {
    (443, 601): 'The Dc of Streaky Bay',
    (628, 648): 'The Corporation of the City of Whyalla',
    (645, 616): 'Port Augusta City Council',
    (580, 508): 'Pastoral Unincorporated Area',
    (628, 860): 'Kangaroo Island Council',
    (646, 721): 'Copper Coast Council',
    (646, 766): 'Yorke Peninsula Council',
    (661, 665): 'Port Pirie Regional Council',
    (691, 733): 'Wakefield Regional Council',
    (770, 729): 'Mid Murray Council',
    (857, 734): 'Renmark Paringa Council',
    (831, 788): 'The Dc of Loxton Waikerie',
    (704, 845): 'City of Victor Harbor',
    (747, 813): 'The Rural City of Murray Bridge',
    (844, 891): 'Tatiara Dc',
    (795, 918): 'Kingston Dc',
    (833, 742): 'The Berri Barmera Council',
    (850, 1001): 'Wattle Range Council',
    (592, 450): 'Municipal Council of Roxby Downs',
}

metro_relative_to = (171, 339)
metro_match = {
    (241, 196): 'City of Playford',
    (239, 309): 'City of Salisbury',
    (403, 336): 'City of Tea Tree Gully',
    (366, 97): 'Light Regional Council',
    (377, 149): 'Town of Gawler',
    (653, 262): 'The Barossa Council',
    (524, 429): 'Adelaide Hills Council',
    (220, 416): 'City of Port Adelaide Enfield',
    (269, 475): 'City of Prospect',
    (293, 511): 'The City of Norwood Payneham and St Peters',
    (280, 488): 'The Corporation of the Town of Walkerville',
    (253, 524): 'Adelaide City Council',
    (203, 474): 'City of Charles Sturt',
    (211, 531): 'City of West Torrens',
    (339, 533): 'City of Burnside',
    (272, 555): 'City of Unley',
    (177, 617): 'City of Holdfast Bay',
    (209, 645): 'City of Marion',
    (313, 627): 'City of Mitcham',
    (285, 726): 'City of Onkaparinga',
    (480, 749): 'Mount Barker District Council',
    (344, 962): 'Alexandrina Council',
}


class SAPDFExtract:
    def __init__(self,
                 pdf_path,
                 relative_to,
                 lga_dict,
                 small_img_path):

        self.relative_to = relative_to
        self.lga_dict = lga_dict

        small_image = cv2.imread(small_img_path)

        large_image_pil = pdf2image.pdf2image.convert_from_path(
            pdf_path, dpi=80
        )[0].convert('RGB')
        large_image_pil.save(pdf_path+'.png')
        large_image = np.array(large_image_pil)
        # Convert RGB to BGR
        large_image = large_image[:, :, ::-1].copy()

        self.small_image = small_image
        self.large_image_pil = large_image_pil
        self.large_image = large_image

    def get_bounding_coords(self):
        result = cv2.matchTemplate(
            self.small_image, self.large_image,
            method=cv2.TM_SQDIFF_NORMED
        )
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)
        MPx, MPy = mnLoc
        trows, tcols = self.small_image.shape[:2]
        return MPx, MPy, MPx+tcols, MPy+trows

    def get_x_y_difference(self):
        x1, y1, x2, y2 = self.get_bounding_coords()
        return x1-self.relative_to[0], y1-self.relative_to[1]

    def get_counts_dict(self, as_average=False):
        rel_diff = self.get_x_y_difference()

        out = {}
        for (x, y), lga in self.lga_dict.items():
            r, g, b = self.large_image_pil.getpixel(
                (x-rel_diff[0], y-rel_diff[1])
            )

            # Highlight it, for debug purposes
            cv2.rectangle(
                self.large_image,
                (x-rel_diff[0], y-rel_diff[1]),
                (x-rel_diff[0]+5, y-rel_diff[1]+5),
                (0, 0, 255), 2
            )

            for (c_r, c_g, c_b), (from_count, to_count) in color_map.items():
                if abs(r-c_r) + abs(g-c_g) + abs(b-c_b) < 15:
                    if as_average:
                        out[lga] = (from_count + to_count) // 2
                    else:
                        out[lga] = (from_count, to_count)
                    break
        return out

    def display(self, x1, y1, x2, y2):
        print(x1, y1)
        cv2.rectangle(self.large_image, (x1, y1), (x2, y2), (0,0,255), 2)
        cv2.imshow('output', self.large_image)
        cv2.waitKey(0)


if __name__ == '__main__':
    import json
    from os import listdir
    from glob import glob

    output_dict = {}  # {date: [(LGA, amount), ...], ...}

    for dir_ in listdir(PDFS_DIR):
        for pdf_path in glob(f'{PDFS_DIR}/{dir_}/*.pdf'):
            print(pdf_path)

            if 'Active' in pdf_path:
                datatype = 'DataTypes.STATUS_ACTIVE'
            elif 'Positive' in pdf_path:
                datatype = 'DataTypes.TOTAL'
            else:
                raise Exception(pdf_path)

            if pdf_path.endswith('1.pdf') or 'Metropolitan' in pdf_path:
                # Metro
                spe = SAPDFExtract(
                    pdf_path,
                    metro_relative_to,
                    metro_match,
                    'metro_small_img.png'
                )
                counts_dict = spe.get_counts_dict(
                    as_average=True
                )

                for lga, count in counts_dict.items():
                    output_dict.setdefault(dir_, []).append((lga, datatype, count))

                x1, y1, x2, y2 = spe.get_bounding_coords()
                #spe.display(x1, y1, x2, y2)

            elif pdf_path.endswith('2.pdf') or 'Overall' in pdf_path:
                # Regional
                spe = SAPDFExtract(
                    pdf_path,
                    wholesa_relative_to,
                    wholesa_match,
                    'wholesa_small_img.png'
                )
                #print("DIFFERENCE:", spe.get_x_y_difference())
                counts_dict = spe.get_counts_dict(
                    as_average=True
                )

                for lga, count in counts_dict.items():
                    output_dict.setdefault(dir_, []).append((lga, datatype, count))

                x1, y1, x2, y2 = spe.get_bounding_coords()
                #spe.display(x1, y1, x2, y2)

            else:
                raise Exception(pdf_path)

    for date, count_list in output_dict.items():
        with open(f'{OUTPUT_DIR}/{date}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(count_list, indent=4))
