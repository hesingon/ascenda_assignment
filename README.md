# READ ME

### Performance enhancement
Since this api will query different suppliers' api to retrieve
the latest info, the retrived info can be stored in a local 
database. Since the info are unstructured data, we will use 
MongoDB.
 
We can check the updates for a set interval (e.g. every 3 hours
or 1 day)

The query of multiple supplier APIs is done using
multi-threading to minimise async latency.
 
### Further enhancement (but not implemented)
1. If we can query the 3 supplier-APIs on a specific hotel
 instead of all hotels in every request, there will be some
 performace improvement.
 

