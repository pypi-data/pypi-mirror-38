# lp_mongodb
MongoDB storage adapter for thumbor.

# Versions

This projects uses the following versioning scheme:

`<thumbor major>.<mongodb plugin major>.<mongodb plugin minor>`


# Configuration
```
# MONGO STORAGE OPTIONS
MONGO_LP_SERVER_HOST = 'localhost' # MongoDB storage server host
MONGO_LP_SERVER_PORT = 27017 # MongoDB storage server port
MONGO_LP_SERVER_DB = 'thumbor' # MongoDB storage server database name
MONGO_LP_SERVER_COLLECTION = 'images' # MongoDB storage image collection
MONGO_LP_DOC_FIELD = 'content' #document field used for image content
```
