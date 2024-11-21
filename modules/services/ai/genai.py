import json


def ai_parse(ai_model, html_data):
    prompt = f"""```html_data
{html_data}
```

```available_brand_data
[
    "ASK YOURSELF",
    "ACNE STUDIOS",
    "ALEXANDER MCQUEEN",
    "ALEXANDER WANG",
    "ALYX",
    "AMI",
    "AMIRI",
    "ARCTERYX",
    "AUDEMARS PIGUET",
    "BALENCIAGA",
    "BALMAIN",
    "BAPE",
    "BERLUTI",
    "BLANCPAIN",
    "BOTTEGA VENETA",
    "BREGUET",
    "BALLY",
    "BREITLING",
    "BRUNELLO CUCINELLI",
    "BULGARI",
    "BURBERRY",
    "CANADA GOOSE",
    "CARTIER",
    "CASABLANCA",
    "CELINE",
    "CHANEL",
    "CHAUMET",
    "CHLOE",
    "CHROME HEARTS",
    "COMME DES GARCONS",
    "CP COMPANY",
    "DELVAUX",
    "DRIES VAN NOTEN",
    "DIESEL",
    "DIOR",
    "DOLCE & GABBANA",
    "EMPORIO ARMANI",
    "FEAR OF GOD",
    "FENDI",
    "FERRAGAMO",
    "GALLERY DEPT",
    "GENTLE MONSTER",
    "GIVENCHY",
    "GOLDEN GOOSE",
    "GOYARD",
    "GUCCI",
    "HERMES",
    "HUBLOT",
    "ISABEL MARANT",
    "IAB STUDIO",
    "IWC",
    "JACQUEMUS",
    "JIL SANDER",
    "JUNJI",
    "JIMMY CHOO",
    "JORDAN",
    "JUNYA WATANABE",
    "KENZO",
    "LANVIN BLANC",
    "LANVIN",
    "LEMAIRE",
    "LOEWE",
    "LORO PIANA",
    "LOUBOUTIN",
    "LOUIS VUITTON",
    "MACKAGE",
    "MAISON MARGIELA",
    "MAISON MIHARA YASUHIRO",
    "MANOLO BLAHNIK",
    "MARNI",
    "MARTINE ROSE",
    "MAX MARA",
    "MAISON KITSUNE",
    "MIU MIU",
    "MONCLER",
    "MOOSE KNUCKLES",
    "NEW BALANCE",
    "NIKE",
    "OFF WHITE",
    "OMEGA",
    "PHILIPP PLEIN",
    "PANERAI",
    "PARAJUMPERS",
    "PALM ANGELS",
    "PALACE",
    "PATEK PHILIPPE",
    "PRADA",
    "PIAGET",
    "POLORALPHLAUREN",
    "RAY BAN",
    "RHUDE",
    "RICK OWENS",
    "RIMOWA",
    "ROGER VIVIER",
    "ROLEX",
    "SACAI",
    "SUPREME",
    "SAINT LAURENT",
    "SALOMON",
    "STUSSY",
    "STONE ISLAND",
    "TAG HEUER",
    "THE NORTH FACE",
    "THOM BROWNE",
    "TIFFANY & CO",
    "TOM FORD",
    "TUDOR",
    "UMA WANG",
    "VACHERON CONSTANTIN",
    "VALENTINO",
    "VETEMENTS",
    "VANCLEEF",
    "VERSACE",
    "WOOYOUNGMI",
    "YEEZY",
    "ZEGNA",
    "OTHERS"
]
```

```available_category_data
{{
    "상의": ["반팔 티셔츠", "긴팔 티셔츠", "니트/가디건", "맨투맨", "후드", "원피스", "셔츠", "드레스", "슬리브리스", "셋업", "기타 상의"],
    "아우터": ["집업", "자켓", "패딩", "레더", "코트", "기타 아우터"],
    "하의": ["팬츠", "쇼츠", "트레이닝 팬츠", "데님", "스커트", "기타 하의"],
    "가방": ["미니백", "백팩", "숄더백", "토트백", "크로스백", "클러치", "캐리어", "핸드백", "더플백", "버킷백", "기타 가방"],
    "신발": ["스니커즈", "샌들/슬리퍼", "플랫", "로퍼", "더비/레이스업", "힐/펌프스", "부츠", "기타 신발"],
    "지갑": ["반지갑", "카드지갑", "지퍼장지갑", "중/장지갑", "여권지갑", "WOC", "기타 지갑"],
    "시계": ["메탈", "가죽", "우레탄"],
    "패션잡화": ["머플러/스카프", "아이웨어", "넥타이", "모자", "헤어액세서리", "기타 잡화"],
    "액세서리": ["반지", "목걸이", "팔찌", "귀걸이", "키링", "브로치", "기타 ACC"],
    "벨트": []
}}
```

Process the given html_data into a comma-separated dict format JSON data containing the following elements.

price : int (상품의 판매 가격),
market_price : str (상품의 정품 가격 또는 매장 가격. 찾을 수 없다면 공백),
brand : string (상품의 영어 브랜드 이름. 반드시 available_brand_data 에 포함되어야 함. 포함되지 않는다면 공백),
first_category : string (상품의 1차 카테고리 분류. 반드시 available_category_data의 key 에 포함되어야 함. 포함되지 않는다면 공백),
second_category : string (상품의 1차 카테고리 분류. 반드시 available_category_data의 list에 포함되어야 함. 포함되지 않거나 first_category가 공백이라면 공백),
gender : string (상품의 대상 성별. '남성', '여성', '남성,여성' 중 하나. 정확하지 않다면 '남성,여성'),
colors : list(string) (상품의 색상 옵션값. 찾을 수 없다면 []),
sizes : list(string) (상품의 사이즈 옵션값. 찾을 수 없다면 []),
kor_name : string (상품의 한글 이름. 이름 앞에 브랜드가 딱 한번 적혀 있어야 하며 반드시 한글이어야 함),
eng_name : string (상품의 한글 이름의 영어 번역 결과. 이름 앞에 브랜드가 딱 한번 적혀 있어야 하며 반드시 영어여야 함),
genuine_number : string (상품의 정품 코드. 정품 번호는 제품 이름에 의미 없는 문자와 숫자의 조합으로 표시될 수 있음. 찾을 수 없다면 공백)
"""

    response = ai_model.generate_content(prompt).text.strip()
    return json.loads(response)