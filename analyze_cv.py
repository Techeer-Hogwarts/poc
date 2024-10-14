import pdfplumber
import os
from langchain import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

# .env 파일을 로드하여 환경 변수 설정
load_dotenv()

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


def extract_skills_from_resume(resume_text):
    """
    이력서 텍스트에서 어떤 스킬을 가지고 있는지 GPT 모델을 사용하여 추출하는 함수

    Parameters:
        resume_text (str): 이력서에서 추출한 텍스트.

    Returns:
        str: GPT 모델이 추출한 스킬 리스트.
    """
    # 프롬프트 템플릿을 설정합니다.
    prompt_template = """
    Here is a resume text:
    {resume_text}

    Please identify and list all the skills that the person possesses based on the resume text.
    """

    # LLM (GPT-3.5 모델) 생성
    llm = ChatOpenAI(model="gpt-3.5-turbo")  # GPT-3.5-turbo 모델 사용

    # 프롬프트 템플릿을 생성
    prompt = PromptTemplate(
        input_variables=["resume_text"],
        template=prompt_template,
    )

    # LLMChain 설정
    chain = LLMChain(llm=llm, prompt=prompt)

    # 이력서 텍스트를 입력으로 사용하여 스킬을 추출하는 질의 실행
    result = chain.run(resume_text=resume_text)

    return result  # GPT 모델로부터 받은 응답 반환


if __name__ == '__main__':
    input_pdf_path = './CV/박유경.pdf'  # 예시 PDF 파일 경로
    extracted_text = extract_text_from_pdf(input_pdf_path)  # 텍스트를 추출합니다.

    if extracted_text:  # 텍스트가 정상적으로 추출된 경우
        print(extracted_text)  # 추출된 텍스트를 출력합니다.
        skills = extract_skills_from_resume(extracted_text)
        print("Extracted Skills:", skills)
