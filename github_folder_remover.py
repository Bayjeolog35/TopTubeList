import os
import subprocess
import argparse

def delete_folders(repo_path, folders_to_delete, commit_message="Deleted folders"):
    """
    GitHub deposundan belirtilen klasörleri siler.
    
    :param repo_path: Yerel repo yolu (örneğin: "/home/user/my_repo").
    :param folders_to_delete: Silinecek klasörlerin listesi (örneğin: ["temp/", "docs/"]).
    :param commit_message: Git commit mesajı.
    """
    try:
        # Repo dizinine git
        os.chdir(repo_path)
        
        # Klasörleri sil
        for folder in folders_to_delete:
            subprocess.run(["git", "rm", "-r", "--cached", folder], check=True)
            print(f"✅ Klasör silindi: {folder}")
        
        # Commit ve push işlemleri
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Değişiklikler GitHub'a gönderildi.")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Hata oluştu: {e}")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    # Argümanları ayarla
    parser = argparse.ArgumentParser(description="GitHub'dan klasör silme aracı")
    parser.add_argument("--repo", required=True, help="Yerel repo yolu")
    parser.add_argument("--folders", nargs="+", required=True, help="Silinecek klasörler (örneğin: 'temp/ docs/')")
    parser.add_argument("--message", default="Deleted folders", help="Commit mesajı")
    
    args = parser.parse_args()
    
    # Fonksiyonu çağır
    delete_folders(args.repo, args.folders, args.message)
