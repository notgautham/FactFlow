import torch
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

def get_model(model_name="roberta-base", num_labels=3):
    """ Load the RoBERTa model for 3-class sequence classification. """
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    return model

def train_model(model, train_dataset, val_dataset, tokenizer):
    """ Fine-tune the model using Hugging Face Trainer with label smoothing. """
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
        report_to="none",
        label_smoothing_factor=0.1  # prevents overconfidence
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
