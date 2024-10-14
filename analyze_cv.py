import pdfplumber

def extract_text_from_pdf(input_pdf_path):
    """
    PDF 파일에서 텍스트를 추출하여 반환하는 함수입니다.

    Parameters:
    input_pdf_path (str): 텍스트를 추출할 PDF 파일의 경로.

    Returns:
    str: 추출된 전체 텍스트.
    """
    try:
        with pdfplumber.open(input_pdf_path) as pdf:  # PDF 파일을 엽니다.
            text = ''  # 추출된 텍스트를 저장할 빈 문자열을 초기화합니다.
            for page in pdf.pages:  # 모든 페이지를 순회하면서
                page_text = page.extract_text()  # 각 페이지에서 텍스트를 추출합니다.
                if page_text:  # 텍스트가 있는 경우에만 추가합니다.
                    text += page_text + '\n'  # 텍스트를 줄바꿈과 함께 추가합니다.
        return text  # 추출된 텍스트를 반환합니다.
    except Exception as e:
        print(f"Error: {e}")  # 오류가 발생하면 메시지를 출력합니다.
        return None  # 오류 발생 시 None을 반환합니다.


# 사용 예시
if __name__ == '__main__':
    input_pdf_path = 'sample.pdf'  # 예시 PDF 파일 경로
    extracted_text = extract_text_from_pdf(input_pdf_path)  # 텍스트를 추출합니다.

    if extracted_text:  # 텍스트가 정상적으로 추출된 경우
        print(extracted_text)  # 추출된 텍스트를 출력합니다.
