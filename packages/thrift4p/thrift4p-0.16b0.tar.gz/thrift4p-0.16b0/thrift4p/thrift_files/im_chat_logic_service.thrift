namespace java com.didapinche.im.logic

struct ChatMessage {
    1:required i32 msg_type;
    2:required i64 timestamp;
    3:required string message;
}

struct ChatMessageWrapper{
    1:required i64 syncKey;
    2:required ChatMessage message;
}

typedef list<ChatMessageWrapper> ChatMessageList

struct ChatSyncRet{
    1:required ChatMessageList data ;
    2:required bool finish;
}

exception ChatLogicException {
    1: i32 code;
    2: string message;
}

struct User{
    1:string cid;
    2:i32 packageType;
}

// 已读消息相关
struct ChatRMessageWrapper{
    1: required i64 syncKey;
    2: required i64 message;
}
struct ChatRSyncRet {
    1: required list<ChatRMessageWrapper> data;
    2: required bool finish;
}


service ImChatLogicService {
    void send(1:string sender,2:string receiver,3:ChatMessage message) throws (1:ChatLogicException e);
    i64 send4Comet(1:User sender,2:User receiver,3:ChatMessage message) throws (1:ChatLogicException e);
    ChatSyncRet sync(1:User cid,2:User sid,3:i64 syncKey) throws (1:ChatLogicException e);
    void syncFin(1:User cid,2:User sid,3:i64 syncKey) throws (1:ChatLogicException e);
    void subscribe(1:string cid1,2:string cid2)  throws (1:ChatLogicException e);
    void subscribeByPlat(1:string cid1,2:string cid2,3:i32 exp,4:i32 platType)  throws (1:ChatLogicException e);
    void subscribeExp(1:string cid1,2:string cid2,3:i32 exp)  throws (1:ChatLogicException e);
    void unSubscribe(1:string cid1,2:string cid2)  throws (1:ChatLogicException e);
    void loadNotifies(1:User cid)  throws (1:ChatLogicException e);
    void deleteTempRelation(1:string cid1,2:string cid2)  throws (1:ChatLogicException e);
    // 使用User代替cid
    void sendUser(1:User sender,2:User receiver,3:ChatMessage message) throws(1:ChatLogicException e);
    void subscribeUser(1:User sender,2:User receiver) throws (1:ChatLogicException e);
    void subscribeUserExp(1:User sender,2:User receiver,3:i32 exp) throws (1:ChatLogicException e);
    void unSubscribeUser(1:User user1,2:User user2)  throws (1:ChatLogicException e);
    void deleteUserTempRelation(1:User user1,2:User user2)  throws (1:ChatLogicException e);
    // 已读未读相关
    void rsend(1:User sender,2:User receiver,3:i64 syncKey) throws(1:ChatLogicException e);
    ChatRSyncRet rsync(1:User sender,2:User receiver,3:i64 syncKey) throws(1:ChatLogicException e);
    void rsyncFin(1:User sender,2:User receiver,3:i64 syncKey) throws(1:ChatLogicException e);
    i64 hasUnread(1:User sender,2:User receiver) throws(1:ChatLogicException e);
}

