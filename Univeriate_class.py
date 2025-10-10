class univeriate():
   def quanqual(datapool):
       quan=datapool.select_dtypes(exclude=object)
       qual=datapool.select_dtypes(include=object)
       return qual,quan