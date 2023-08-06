namespace java com.didapinche.thrift.dm.proxy.dm_trace_query_service

struct Location {
    1:string lon,
	2:string lat,
	3:string time
}

service DmTraceQueryService {
	list<Location> locationsQuery(1:string userId,2:string beginTime,3:string endTime,4:i32 compress)
}