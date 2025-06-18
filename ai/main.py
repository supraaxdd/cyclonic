import argparse

from pathlib import Path

from core.trainer import train
from core.evaluator import evaluate
from core.predictor import predict

def parse_args():
	parser = argparse.ArgumentParser(
		description="Cyclonic AI CLI: Train, predict, and evaluate wind forecasting models"
	)

	subparsers = parser.add_subparsers(dest="command", required=True)

	train_parser = subparsers.add_parser("train", help="Train the model", description="Train a wind forecasting model using LSTM")
	train_parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
	train_parser.add_argument("--lr", type=float, default=0.005, help="Learning rate")

	predict_parser = subparsers.add_parser("predict", help="Make a prediction", description="Make a prediction using the saved trained model")
	predict_parser.add_argument("--input", required=False, default="input/result.json", help="Path to the input data")
	predict_parser.add_argument("--output", required=False, default="output/prediction.json", help="Path to save the predictions to")

	evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate Model", description="Evaluate model performance by examining in-depth metrics")

	return parser.parse_args()

if __name__ == "__main__":
	args = parse_args()

	if args.command == "train":
		train(epochs=args.epochs, lr=args.lr)
	elif args.command == "evaluate":
		evaluate()
	elif args.command == "predict":
		predict(input_path=args.input, output_path=args.output)