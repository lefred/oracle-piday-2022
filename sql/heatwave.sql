show global status like 'rapid_%er%_status';

CALL sys.heatwave_load(JSON_ARRAY('piday'), NULL);

show global status like 'rapid_query_offload_count';

CALL sys.heatwave_advisor(JSON_OBJECT("auto_enc",JSON_OBJECT("mode", "recommend")));

CALL sys.heatwave_advisor(JSON_OBJECT("target_schema", JSON_ARRAY("piday")))

