from urllib.parse import urlparse, parse_qs

def extract_it_id(url):
    try:
        # URL 파싱
        parsed_url = urlparse(url)

        # 쿼리 문자열 파싱
        query_params = parse_qs(parsed_url.query)

        # it_id 추출
        it_id = query_params.get("it_id", [None])[0]

        return f"{it_id}"
    except Exception as e:
        return f"Error: {e}"