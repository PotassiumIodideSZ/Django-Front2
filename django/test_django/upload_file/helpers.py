import re
from upload_file.models import Keyword


# def text_update_key(s):
#     vocab = ['дороги', 'трамваи', 'рельсы', 'асфальт', 'тросы', 'безопасность', 'пешеходы', 'мост',
#              'освещение',
#              'отсыпка', 'грейдер',
#              'светофор', 'придорожный', 'сервис', 'шум', 'реагенты', 'парковка', 'подъездной' 'путь', 'яма',
#              'общественный', 'транспорт',
#              'выхлопы', 'многодетная', 'семья', 'инвалид', 'ветеран', 'волонтеры', 'алименты', 'алиментщик',
#              'родительские',
#              'права', 'судебные', 'приставы', 'вкладчики', 'ипотека', 'мошенничество', 'накопления',
#              'каникулы',
#              'кредит',
#              'налог', 'вклад', 'девальвация', 'Сбербанк', 'обязательства', 'списание', 'пенсионные',
#              'взносы',
#              'комиссия',
#              'рефинансирование', 'заработная', 'плата', 'пирамида', 'долг', 'проценты', 'счет',
#              'сберегательная',
#              'книжка', 'банк',
#              'компенсация', 'потребительский', 'кооператив', 'карта', 'коллекторы', 'банкрот', 'наличные',
#              'индексация',
#              'благодарность', 'глава', 'города', 'губернатор', 'благоустройство', 'околошкольная',
#              'территория',
#              'детская', 'площадка',
#              'преображение', 'снег', 'мусор', 'деревья', 'памятник', 'чистить', 'поиск', 'работы',
#              'интернет',
#              'собак', 'пляж', 'городской', 'парк', 'аттракционы', 'радиочастотная', 'электромагнитная',
#              'антенна',
#              'зловоние', 'питьевая',
#              'вода', 'дворец', 'спорта', 'детский', 'садик', 'поликлиники', 'придомовая', 'территория',
#              'облагораживание', 'очистные',
#              'сооружения', 'очистка', 'реки', 'канализации', 'стоянки', 'автомобилей', 'тротуар',
#              'межевание', 'двора',
#              'незаконные',
#              'лесной', 'массив', 'приют', 'выгул', 'пчелы', 'вода', 'трубы', 'водопровод', 'ЖКХ',
#              'водоснабжение',
#              'водоотведение', 'трудоустройство', 'инвалиды', 'работодатели', 'работа', 'индексирование',
#              'инфляция',
#              'пенсия', 'инвалидность', 'оплата', 'МРОТ', 'пособия', 'сокращение', 'РВП', 'вахтовый',
#              'метод', 'центр',
#              'занятости', 'бюджетники', 'неофициально', 'сокращение', 'социальная', 'польза', 'оклад',
#              'прожиточный',
#              'минимум',
#              'трудовой', 'стаж', 'должность', 'изобретательство', 'производство', 'цены', 'средний',
#              'доход',
#              'боевых', 'действий', 'условия', 'декрет', 'гражданство', 'пенсия', 'прожиточный', 'пенсионер',
#              'инвалид',
#              'стаж', 'прожиточный', 'участник', 'дети', 'войны', 'знак', 'отличия', 'пенсионный', 'возраст',
#              'выслуга',
#              'лет',
#              'фонд', 'РФ', 'газоснабжение', 'газификация', 'газ', 'газовые', 'коммуникации', 'газовая',
#              'служба',
#              'газопровод',
#              'газофицирование', 'оборудование', 'газовое', 'отопление', 'гражданство', 'виза', 'паспорт',
#              'вид',
#              'жительство',
#              'регистрация', 'детей', 'граница', 'эмигранты', 'воссоединение', 'семьей', 'запрет', 'въезд',
#              'знак',
#              'магазины',
#              'инфраструктура', 'жилье', 'жилищная', 'субсидия', 'жилищный', 'вопрос', 'жилищные', 'условия',
#              'квартира', 'ДЕЗ', 'ЖКХ', 'несущая', 'стена', 'жилплощадь', 'ухудшение', 'проживания',
#              'аварийный',
#              'управляющая',
#              'компания', 'подвал', 'жилая', 'площадь', 'общежитие', 'коммунальные', 'услуги', 'жильцы',
#              'оплаты',
#              'ремонт', 'ветхое',
#              'жилье', 'соседи', 'расселение', 'минздрав', 'вред', 'поликлиника', 'врач', 'операция',
#              'лекарства',
#              'здравоохранение', 'скорая', 'приписка', 'терапевт', 'госпиталь', 'ГКБ', 'работник',
#              'COVID', 'реабилитация', 'страховка', 'прием', 'роды', 'специалисты', 'стоматология', 'МРТ',
#              'обследование',
#              'пациенты', 'процедура', 'клиника', 'стоматолог', 'госпитализация', 'талон', 'узкие',
#              'специалисты',
#              'регистратура',
#              'укол', 'ревматолог', 'прививка', 'больничный', 'лист', 'зуб', 'роддом', 'аптека', 'провизор',
#              'минздрав',
#              'операции', 'лекарства', 'заболевание', 'анализы', 'аптеки', 'донор', 'платежи',
#              'беременность', 'полис', 'химиотерапия', 'медицина', 'медицинская', 'карта', 'ростреестр',
#              'участок',
#              'кадастр', 'дом', 'земля',
#              'приватизация', 'СНТ', 'огород', 'сотки', 'территория', 'двор', 'дачная', 'амнистия', 'поборы',
#              'самозахват', 'имущество',
#              'национальный', 'проект', 'порча', 'имущества', 'база', 'сайт', 'интернет', 'программное',
#              'обеспечение',
#              'связь',
#              'Ростелеком', 'средства', 'массовой', 'информации', 'цифровизация', 'мобильная', 'сеть',
#              'персональные',
#              'данные', 'операционная',
#              'система', 'тикток', 'российская', 'платформа', 'больница', 'клиника', 'covid', 'лаборатории',
#              'лечение', 'здравоохранение', 'лекарство', 'диабет', 'укол', 'диагностика', 'питание',
#              'терапия',
#              'пациент', 'суд',
#              'ОКБ', 'пандемия', 'медицинский', 'стаж', 'оплаты', 'поликлиника', 'больница', 'санитарный',
#              'персонал',
#              'пломбы', 'пенсионер', 'вакцина', 'ковид', 'препараты', 'санитарки', 'карантин',
#              'пункт', 'протезирование', 'операция', 'аналоги', 'здоровье', 'аборты',
#              'медперсонал', 'таблетки', 'суррогатное', 'материнство', 'диагноз', 'аптека', 'кино', 'фильмы',
#              'Вечный',
#              'Огонь', 'Герой', 'Социалистического', 'Труда', 'музей', 'цензура', 'балет', 'стиль',
#              'архитектуры',
#              'наследие', 'будущее',
#              'социальные', 'телевизор', 'книга', 'лес', 'участок', 'ГОК', 'валежник', 'егерь', 'АвтоВАЗ',
#              'песни',
#              'Конституция', 'маска',
#              'офис', 'собака', 'народ', 'санкции', 'желание', 'жизнь', 'смерти', 'коллектив', 'свадьба',
#              'елка',
#              'подарите', 'закрытые',
#              'города', 'приглашение', 'выступить', 'защиту', 'экспериментальной', 'музыки', 'загранпаспорт',
#              'выпуск',
#              'сборник',
#              'поблагодарить', 'турецкий', 'поток', 'личная', 'встреча', 'персональные', 'выставки',
#              'экономическое',
#              'развитие', 'рабочий',
#              'класс', 'соц', 'защита', 'инвалид', 'комиссия', 'подъемник', 'волонтер', 'страхование',
#              'малообеспеченные', 'безработица', 'биржа',
#              'труда', 'выплаты', 'пособие', 'компенсация', 'малоимущим', 'материнский', 'капитал', 'помощь',
#              'многодетные']

#     text = ''
#     for word in s.split():
#         if word in vocab:
#             text = text + word + ' '

#     return text[:-1]
def text_update_key(s):
    vocab = Keyword.objects.values_list('word', flat=True)
    
    

    text = ''
    for word in s.split():
        if word in vocab:
            text = text + word + ' '

    return text[:-1]


def get_lower(s):
    return s.lower()


def onlygoodsymbols(s):
    reg = re.compile('[^a-zа-я ]')
    return reg.sub('', s)
