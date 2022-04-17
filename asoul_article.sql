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

 Date: 17/04/2022 12:14:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for asoul_article
-- ----------------------------
DROP TABLE IF EXISTS `asoul_article`;
CREATE TABLE `asoul_article`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `tid` int NOT NULL,
  `order` int NULL DEFAULT NULL,
  `textdata` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `tid`(`tid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 139824 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
