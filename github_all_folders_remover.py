# github_all_folders_remover.py

import os
import subprocess
import argparse

def delete_all_folders_in_path(repo_path, target_directory="", commit_message="GitHub Action: All specified folders deleted"):
    """
    GitHub deposunda, belirtilen hedef dizin altındaki tüm alt klasörleri siler.
    
    :param repo_path: Yerel repo yolu (örneğin: "/home/runner/work/my_repo/my_repo").
    :param target_directory: Klasörlerin silineceği ana dizin (repo_path'e göre). Varsayılan olarak repo kökü.
    :param commit_message: Git commit mesajı.
    """
    try:
        # Repo dizinine git
        os.chdir(repo_path)
        print(f"Working directory changed to: {os.getcwd()}")

        # Hedef dizine git (varsa)
        full_target_path = os.path.join(repo_path, target_directory)
        if not os.path.isdir(full_target_path):
            print(f"❌ Hedef dizin bulunamadı: {full_target_path}")
            return
        
        print(f"Scanning for folders in: {full_target_path}")

        # Hedef dizindeki tüm alt klasörleri listele
        # Sadece dizinleri al, dosyaları değil
        folders_to_delete = [
            d for d in os.listdir(full_target_path) 
            if os.path.isdir(os.path.join(full_target_path, d)) and not d.startswith('.') and d != '.git'
        ]
        
        if not folders_to_delete:
            print("ℹ️ Silinecek bir klasör bulunamadı.")
            return

        print(f"Found folders to delete: {', '.join(folders_to_delete)}")
        
        deleted_count = 0
        for folder in folders_to_delete:
            folder_full_path = os.path.join(full_target_path, folder)
            
            try:
                # Git'ten klasörü kaldırmaya çalış
                # NOT: Eğer klasörü hem Git'ten hem de fiziksel olarak silmek isterseniz:
                # subprocess.run(["git", "rm", "-r", folder_full_path], check=True)
                # print(f"✅ Klasör fiziksel olarak ve Git indeksinden silindi: {folder_full_path}")

                # Eğer sadece Git indeksinden kaldırıp, fiziksel olarak bırakmak isterseniz (genelde istenmez):
                subprocess.run(["git", "rm", "-r", "--cached", folder_full_path], check=True)
                print(f"✅ Klasör Git indeksinden silindi: {folder_full_path}")
                deleted_count += 1

            except subprocess.CalledProcessError as e:
                # Klasör zaten Git tarafından izlenmiyorsa veya başka bir hata varsa
                print(f"❌ Hata oluştu '{folder_full_path}' silinirken: {e.stderr.decode().strip()}")
            except Exception as e:
                print(f"❌ Beklenmeyen hata '{folder_full_path}' işlenirken: {e}")

        if deleted_count > 0:
            # Commit ve push işlemleri
            try:
                subprocess.run(["git", "commit", "-m", commit_message], check=True)
                subprocess.run(["git", "push"], check=True)
                print("🚀 Değişiklikler GitHub'a gönderildi.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Commit/Push sırasında hata oluştu: {e.stderr.decode().strip()}")
        else:
            print("ℹ️ Silinecek bir değişiklik yapılmadı. Commit ve push atlanıyor.")
            
    except Exception as e:
        print(f"❌ Genel hata oluştu: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub'dan belirli bir dizindeki tüm klasörleri silme aracı.")
    parser.add_argument("--repo", required=True, help="Yerel repo yolu (örneğin: /home/runner/work/my_repo/my_repo).")
    parser.add_argument("--target_dir", default="", help="Klasörlerin silineceği ana dizin (repo_path'e göre). Varsayılan olarak repo kökü.")
    parser.add_argument("--message", default="GitHub Action: All specified folders deleted", help="Commit mesajı.")
    
    args = parser.parse_args()
    
    delete_all_folders_in_path(args.repo, args.target_dir, args.message)
