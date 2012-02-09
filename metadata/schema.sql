/*
 Navicat Premium Data Transfer

 Source Server         : PostgreSQL @ tesla
 Source Server Type    : PostgreSQL
 Source Server Version : 90004
 Source Host           : localhost
 Source Database       : itunesconnect
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 90004
 File Encoding         : utf-8

 Date: 12/06/2011 16:58:47 PM
*/

-- ----------------------------
--  Sequence structure for "id_app_seq"
-- ----------------------------
DROP SEQUENCE IF EXISTS "id_app_seq";
CREATE SEQUENCE "id_app_seq" INCREMENT 1 START 24 MAXVALUE 9223372036854775807 MINVALUE 1 CACHE 1;
ALTER TABLE "id_app_seq" OWNER TO "postgres";

-- ----------------------------
--  Table structure for "itunes"
-- ----------------------------
DROP TABLE IF EXISTS "itunes";
CREATE TABLE "itunes" (
	"sku" varchar(100),
	"end_date" date,
	"customer_currency" varchar(3),
	"begin_date" date,
	"developer_proceeds" int8,
	"promo_code" varchar(100),
	"title" varchar(100),
	"parent_identifier" varchar(100),
	"customer_price" float4,
	"period" varchar(100),
	"currency_of_proceeds" varchar(3),
	"type_identifier" varchar(100),
	"provider_country" varchar(2),
	"country_code" varchar(2),
	"apple_identifier" varchar(100),
	"version" varchar(20),
	"provider" varchar(20),
	"units" int8,
	"subscription" varchar(100),
	"developer" varchar(100),
	"id" int8 NOT NULL DEFAULT nextval('id_app_seq'::regclass),
	"publisher_name" varchar(100),
	"publisher_id" varchar(100)
)
WITH (OIDS=FALSE);
ALTER TABLE "itunes" OWNER TO "postgres";

-- ----------------------------
--  Function structure for mtd_downloads(text, text, int8, int8)
-- ----------------------------
DROP FUNCTION IF EXISTS "mtd_downloads"(text, text, int8, int8);
CREATE FUNCTION "mtd_downloads"(IN text, IN text, IN int8, IN int8) RETURNS "int8" 
	AS $BODY$

SELECT 
	SUM(units)::int8 FROM itunes
WHERE 
	extract(month from begin_date) = $3 AND
	extract(year from begin_date) = $4 AND
	title = $1 AND
	version = $2 AND
	type_identifier = '1';

$BODY$
	LANGUAGE sql
	COST 100
	CALLED ON NULL INPUT
	SECURITY INVOKER
	VOLATILE;
ALTER FUNCTION "mtd_downloads"(IN text, IN text, IN int8, IN int8) OWNER TO "postgres";

-- ----------------------------
--  Function structure for mtd_updates(text, text, int8, int8)
-- ----------------------------
DROP FUNCTION IF EXISTS "mtd_updates"(text, text, int8, int8);
CREATE FUNCTION "mtd_updates"(IN text, IN text, IN int8, IN int8) RETURNS "int8" 
	AS $BODY$

SELECT 
	SUM(units)::int8 FROM itunes
WHERE 
	extract(month from begin_date) = $3 AND
	extract(year from begin_date) = $4 AND
	title = $1 AND
	version = $2 AND
	type_identifier = '7';

$BODY$
	LANGUAGE sql
	COST 100
	CALLED ON NULL INPUT
	SECURITY INVOKER
	VOLATILE;
ALTER FUNCTION "mtd_updates"(IN text, IN text, IN int8, IN int8) OWNER TO "postgres";

-- ----------------------------
--  Primary key structure for table "itunes"
-- ----------------------------
ALTER TABLE "itunes" ADD CONSTRAINT "itunes_pkey" PRIMARY KEY ("id") NOT DEFERRABLE INITIALLY IMMEDIATE;