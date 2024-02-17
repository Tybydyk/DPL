import cv2
import pytesseract
from pytesseract import Output


def image_to_text(image_pointer):
    reg_num = 'Не определен'
    vin_num = 'Не определен'
    vehicle_color = 'Не определен'
    vehicle_year = 9999
    image_height = 1250
    image_wight = 900
    cnf_data = r'-l rus+eng --oem 2 --psm 6'
    cnf_rus = r'-l rus --oem 2 --psm 6'
    cnf_digit = r'--oem 2 --psm 6 -c tessedit_char_whitelist=0123456789'
    cnf_reg_num = r'--oem 2 --psm 6 -c tessedit_char_whitelist=ABECOPKHMTYX0123456789'
    cnf_vin = r'--oem 2 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHJKLMNPRSTVWXYZ'
    cnf_reg_num_rus = r'--oem 3 --psm 6 -c tessedit_char_whitelist=АВЕКМНОРСТУХ0123456789'
    conf_1 = 0
    conf_2 = 0

    img = cv2.imread(image_pointer)
    img = cv2.resize(img, (image_wight, image_height))  # normalize size 1:4
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey to reduce detials
    thresh = thresholding(gray)  # we use the binarization function

    #   we recognize the text for the first time, form a dictionary, determine the size of the dictionary
    cr_data = pytesseract.image_to_data(thresh, config=cnf_data, output_type=Output.DICT)  # make boxes arround words
    n_boxes = len(cr_data['text'])

    for i in range(n_boxes):
        if int(cr_data['conf'][i]) > 10:  # if the recognition accuracy is higher 10
            # (x, y, w, h) = (cr_data['left'][i], cr_data['top'][i], cr_data['width'][i], cr_data['height'][i])
            # print(i, " * ", x, y, w, h, "*", cr_data['text'][i], 'conf=', cr_data['conf'][i])
            # img = cv2.rectangle(img, (x, y), (x + w, y + h), (50, 255, 50), 1)

            # nomer - anchor
            if "знак" in cr_data['text'][i]:
                for j in range(i + 1, i + 4):
                    if 7 < len(cr_data['text'][j]) < 15:
                        if cr_data['conf'][j] >= 0:
                            reg_num = cr_data['text'][j]  # the reg_num in first OSR
                            conf_1 = cr_data['conf'][j]
                            break
                x1 = cr_data['left'][i] + cr_data['width'][i]
                x2 = image_wight - 2
                y1 = cr_data['top'][i] - 2 * cr_data['height'][i]
                y2 = cr_data['top'][i] + 2 * cr_data['height'][i]
                # the reg_num in second OSR
                num_2, conf_2 = crop_rectangle_ocr_to_data(x1, x2, y1, y2, cnf_reg_num, thresh)
                if conf_2 > conf_1:
                    reg_num = num_2

            # VIN - anchor
            elif "VIN" in cr_data['text'][i]:
                for j in range(i + 1, i + 6):
                    if len(cr_data['text'][j]) > 15:
                        if check_vin(cr_data['text'][j]) and cr_data['conf'][j] >= 0:
                            vin_num = cr_data['text'][j]  # the VIN in first OSR
                            conf_1 = cr_data['conf'][j]
                            x1 = cr_data['left'][j] - 10
                            x2 = cr_data['left'][j] + cr_data['width'][j] + 10
                            y1 = cr_data['top'][j] - 4
                            if cr_data['height'][j] < 35:
                                y2 = cr_data['top'][j] + cr_data['height'][j] + 4
                            else:
                                y2 = cr_data['top'][j] + 40
                    # the VIN in second OSR
                            vin_2, conf_2 = crop_rectangle_ocr_to_data(x1, x2, y1, y2, cnf_vin, thresh)
                            if check_vin(vin_2) and conf_2 > conf_1:
                                vin_num = vin_2
                            break

            # color - anchor
            elif "вет" in cr_data['text'][i] or "BET" in cr_data['text'][i]:
                for j in range(i + 1, i + 6):
                    # the Color in first OSR
                    if len(cr_data['text'][j]) > 4:
                        vehicle_color = cr_data['text'][j]
                        conf_1 = cr_data['conf'][j]
                        x1 = cr_data['left'][j] - 10
                        x2 = cr_data['left'][j] + cr_data['width'][j] + 10
                        y1 = cr_data['top'][j] - 4
                        y2 = cr_data['top'][j] + cr_data['height'][j] + 4
                # the Color in second OSR
                        color_2, conf_2 = crop_rectangle_ocr_to_data(x1, x2, y1, y2, cnf_rus, thresh)
                        if conf_2 > conf_1:
                            vehicle_color = color_2
                        break

                # year - anchor
            elif "Год" in cr_data['text'][i]:
                for j in range(i + 1, i + 6):
                    if len(cr_data['text'][j]) == 4:
                        vehicle_year = cr_data['text'][j]    # the Year in first OSR
                        conf_1 = cr_data['conf'][j]
                        x1 = cr_data['left'][j] - 10
                        x2 = cr_data['left'][j] + cr_data['width'][j] + 10
                        y1 = cr_data['top'][j] - 4
                        y2 = cr_data['top'][j] + cr_data['height'][j] + 4
                    # the Year in second OSR
                        year_2 = crop_rectangle_ocr_to_data(x1, x2, y1, y2, cnf_digit, thresh)
                        if conf_2 > conf_1:
                            vehicle_year = year_2
                        break

    result = [reg_num, vin_num, vehicle_year, vehicle_color]
    return result


def thresholding(image):
    return cv2.threshold(image, 10, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def crop_rectangle_ocr_to_data(x1, x2, y1, y2, config, image):
    data_1 = 'xxx'
    data_2 = -10
    crop_img = image[y1:y2, x1:x2]

    c_d = pytesseract.image_to_data(crop_img, config=config, output_type=Output.DICT)  # make boxes around words
    numbers_boxes = len(c_d['text'])
    for i in range(numbers_boxes):
        if int(c_d['conf'][i]) >= 0 and len(c_d['text'][i]) > 3:
            data_1 = c_d['text'][i]
            data_2 = c_d['conf'][i]
    return data_1, data_2


def check_vin(vin):
    return vin[10:17:].isdigit() and len(vin) == 17


if __name__ == "__main__":
    image_to_text('sts01.jpg')
