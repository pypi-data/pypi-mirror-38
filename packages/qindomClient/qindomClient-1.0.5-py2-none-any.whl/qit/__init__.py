from qit.Qclient import Qclient

if __name__ == "__main__":
    client = Qclient('wangbo', 'C3783151-AE12-4F18-BA6D-FA1F024E3178')
    #
    # r = client.train_model_s3(
    #     training_data="wangbo/census_train_X_y_df.csv", clf_type='QBOOST_IT')
    #
    # modelId = r['body']
    # print(modelId)
    #print(client.predict_sync("wangbo/census_valid_X.csv", modelId=141872))
    print(client.get_methods());
    print(client.get_token());
