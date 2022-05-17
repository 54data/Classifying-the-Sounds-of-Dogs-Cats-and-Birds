# [DL] Classifying the Sounds of Dogs Cats and Birds

### 1. 프로젝트 설명 
- [프로젝트 PPT](https://github.com/54data/Classifying-the-Sounds-of-Dogs-Cats-and-Birds/blob/main/%5BPPT%5D%20%EA%B0%9C%2C%20%EA%B3%A0%EC%96%91%EC%9D%B4%2C%20%EC%83%88%20%EC%9D%8C%EC%84%B1%20%EB%B6%84%EB%A5%98%ED%95%98%EA%B8%B0.pdf)
- 개, 고양이, 새의 음성 데이터를 통하여 음성을 분류하는 인공신경망 모델을 구축한다.  
- 인공신경망 모델을 기반으로 GUI를 구성해 사용자가 직접 음성을 넣어 테스트할 수 있도록 설계한다.
- **담당 포지션 : 인공신경망 모델 기반 GUI 구현**

### 2. 데이터 수집 및 정제  
- 총 1084개
- 개, 고양이, 새 음성 데이터를 수집하여 각각 훈련 데이터 324개, 테스트 데이터 36개로 나누고, 이후에 고양이 음성 분류 정확도 향상을 위해서 고양이 음성 데이터 4개를 훈련 데이터에 추가하였다.
- **데이터 정제 기준**  

  - 주변 소음이 큰 데이터   
  - 해당 동물 외에 다른 동물의 소리가 겹쳐있는 데이터  
  - 15초 이내의 데이터로만 구성하기 위해 긴 음성 데이터는 잘라서 사용  

### 3. 모델 구현  
3-1) 모델 목표
  - 새로운 데이터를 올바르게 분류 분석  
  - 테스트 데이터 정확도 90%이상으로 구현하기  
  - 오버피팅을 최소화하여 구현하기  

3-2) 최적의 모델 채택 과정
- 위의 목표를 기반으로 최적의 정확도를 가진 인공신경망을 구현하고자 하였고 그 결과 **완전연결계층으로 3층 신경망 모델**을 채택하였다.  
- 모델 채택 과정 중에 고양이 음성 데이터만 오분류하는 문제점이 발생하였고, 이를 해결하기 위하여 아래와 같이 진행하였다.  

    - 훈련/테스트 데이터 비율을 9:1로 수정
    - 테스트 과정 중 틀리게 분류한 4개의 음성 데이터를 훈련 데이터로 추가

### 4. GUI




  
    
  


