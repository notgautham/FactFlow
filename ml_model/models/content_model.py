import torch
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

def get_model(model_name="roberta-base", num_labels=2):
    """ Load the RoBERTa model for sequence classification. """
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    return model

def train_model(model, train_dataset, val_dataset, tokenizer):
    """
    Fine-tune the model on the dataset using Hugging Face Trainer.
    Tokenizer is included to enable preprocessing and evaluation logging.
    """
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        report_to="none",  # Disables default logging to W&B
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
    )

    trainer.train()
    return trainer
