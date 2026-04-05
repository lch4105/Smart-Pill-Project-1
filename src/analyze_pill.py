import pandas as pd
import os

def select_strategic_50(df):
    final_list = []

    # 전략 1: 색상 중심 (CNN 기본 분류용 - 약 20종)
    # 주요 색상별로 데이터가 가장 많은(이미지 수가 많은) 알약들을 선별합니다.
    colors = ['하양', '노랑', '주황', '분홍', '빨강', '갈색', '연두', '초록', '청록', '파랑', '보라', '자주']
    for color in colors:
        # 해당 색상 중 알약별 이미지 개수 확인 후 상위 2종 추출
        sample = df[df['color_class1'] == color].groupby('pill_name').filter(lambda x: len(x) >= 100)
        if not sample.empty:
            top_pills = sample['pill_name'].value_counts().head(2).index
            final_list.append(df[df['pill_name'].isin(top_pills)].drop_duplicates('pill_name'))
    
    # 전략 2: 제형 및 모양 중심 (기하학적 특징용 - 약 15종)
    # 원형 외의 특이 제형들을 우선적으로 포함합니다.
    shapes = ['장방형', '타원형', '삼각형', '사각형', '오각형', '육각형', '팔각형']
    for shape in shapes:
        sample = df[df['drug_shape'] == shape].groupby('pill_name').filter(lambda x: len(x) >= 100)
        if not sample.empty:
            top_pills = sample['pill_name'].value_counts().head(2).index
            final_list.append(df[df['pill_name'].isin(top_pills)].drop_duplicates('pill_name'))

    # 전략 3: 각인이 뚜렷한 약 (OCR 성능 검증용 - 약 15종)
    # 각인(print_front) 텍스트가 존재하고 데이터가 많은 것들 위주
    ocr_sample = df[df['print_front'].fillna('').str.len() >= 1].groupby('pill_name').filter(lambda x: len(x) >= 100)
    if not ocr_sample.empty:
        top_ocr_pills = ocr_sample['pill_name'].value_counts().head(15).index
        final_list.append(df[df['pill_name'].isin(top_ocr_pills)].drop_duplicates('pill_name'))

    # 결과 통합 및 중복 제거 후 최종 50종 확정
    result_df = pd.concat(final_list).drop_duplicates('pill_name').head(50)
    return result_df

if __name__ == "__main__":
    # 1. 갱신된 상세 정보 CSV 로드
    CSV_PATH = 'data/interim/label_summary.csv'
    
    if not os.path.exists(CSV_PATH):
        print(f"❌ {CSV_PATH} 파일이 없습니다. preprocess.py를 먼저 실행하세요.")
    else:
        df = pd.read_csv(CSV_PATH)
        
        # 2. 전략적 추출 실행
        target_50 = select_strategic_50(df)
        
        if not target_50.empty:
            print(f"--- 🎯 전략 기반 타겟 50종 선별 완료 (총 {len(target_50)}종) ---")
            print(target_50[['pill_name', 'drug_shape', 'color_class1', 'print_front']].head(20))
            
            # 3. 최종 리스트 저장 (이 리스트가 '핀셋 압축 해제'의 기준이 됩니다)
            os.makedirs('data/interim', exist_ok=True)
            target_50.to_csv('data/interim/strategic_50_pills.csv', index=False, encoding='utf-8-sig')
            print(f"\n💾 저장 완료: data/interim/strategic_50_pills.csv")
        else:
            print("❌ 조건에 맞는 알약을 찾지 못했습니다. CSV의 컬럼명을 확인하세요.")