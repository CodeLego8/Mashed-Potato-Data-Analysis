import os
import pandas as pd
from pca.repository.pca_repository_impl import PCARepositoryImpl

class PCAServiceImpl:
    def __init__(self):
        self.repository = PCARepositoryImpl()
        self.data_path = os.getenv("PROCESSED_DATA_PATH", "resource/preprocessed_data.csv")

    async def performPCA(self):
        # 데이터 로드
        data = self.repository.loadData(self.data_path)

        # 주요 분석 컬럼 정의
        analysis_columns = [
            '구매 횟수', '평균 거래 금액', '평점', '평균 평점', '가입 기간', '평균 거래 주기'
        ]
        selected_data = data[analysis_columns]

        # 데이터 스케일링
        scaled_data, _ = self.repository.scaleData(selected_data)

        # PCA 적용
        n_components = 5  # 주성분 수
        pca, transformed_data, explained_variance, components = self.repository.applyPCA(scaled_data, analysis_columns, n_components)

        # 결과 저장
        output_path = os.getenv("PCA_RESULT_PATH", "resource/pca_result.csv")
        transformed_df = pd.DataFrame(transformed_data, columns=[f"PC{i+1}" for i in range(n_components)])
        transformed_df.to_csv(output_path, index=False)

        # 주성분 가중치 시각화
        self.repository.createHeatmap(components, analysis_columns)

        # 결과 반환
        return {
            "message": "PCA completed successfully",
            "explained_variance": explained_variance.tolist(),
            "components": components.to_dict(),
            "output_path": output_path
        }