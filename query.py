# #SQL Wyciągający błędy z bazy
# rep_street_sql = """
# select
#      tags -> 'osm_user' as user,
#      tags -> 'osm_changeset' as changeset,
#      osm_id,
#        case
#          when po."addr:city" is not null and po."addr:place" is not null and po."addr:street" is not null then 'c_p_s'::text
#          when po."addr:city" is null and po."addr:place" is not null and po."addr:street" is not null then 'nc_p_s'::text
#          when po."addr:city" is null and po."addr:place" is null and po."addr:street" is not null then 'nc_np_s'::text
#          when po."addr:city" is not null and po."addr:place" is not null and po."addr:street" is null then 'c_p_ns'::text
#          when po."addr:city" is not null and po."addr:place" is null and po."addr:street"  is null then 'c_np_ns'::text
#          when po."addr:city" is null and po."addr:place" is null and po."addr:street" is null then 'nc_np_ns'::text
#          else null::text
#        end as reason,
#      'node' as type,
#      tags -> 'osm_version' as version,
#      ST_Y(ST_Transform(way,4326)) as lat,
#      ST_X(ST_Transform(way,4326)) as lon
#    from planet_osm_point po
#    where po."addr:housenumber" is not null
#    and (po.tags->'osm_timestamp')::timestamp at time zone '0:00' between (date_trunc('hour',current_timestamp) - interval '24 hour')::timestamp and current_timestamp::timestamp
#    and aba_isinpoland(po.way) = true
#    and (
#      (po."addr:city" is not null and po."addr:place" is not null and po."addr:street" is not null) or
#      (po."addr:city" is null and po."addr:place" is not null and po."addr:street" is not null) or
#      (po."addr:city" is null and po."addr:place" is null and po."addr:street" is not null) or
#      (po."addr:city" is not null and po."addr:place" is not null and po."addr:street" is null) or
#      (po."addr:city" is not null and po."addr:place" is null and po."addr:street"  is null) or
#      (po."addr:city" is null and po."addr:place" is null and po."addr:street" is null)
#    )
# union all
#    select
#      tags -> 'osm_user' as user,
#      tags -> 'osm_changeset' as changeset,
#      osm_id,
#        case
#          when po."addr:city" is not null and po."addr:place" is not null and po."addr:street" is not null then 'c_p_s'::text
#          when po."addr:city" is null and po."addr:place" is not null and po."addr:street" is not null then 'nc_p_s'::text
#          when po."addr:city" is null and po."addr:place" is null and po."addr:street" is not null then 'nc_np_s'::text
#          when po."addr:city" is not null and po."addr:place" is not null and po."addr:street" is null then 'c_p_ns'::text
#          when po."addr:city" is not null and po."addr:place" is null and po."addr:street"  is null then 'c_np_ns'::text
#          when po."addr:city" is null and po."addr:place" is null and po."addr:street" is null then 'nc_np_ns'::text
#          else null::text
#        end
#      as reason,
#      case
#          when osm_id > 0 then 'way'
#          when osm_id < 0 then 'relation'
#        end
#      as type,
#      tags -> 'osm_version' as version,
#      ST_Y(ST_Transform(ST_Centroid(way),4326)) as lat,
#      ST_X(ST_Transform(ST_Centroid(way),4326)) as lon
#    from planet_osm_polygon po
#    where po."addr:housenumber" is not null
#    and (po.tags->'osm_timestamp')::timestamp at time zone '0:00' between (date_trunc('hour',current_timestamp) - interval '24 hour')::timestamp and current_timestamp::timestamp
#    and aba_isinpoland(po.way) = true
#    and (
#      (po."addr:city" is not null and po."addr:place" is not null and po."addr:street" is not null) or
#      (po."addr:city" is null and po."addr:place" is not null and po."addr:street" is not null) or
#      (po."addr:city" is null and po."addr:place" is null and po."addr:street" is not null) or
#      (po."addr:city" is not null and po."addr:place" is not null and po."addr:street" is null) or
#      (po."addr:city" is not null and po."addr:place" is null and po."addr:street"  is null) or
#      (po."addr:city" is null and po."addr:place" is null and po."addr:street" is null)
#    )
# """

# SQL idzie długo więc zrobiłem tabelę tymczasową do developmentu
rep_street_sql = "select * from tmp_rep_test"
