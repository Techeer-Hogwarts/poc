import os
import pdfplumber
import re

def extract_text_with_page_numbers(filename, input_path, output_path):
    """PDF 파일에서 텍스트를 추출하고, 줄바꿈을 다 없애서, 이를 텍스트 파일로 저장합니다."""
    output_path_txt = os.path.join(output_path, filename + '.txt')  # 텍스트 파일을 저장할 경로를 설정합니다.
    try:
        with pdfplumber.open(input_path) as pdf:                     # pdfplumber를 사용하여 입력 경로의 PDF 파일을 엽니다.
            text = ''                                                # 추출된 텍스트를 저장할 빈 문자열을 초기화합니다.
            total_pages = len(pdf.pages)                             # 전체 페이지 수를 가져옵니다.
            for i, page in enumerate(pdf.pages, start=1):            # 모든 페이지를 순회합니다. 페이지 번호는 1부터 시작합니다.
                page_text = page.extract_text()                      # 현재 페이지에서 텍스트를 추출합니다.
                if page_text:                                        # 페이지에서 텍스트를 성공적으로 추출한 경우
                    page_text = page_text.replace('\n', '')          # 줄바꿈을 없애고 추출된 텍스트를 누적합니다.
                    page_text = format_text(page_text)
                if i != total_pages:
                    patterns = [
                        "표준명 취업규칙",
                        "표준코드 개정번호 GHS-L11C-01-00 12 기안부서 HR경영팀 기안일자 2022.11.16 적용범위 전사 시행일자 2022.11.01.",
                        "취업규칙한국타이어앤테크놀로지 주식회사표준코드 개정번호GHS-L11C-01-00 12기안부서 HR경영팀 기안일자 2022.11.16적용범위 전사 시행일자 2022.11.01.",
                        "한국타이어앤테크놀로지 주식회사",
                        r"\d{1,2}(?=\s*표준코드 개정번호GHS-L11C-01-00\s*12\s*기안부서 HR경영팀\s*기안일자\s*2022\.11\.16\s*적용범위\s*전사\s*시행일자\s*2022\.11\.01\.)",
                        '취업규칙표준코드 개정번호GHS-L11C-01-00 12기안부서 HR경영팀 기안일자 2022.11.16적용범위 전사 시행일자 2022.11.01.목 차',
                        '표준코드 개정번호표준명 취업규칙GHS-L11C-01-00 12기안부서 HR경영팀 기안일자 2022.11.16적용범위 전사 시행일자 2022.11.01.1. ',
                        '표준코드 개정번호GHS-L11C-01-00 12기안부서 HR경영팀 기안일자 2022.11.16적용범위 전사 시행일자 2022.11.01.'
                    ]
                    for pattern in patterns:
                        # 정규 표현식을 사용하는 경우 re.sub 함수를 사용합니다.
                        if re.match(r'\d{1,2}', pattern):  # 정규 표현식이 숫자 패턴인 경우
                            page_text = re.sub(pattern, '', page_text, 1)
                        else:
                            page_text = page_text.replace(pattern, '', 1)
                text += page_text
            print(text)
            with open(output_path_txt, 'w', encoding='utf-8') as outfile:  # 추출된 텍스트를 저장할 파일을 엽니다.
                outfile.write(text)                                  # 추출된 텍스트를 파일에 씁니다.
    except Exception as e:
        print(f"Error: Can't open PDF file. {e}")                          # PDF 파일을 열 수 없는 경우 오류 메시지를 출력합니다.

def createDirectory(directory):
    """주어진 경로에 디렉토리를 생성합니다. 디렉토리가 이미 존재하지 않는 경우에만 생성합니다."""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)  # 디렉토리가 존재하지 않으면 생성합니다.
    except OSError as e:
        print(f"Error: Failed to create the directory. {e}")  # 디렉토리 생성에 실패한 경우 오류 메시지를 출력합니다.

if __name__ == '__main__':
    # 입력 및 출력 디렉토리를 설정합니다.
    target_dir = "D:\Project\TChat\KB_Tech\Head\HR"
    output_dir = '../KB_Tech/Head/HR'
    createDirectory(output_dir)  # 출력 디렉토리를 생성합니다.
    newline = True  # 줄바꿈 옵션을 설정합니다.

    for (path, dir, files) in os.walk(target_dir):  # 입력 디렉토리를 순회합니다.
        for filename in files:
            ext = os.path.splitext(filename)[-1]  # 파일 확장자를 확인합니다.
            if ext == '.pdf':  # 파일이 PDF인 경우
                input_path = os.path.join(path, filename)  # 입력 파일의 전체 경로를 설정합니다.
                output_path = os.path.join(output_dir, os.path.relpath(path, target_dir))  # 출력 경로를 설정합니다.
                print("input_path ", input_path)  # 입력 경로를 출력합니다.
                print("output_path ", output_path)  # 출력 경로를 출력합니다.
                createDirectory(output_path)  # 출력 경로에 디렉토리를 생성합니다.
                extract_text_with_page_numbers(filename, input_path, output_path)  # 텍스트와 페이지 번호를 추출합니다.
