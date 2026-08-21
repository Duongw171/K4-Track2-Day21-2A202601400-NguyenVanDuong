import pandas as pd
import joblib
import boto3
from sklearn.ensemble import GradientBoostingClassifier

print("Training model on EC2...")
df_train = pd.read_csv("/home/ubuntu/data/train_batch1.csv")
X_train = df_train.drop(columns=["target"])
y_train = df_train["target"]

model = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "/home/ubuntu/models/model.joblib")
print("Saved model to /home/ubuntu/models/model.joblib")

s3 = boto3.client("s3")
s3.upload_file("/home/ubuntu/models/model.joblib", "lab21-046989631558-ap-southeast-2-an", "artifacts/current/model.joblib")
print("Uploaded model to S3 successfully!")
