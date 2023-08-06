namespace java com.didapinche.dm.ac.thrift.sexyUserCheck

service SexyUserCheckService{
    bool isSexyUser(1:i32 userid)
    set<i32> checkMultiUser(1:set<i32> userset)
    set<i32> multiUserFilter(1:set<i32> userSet)
}