from qit.Qclient import Qclient

if __name__ == "__main__":
    client = Qclient('jimmy', 'b4415bc3-b497-493d-9d1b-ad65beca5d44')
    # print(client.get_methods())
    print(client.get_token())
    #
    # r = client.train_model_s3(
    #     training_data="jimmy/iris_train_X_y.csv", clf_type='QBOOST_IT')
    #
    # modelId = r['body']
    # print(modelId)
    print(client.predict_sync("jimmy/ad_valid_X.csv", modelId=142079))
