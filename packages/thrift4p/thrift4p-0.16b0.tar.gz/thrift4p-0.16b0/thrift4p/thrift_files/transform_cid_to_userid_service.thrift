namespace java com.didapinche.thrift.dm_cidreflection

service CidReflectionService {
    i32 getUserId(1:string cid)
    list<i32> getMutiUserId(1:list<string> cidarr)
    i32 getMapCount()
}