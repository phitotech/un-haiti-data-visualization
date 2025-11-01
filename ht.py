# 📦 1. Installer les bibliothèques nécessaires
!pip install transformers accelerate datasets peft bitsandbytes

# 🧠 2. Charger le modèle Mistral 7B
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_4bit=True,
    trust_remote_code=True
)

# 📊 3. Charger le dataset financier
from datasets import load_dataset

dataset = load_dataset("financial_phrasebank", split="train")
print("Exemple :", dataset[0])

# 🧹 4. Prétraiter les données
def preprocess(example):
    return tokenizer(example["sentence"], truncation=True, padding="max_length", max_length=128)

tokenized_dataset = dataset.map(preprocess)

# 🏋️ 5. Fine-tuning avec PEFT (LoRA)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

model = prepare_model_for_kbit_training(model)

config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)
model.print_trainable_parameters()

# 🧪 6. Entraînement avec Trainer
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    logging_dir="./logs",
    logging_steps=10,
    save_steps=500,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

# 🚀 7. Tester le modèle
input_text = "The company's quarterly results exceeded expectations."
inputs = tokenizer(input_text, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=50)
print("Réponse générée :", tokenizer.decode(outputs[0]))
