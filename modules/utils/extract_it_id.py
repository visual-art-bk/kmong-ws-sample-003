def extract_it_id(url):
    import random
    from urllib.parse import urlparse, parse_qs
    from datetime import datetime

    try:
        prefix = datetime.now().strftime("%Y%m%d_%H%M%S.%f")[:-4]  
        parsed_url = urlparse(url)

        # 쿼리 문자열 파싱
        query_params = parse_qs(parsed_url.query)

        # 키 후보군 정의
        prod_id_candidates = ["it_id", "product_no"]

        # 키 후보군 순회
        for key in prod_id_candidates:
            values = query_params.get(key, [])
            for value in values:
                if value:  # 값이 None, 빈 문자열("")이 아닌 경우 반환
                    return f"{prefix}_{value}"
        
        # 모든 키에서 값이 없을 경우 랜덤 6자리 숫자 생성
        random_it_id = str(random.randint(100000, 999999))
        return f"{prefix}_{random_it_id}"

    except Exception as e:
        return f"Error: {e}"
