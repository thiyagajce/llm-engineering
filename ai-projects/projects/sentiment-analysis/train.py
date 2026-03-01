"""Train and evaluate sentiment analysis model."""
import argparse
import csv
from pathlib import Path
from sentiment_analyzer import SentimentAnalyzer


def load_data(csv_path: str) -> tuple:
    """Load data from CSV file.
    
    Args:
        csv_path: Path to CSV with 'text' and 'label' columns.
        
    Returns:
        Tuple of (texts, labels).
    """
    texts = []
    labels = []
    
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                texts.append(row['text'])
                labels.append(int(row['label']))
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found. Using sample data.")
        texts = [
            'I love this product',
            'This is the worst experience',
            'Pretty good overall',
            'Not what I expected',
            'It\'s okay'
        ]
        labels = [1, 0, 1, 0, 1]
    
    return texts, labels


def main():
    parser = argparse.ArgumentParser(description='Train sentiment analysis model')
    parser.add_argument('--data', default='../../datasets/sentiment.csv', help='Path to training data CSV')
    parser.add_argument('--model-out', default='model.pkl', help='Path to save trained model')
    parser.add_argument('--test-split', type=float, default=0.2, help='Test split ratio')
    args = parser.parse_args()
    
    print("Loading data...")
    texts, labels = load_data(args.data)
    print(f"Loaded {len(texts)} samples")
    
    # Split data
    split_idx = int(len(texts) * (1 - args.test_split))
    train_texts = texts[:split_idx]
    train_labels = labels[:split_idx]
    test_texts = texts[split_idx:]
    test_labels = labels[split_idx:]
    
    print(f"Training on {len(train_texts)} samples, testing on {len(test_texts)} samples")
    
    # Train model
    print("Training model...")
    analyzer = SentimentAnalyzer()
    analyzer.train(train_texts, train_labels)
    
    # Evaluate
    if test_texts:
        accuracy = analyzer.evaluate(test_texts, test_labels)
        print(f"Model accuracy: {accuracy:.2%}")
    
    # Save model
    model_path = Path(args.model_out)
    analyzer.save_model(model_path)
    print(f"Model saved to {model_path}")
    
    # Test predictions
    print("\nSample predictions:")
    test_samples = ['I love this!', 'This is terrible', 'It\'s okay']
    for sample in test_samples:
        sentiment, confidence = analyzer.predict(sample)
        label = 'positive' if sentiment == 1 else 'negative'
        print(f"  '{sample}' -> {label} ({confidence:.2%})")


if __name__ == '__main__':
    main()
