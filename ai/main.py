import argparse

from pathlib import Path

from core.trainer import train
from core.evaluator import evaluate
from core.predictor import predict

def parse_args():
	parser = argparse.ArgumentParser(
		description="Train, evaluate and use the model to predict future wind speeds"
	)

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-t", "--train", action="store_true", help="Train the model")
	group.add_argument("-e", "--evaluate", action="store_true", help="Evaluate the model")
	group.add_argument("-p", "--predict", action="store_true", help="Predict using the model")

	return parser.parse_args()

if __name__ == "__main__":
	args = parse_args()

	if args.train:
		train()
	elif args.evaluate:
		evaluate()
	elif args.predict:
		predict()