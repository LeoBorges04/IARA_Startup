import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.rag_service import get_openai_client
from scripts.generate_finetune_dataset import generate_finetune_dataset

def main():
    print("=== INICIANDO PIPELINE DE FINE-TUNING DA TUTORA IARA (OPENAI GPT-4O-MINI) ===")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ds_path = os.path.join(base_dir, "data", "finetune_dataset.jsonl")

    # 1. Gerar Dataset JSONL
    generate_finetune_dataset(ds_path, target_count=250)

    # 2. Conectar à API OpenAI
    client = get_openai_client()
    if not client:
        print("❌ Erro: Chave de API da OpenAI não configurada. Defina OPENAI_API_KEY no arquivo .env.")
        return

    # 3. Fazer Upload do Arquivo no OpenAI Files
    print("\n⏳ 1/3 Fazer Upload do arquivo 'finetune_dataset.jsonl' para o OpenAI Files...")
    with open(ds_path, "rb") as f:
        file_response = client.files.create(file=f, purpose="fine-tune")
    
    file_id = file_response.id
    print(f"✅ Arquivo enviado com sucesso! File ID: {file_id}")

    # 4. Criar o Job de Fine-Tuning
    print("\n⏳ 2/3 Iniciando Job de Fine-Tuning do modelo 'gpt-4o-mini-2024-07-18'...")
    job_response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-4o-mini-2024-07-18",
        suffix="iara-tutor-pbl"
    )
    
    job_id = job_response.id
    print(f"🚀 Job de Fine-Tuning criado com sucesso!")
    print(f"   -> Job ID: {job_id}")
    print(f"   -> Modelo Base: {job_response.model}")
    print(f"   -> Status Inicial: {job_response.status}")

    # 5. Monitorar o Status do Treinamento
    print("\n⏳ 3/3 Acompanhando o progresso do treinamento (pressione Ctrl+C para sair do monitoramento)...")
    try:
        while True:
            job = client.fine_tuning.jobs.retrieve(job_id)
            status = job.status
            print(f"   [{time.strftime('%H:%M:%S')}] Status Atual: {status.upper()}")
            
            if status == "succeeded":
                ft_model_id = job.fine_tuned_model
                print("\n🎉 FINE-TUNING CONCLUÍDO COM SUCESSO!")
                print(f"============================================================")
                print(f"NOVO MODELO DEDICADO IARA: {ft_model_id}")
                print(f"============================================================")
                print(f"Para ativar o novo modelo no backend, insira a seguinte linha no seu '.env':")
                print(f"OPENAI_MODEL={ft_model_id}")
                break
            elif status in ["failed", "cancelled"]:
                print(f"❌ O Job de Fine-Tuning foi encerrado com status: {status}")
                break
                
            time.sleep(15)
    except KeyboardInterrupt:
        print(f"\n⚠️ Monitoramento pausado. O Job '{job_id}' continuará rodando nos servidores da OpenAI.")
        print(f"Você pode checar o status no painel da OpenAI (https://platform.openai.com/fine-tuning).")

if __name__ == "__main__":
    main()
