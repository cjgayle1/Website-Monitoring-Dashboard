import json

# Example JSON data - replace this with your actual JSON data
data = {
  "type": "service_account",
  "project_id": "loyal-saga-400818",
  "private_key_id": "51d91bb184ce27d5d8291703ffb1c69876c888fb",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtFsyrij3IaW2Z\nH0125SzXTrkSIkc+nj1xrXkF+ckWHtlJso5w7Vyn5mk7vLZd88q2/3dmXs4I4/3c\n9VPwWWXlECs6sgAI42flNLXLcHizvmbgG/C9J54/s0I50wnpQ3lf6Dhns2aK62PZ\nu+fKxbkjtTLKX9fdCLbz/nrRF5mowQboohZGZT0VDAYo11mjyuD88J/3IvDazI/8\ncofF2yByuxyYhCsiLSSRmkUo9NAaafYzNKmunz77KUHzuzARu6YeN5tZSXL/KHan\nNUXWfDtRnZWC+0Ggwyc1P7THurIOTU6NDnvxroqVIv43lLqhZhvtYVaYCnk0vbfF\nmbvoRryNAgMBAAECggEAG4s+RKn6DPNiAnTtwdbUXOrlHpKf3cIWqwlc8et+6Ws9\nTrIAYs4S6ZEL+/qa1rad8qMSoBLEHLwTQN81XVEMmvgIuQ1sXf26IcpSh649NvU8\nr7sigydT0nU3O7ZupFUdcnqkxzPQRJkSyapSR31RafJCw9ueoUjqvEcpyi5EQIs7\ni7Mx/zLA/O+zUSYphwwd4w9K2mx2t2QqLIhEeJ61YDuPw9hzLbY3xIWuRR9n5H98\n/mAqn8+GEp5AFLdohCBSfWqJoLHtNSW/LurSptmWunb6Gm9ZVi/zJVzh6W3HPR0a\nfT9Ec8FuMHxw/DARIFNE7/UWNXhUpHmPAVf82RxwDQKBgQDt57a1+uzOrK6WZVlo\nwmQtC/xHWtRIaIthNNT2+qLIBnhGE7778y8i5c0e5JLRo55SEKeucPNK6twT56tP\nQS5M8K1g4aSvB//dztqqRY9sRI4HOacNfRE29rTHoVK77lymT0kbpMUdoFJCvqua\nWlneAxmCG8luRRyvCh7+4/UztwKBgQC6QQraTtboad64FSXZlI2vXwS+4U0I0jYl\ntG75tc+N/FpnMDNmQ06uN8gSyBwPNRk40bBtXDRWybiaynXqAbL2s7Z8RaC9/61v\n3CiXc0Q0y/gynjnFsInSEYXc6rcuu48qoEJgZedKl7fH84V1M0cfnmGAhWvf1h6t\nl4r71H552wKBgQDbIVwlAOxQbbQeKVoSaUM2TtzfqKTx0QHY1n32w+NeFL+B5Lw8\ne8GGBl9KPkWRvYCdnGOnBLjD39I4r2IWjTYlfmZkX1J+OgMOfnLg9VNm6TpdI1hg\nzzslAlZ/rnNzUNmcAlmXkcxSPpKmkdOkR+aQ3RAIzKlb3WLPQ6ZLJxN6vwKBgGM4\nAvAIz7M/ssWdfmxKFrA1jfGhU8g/M1kipXugvtCEfiQ6KSdw85kbXhmjQE9ZmfYK\nvlGDrN4O16id8fKWtR923N+Wt+p/KYVNYtJLNSpq/ez5HQ2S3dhqPUVSRANBJyMt\n/C4eGvhBmkWKFK46gsj1Njug17aF+hG/iOpeaIHBAoGBAMcy5OLHR0WUkS+dqPHW\n0tvQhI5P50GBXTbfbKrP1fZtrYN62aqnVUjjz60XzsrkBPlE+E9YLjPr9Wib2JEk\n0K4kZh7Xbs4LiEWY+0o9FsWbE2zjP1LYDMN53jqxtPINkgrqJRBJx3siqCc6xtVf\n3hcQZeM1Q8LRLmnAZGGw5z0u\n-----END PRIVATE KEY-----\n",
  "client_email": "portfolioserviceaccount@loyal-saga-400818.iam.gserviceaccount.com",
  "client_id": "100735200179888722369",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/portfolioserviceaccount%40loyal-saga-400818.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

    # Include other fields as necessary

# Convert to single-line JSON string
json_string = json.dumps(data)

# Print the JSON string that should be used as the environment variable value
print(json_string)
