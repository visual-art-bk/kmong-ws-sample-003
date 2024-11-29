import os, requests, asyncio, urllib.parse, json, re, traceback
from urllib.parse import urljoin, urlparse
from .extract_it_id import extract_it_id


def fail_result(result: dict, url, result_url_k="결과", result_url_v="실패"):
    result[url][result_url_k] = result_url_v


async def save_scraping_result(
    url, thumb_path, parsed_data: dict, folder_name="정의되지않음"
):
    """local_result에 결과 저장"""
    result = {}

    if not parsed_data:
        return fail_result(result=result, url=url)

    try:
        result[url] = {}

        result[url]["결과"] = "성공"

        result[url]["상품아이디"] = extract_it_id(url=url)

        result[url][
            "링크"
        ] = f'=HYPERLINK("{str(urllib.parse.unquote(url))}", "{str(folder_name)}")'

        result[url]["거래처"] = ""

        result[url]["이미지"] = thumb_path

        result[url]["단가"] = parsed_data.get("price") or "AI분석결과없음"

        result[url]["1차"] = ""

        result[url]["2차"] = parsed_data.get("first_category") or "AI분석결과없음"

        result[url]["3차"] = parsed_data.get("second_category") or "AI분석결과없음"

        result[url]["4차"] = ""

        result[url]["필터"] = ""

        result[url]["성별"] = parsed_data.get("gender") or "AI분석결과없음"

        result[url]["브랜드"] = (parsed_data.get("brand") or "AI분석결과없음").upper()

        result[url]["2차 브랜드"] = ""

        result[url]["상품명"] = (
            re.match(
                r"^\[.*?\] (.*)", str((parsed_data.get("kor_name") or "AI분석결과없음"))
            ).group(1)
            if re.match(
                r"^\[.*?\] (.*)", str((parsed_data.get("kor_name") or "AI분석결과없음"))
            )
            else str(parsed_data["kor_name"])
        )

        result[url]["영문명"] = (
            re.match(
                r"^\[.*?\] (.*)", str((parsed_data.get("eng_name") or "AI분석결과없음"))
            ).group(1)
            if re.match(
                r"^\[.*?\] (.*)", str((parsed_data.get("eng_name") or "AI분석결과없음"))
            )
            else str(parsed_data["eng_name"])
        )

        result[url]["추가 정보\n모델명"] = ""

        result[url]["추가 정보\n배송방법"] = "항공특송"

        result[url]["추가 정보\n소재"] = ""

        result[url]["추가 정보\n구성품"] = "풀박스"

        result[url]["매장가"] = parsed_data.get("market_price") or "AI분석결과없음"

        result[url]["판매가1"] = ""

        result[url]["판매가21"] = ""

        result[url]["판매가3"] = ""

        result[url]["필수옵션\n등급선택"] = ""

        result[url]["필수옵션\n사이즈"] = (
            ",".join(parsed_data["sizes"]).replace("(", "[").replace(")", "]")
        )

        result[url]["필수옵션\n색상"] = ",".join(parsed_data["colors"])

        result[url]["필수옵션\n굽높이"] = ""

        result[url]["필수옵션\n버클"] = ""

        result[url]["필수옵션\n도금방식"] = ""

        result[url]["필수옵션\n밴드"] = ""

    except Exception as e:
        fail_result(result=result, url=url)
        print(f"결과 저장 실패: {e}")
        print("TRACEBACK:")
        traceback.print_exc()  # Traceback 정보 출력

    finally:
        return result
