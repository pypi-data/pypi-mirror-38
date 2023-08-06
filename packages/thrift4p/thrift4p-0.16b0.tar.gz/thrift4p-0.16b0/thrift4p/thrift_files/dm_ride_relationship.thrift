namespace java com.didapinche.thrift.dm_ride_relationship

service RideRelationshipService {
   bool HaveRideRelationship(1:i32 driver_user_id,2:i32 initiator_user_id);
   i32 GetRideRelationshipCount(1:i32 driver_user_id,2:i32 initiator_user_id);
   
   map<i32,bool> HaveRideRelationshipBatch(1:i32 driver_user_id,2:set<i32> initiator_user_ids);
   map<i32,i32> GetRideRelationshipBatchCount(1:i32 driver_user_id,2:set<i32> initiator_user_ids);
   
   bool GiveReviewSubsidy(1:i32 driver_user_id);
   i32 GetReviewSubsidyCount(1:i32 driver_user_id);
}