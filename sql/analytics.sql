select * from (select device_id, max(value) as `max temp`, min(value) as `min temp`, 
                     avg(value) as `avg temp` from temperature_history group by device_id) a 
      natural join (select device_id, max(value) as `max humidity`, min(value) as `min humidity`,
                     avg(value) as `avg humidity`  from humidity_history group by device_id) b ;

select * from (
        select date(time_stamp) as `day`, device_id, count(*) as `tot`, 
        max(value) as `max hum`, min(value) as `min hum`, avg(value) as `avg hum`  
        from humidity_history group by device_id, day) a    
      natural join (   
        select date(time_stamp) as `day`, device_id, count(*) as `tot`, 
        max(value) as `max temp`, min(value) as `min temp`, avg(value) as `avg temp`  
        from temperature_history group by device_id, day) b order by day, device_id;

