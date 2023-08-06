namespace java com.didapinche.thrift.dm.proxy.dm_eta_service

struct TPoint {
    1: double lon;
    2: double lat;
}

struct TLine {
    1: TPoint startPoint;
    2: TPoint endPoint;
    3: i64 id;
}

struct TResult {
    1: i16 code;  // 0-success else-fail
    2: string msg;
    3: map<i64, i32> distances;  // key-lineId value-distance
}

service DMEtaService{
	i32 getDistance(1:i32 cityid, 2:double slon, 3:double slat, 4:double elon, 5:double elat);
	list<TPoint> getRoutine(1:i32 cityid, 2:double slon, 3:double slat, 4:double elon, 5:double elat);
	TResult getBatchDistance(1:i32 cityid, 2:list<TLine> lines);
}