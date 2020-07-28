/*
 Navicat Premium Data Transfer

 Source Server         : Botniato
 Source Server Type    : SQLite
 Source Server Version : 3021000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3021000
 File Encoding         : 65001

 Date: 28/07/2020 12:40:57
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for score_board
-- ----------------------------
DROP TABLE IF EXISTS "score_board";
CREATE TABLE "score_board" (
  "id" INTEGER NOT NULL,
  "encounters_score" INTEGER NOT NULL,
  "locations_score" INTEGER NOT NULL,
  "tgid" INTEGER NOT NULL,
  PRIMARY KEY ("id")
);

PRAGMA foreign_keys = true;
