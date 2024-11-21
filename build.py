import os
import subprocess

def build_exe():
    script_name = "main.py"  # 빌드할 스크립트 이름
    exe_name = "main.exe"  # 생성될 exe 파일 이름
    dist_dir = "dist"  # 실행 파일이 저장될 디렉토리 이름

    # dist 디렉토리 생성
    os.makedirs(dist_dir, exist_ok=True)

    # PyInstaller 명령어 생성
    command = [
        "pyinstaller",
        "--onefile",        # 단일 exe 파일로 생성
        "--noconfirm",      # 기존 빌드 폴더를 덮어씀
        "--console",        # 콘솔 창을 표시 (숨기려면 "--noconsole"로 변경)
        "--name", exe_name, # 생성될 exe 파일 이름
        f"--distpath={dist_dir}",  # dist 디렉토리 경로 지정
        script_name         # 빌드할 스크립트
    ]

    print(f"명령 실행 중: {' '.join(command)}")

    try:
        subprocess.run(command, check=True)
        print("\n[완료] 빌드가 성공적으로 완료되었습니다!")
        print(f"생성된 파일은 '{dist_dir}/{exe_name}'에 있습니다.")
    except subprocess.CalledProcessError as e:
        print("\n[에러] 빌드 중 오류가 발생했습니다:")
        print(e)
    except FileNotFoundError:
        print("\n[에러] PyInstaller가 설치되지 않았습니다. 먼저 설치하세요:")
        print("pip install pyinstaller")

if __name__ == "__main__":
    build_exe()
