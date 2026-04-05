### [가상환경 설정 (Conda)]

### 0. VS Code를 '관리자 권한'으로 실행하기

### 1. Conda 기존 환경 종료하기
conda deactivate

### 2. 프로젝트용 가상환경 만들기
conda create -n smart_pill python=3.10.12 -y

### 3. 환경 활성화하기
conda activate smart_pill

### 4. 필수 라이브러리 설치하기
### (주의: requirements.txt 파일이 있는 디렉토리에서 실행)
pip install -r requirements.txt

---

## 📂 프로젝트 폴더 구조 (Project Structure)

본 프로젝트는 대용량 AI 학습 데이터를 효율적으로 관리하기 위해 **MLOps 표준 구조**를 따릅니다.

```text
/SMART-PILL-PROJECT
├── 📂 data
│   ├── 📂 raw                 # ⚠️ 원본 데이터 (수정 금지, 백업용)
│   │   ├── 📂 aihub_pill      # AI Hub에서 다운로드한 데이터
│   │   │   ├── 📂 images      # 원천 이미지 (.jpg, .png)
│   │   │   └── 📂 labels      # 원본 라벨 (.json)
│   │   ├── 📂 google_crawling # 구글 크롤링 수집 데이터
│   │   └── 📂 youtube_capture # 유튜브 영상 캡처 데이터
│   ├── 📂 interim             # 중간 산출물 (분석용 CSV, 요약본 등)  
│   ├── 📂 processed           # 🛠️ 전처리 완료 데이터 (640x640 리사이징 등)
│   └── 📂 augmented           # 데이터 증강(Augmentation) 적용 데이터
├── 📂 models                  # 학습 완료된 모델 가중치 저장 (.pth, .onnx)
├── 📂 src                     # 소스 코드 (Source Code)
├── .gitignore                 # 대용량 데이터 및 가상환경 업로드 방지
├── README.md                  # 프로젝트 매뉴얼
└── requirements.txt           # 라이브러리 설치 목록 (pandas, glob 등)