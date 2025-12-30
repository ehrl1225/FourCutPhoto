
# FourCutPhoto

"FourCutPhoto"는 PyQt6를 사용하여 만든 네 컷 사진 촬영 프로그램입니다. 사용자는 다양한 프레임을 선택하고, 사진을 찍고, 최종 결과물을 인쇄할 수 있습니다.

## 주요 기능

- **프레임 선택**: 다양한 디자인의 프레임을 선택할 수 있습니다.
- **사진 촬영**: 웹캠을 사용하여 4장 또는 6장의 사진을 연속으로 촬영합니다.
- **사진 선택**: 촬영된 사진 중 마음에 드는 사진을 선택하여 최종 이미지를 구성할 수 있습니다. (프레임에 따라 자동 선택될 수도 있습니다.)
- **이미지 합성**: 선택된 사진과 프레임을 자동으로 합성합니다.
- **인쇄**: 완성된 네 컷 사진을 프린터로 인쇄합니다.
- **전체 화면 모드**: 실제 포토 부스처럼 전체 화면으로 실행됩니다.

## 프로젝트 구조

```
D:/programing/FourCutPhoto/
├───setup.py                # 프로젝트 설정 파일
├───gui/                    # GUI 관련 리소스 (이미지, 사운드)
├───img/                    # 사진 프레임 이미지
├───json/                   # 프레임 설정 JSON 파일
├───overlay_img/            # 사진 위에 올라가는 오버레이 이미지
├───result/                 # 결과물이 저장되는 폴더
├───src/                    # 소스 코드 루트
│   └───main/
│       ├───qt_main.py          # 애플리케이션 메인 실행 파일
│       ├───gui/              # GUI 위젯 및 로직
│       │   ├───widget/       # 메인 윈도우 및 화면 전환 위젯
│       │   ├───image/        # 사진 촬영/선택/인쇄 관련 위젯
│       │   └───worker/       # 백그라운드 작업 (프린팅 등)
│       ├───image/            # 이미지 처리 및 데이터 관리
│       ├───printer/          # 프린터 제어
│       └───util/             # 유틸리티 (데이터 관리 등)
└───test/                   # 테스트 코드
```

## 의존성

이 프로젝트를 실행하기 위해 다음 라이브러리가 필요합니다.

- PyQt6
- opencv-python
- pillow
- win32printing

`requirements.txt` 또는 `setup.py`를 통해 설치할 수 있습니다.

```bash
pip install PyQt6 opencv-python pillow win32printing
```

## 실행 방법

1.  저장소를 클론합니다.
    ```bash
    git clone https://github.com/your-username/FourCutPhoto.git
    ```
2.  프로젝트 디렉토리로 이동합니다.
    ```bash
    cd FourCutPhoto
    ```
3.  필요한 패키지를 설치합니다.
    ```bash
    pip install -r requirements.txt 
    ```
    (만약 `requirements.txt` 파일이 없다면 위의 의존성 섹션을 참고하여 직접 설치해주세요.)

4.  애플리케이션을 실행합니다.
    ```bash
    python src/main/qt_main.py
    ```

## 주요 조작

- 대부분의 상호작용은 화면의 버튼을 클릭하여 이루어집니다.
- 사진 촬영 시 특정 키 (예: 스페이스바 또는 엔터)를 눌러 촬영을 시작할 수 있습니다. (구현에 따라 다를 수 있음)

---
*이 README 파일은 Gemini 에이전트에 의해 생성되었습니다.*
