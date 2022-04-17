/*
 Navicat Premium Data Transfer

 Source Server         : 114.55.5.152_3306
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : 114.55.5.152:3306
 Source Schema         : asoul

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 17/04/2022 12:13:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for asoul_paper
-- ----------------------------
DROP TABLE IF EXISTS `asoul_paper`;
CREATE TABLE `asoul_paper`  (
  `tid` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gid` int NULL DEFAULT NULL,
  `uid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `author` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `elite` tinyint(1) NULL DEFAULT 0,
  `banned` tinyint(1) NULL DEFAULT 0,
  `create_time` timestamp(6) NULL DEFAULT NULL,
  `update_time` timestamp(6) NULL DEFAULT NULL,
  `fav_count` int NULL DEFAULT NULL,
  `comment_count` int NULL DEFAULT NULL,
  `like_count` int NULL DEFAULT NULL,
  `flag` int NULL DEFAULT NULL,
  PRIMARY KEY (`tid`) USING BTREE,
  INDEX `fav_count`(`fav_count`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
