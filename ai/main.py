import argparse

from argparse import RawDescriptionHelpFormatter

def parse_args():
	parser = argparse.ArgumentParser(
		description="""
		Cyclonic AI CLI: Train, predict, and evaluate wind forecasting models
		For sub-command help sections, enter a sub-command followed by -h
		Example Usage: python .\\main.py train -h
		""", formatter_class=RawDescriptionHelpFormatter
	)

	subparsers = parser.add_subparsers(dest="command", required=True)

	train_parser = subparsers.add_parser("train", help="Train the model", description="Train a wind forecasting model using LSTM")
	train_parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
	train_parser.add_argument("--lr", type=float, default=0.005, help="Learning rate")
	train_parser.add_argument("--dropout", type=float, default=0.3, help="Dropout rate")
	train_parser.add_argument("--optimizer", default="rmsprop", help="Optimizer to use")
	train_parser.add_argument("--noplot", action="store_true", help="Disable the result plot after training")

	predict_parser = subparsers.add_parser("predict", help="Make a prediction", description="Make a prediction using the saved trained model")
	predict_parser.add_argument("--input", required=False, default="input/result.json", help="Path to the input data")
	predict_parser.add_argument("--output", required=False, default="output/prediction.json", help="Path to save the predictions to")

	evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate Model", description="Evaluate model performance by examining in-depth metrics")

	tune_parser = subparsers.add_parser("tune", help="Tune Model", description="Find the best parameters for the model using different (Hyperparameter Tuning)")

	return parser.parse_args()

if __name__ == "__main__":
	args = parse_args()

	# Import core AI modules here to not load Tensorflow if help section is invoked
	from core.trainer import train
	from core.evaluator import evaluate
	from core.predictor import predict
	from core.tuner import run_grid_search

	if args.command == "train":
		train(epochs=args.epochs, lr=args.lr, dropout=args.dropout, optimizer_name=args.optimizer, no_plotting=args.noplot)
	elif args.command == "evaluate":
		evaluate()
	elif args.command == "predict":
		predict(input_path=args.input, output_path=args.output)
	elif args.command == "tune":
		run_grid_search()