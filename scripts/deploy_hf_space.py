from huggingface_hub import HfApi, Repository
import os
import shutil
from pathlib import Path

def deploy_to_hf_spaces():
    """Deploy application to Hugging Face Spaces"""
    
    # Space configuration
    space_name = "job-matching-mlops"
    space_type = "docker"  # docker, streamlit, gradio
    
    # Create space if it doesn't exist
    api = HfApi()
    try:
        api.create_repo(
            repo_id=f"your-username/{space_name}",
            repo_type="space",
            space_sdk=space_type,
            private=False
        )
        print(f"Created space: {space_name}")
    except:
        print(f"Space {space_name} already exists")
    
    # Clone space repo
    repo = Repository(
        local_dir=f"/tmp/{space_name}",
        clone_from=f"https://huggingface.co/spaces/your-username/{space_name}",
        use_auth_token=os.environ.get("HF_TOKEN")
    )
    
    # Copy application files
    shutil.copytree(".", f"/tmp/{space_name}", dirs_exist_ok=True)
    
    # Create space metadata
    with open(f"/tmp/{space_name}/README.md", "w") as f:
        f.write(f"""
---
title: Job Matching MLOps
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8000
---

# Job Matching System with MLOps

End-to-end job matching system with:
- RAG-based matching
- MLflow experiment tracking
- Prometheus + Grafana monitoring
- Automated CI/CD
        """)
    
    # Push to HF Spaces
    repo.push_to_hub()
    print("Deployed to Hugging Face Spaces!")

if __name__ == "__main__":
    deploy_to_hf_spaces()