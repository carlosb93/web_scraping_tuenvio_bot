/*
 Navicat Premium Data Transfer

 Source Server         : bot_tuenvio
 Source Server Type    : SQLite
 Source Server Version : 3021000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3021000
 File Encoding         : 65001

 Date: 24/07/2020 08:44:59
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for settings
-- ----------------------------
DROP TABLE IF EXISTS "settings";
CREATE TABLE "settings" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(255),
  "code" VARCHAR(255),
  "setting_type" VARCHAR(255),
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of settings
-- ----------------------------
INSERT INTO "settings" VALUES (1, 'Pollo Muslo', 'chickenm', 'alert');
INSERT INTO "settings" VALUES (2, 'Pollo Pechuga', 'chickenp', 'alert');
INSERT INTO "settings" VALUES (3, 'Detergente', 'detergente', 'alert');
INSERT INTO "settings" VALUES (4, 'Pasta Dental', 'pastadental', 'alert');
INSERT INTO "settings" VALUES (5, 'Papel Sanitario', 'papelrollo', 'alert');
INSERT INTO "settings" VALUES (6, 'Atun', 'atun', 'alert');
INSERT INTO "settings" VALUES (7, 'Sardina', 'sardina', 'alert');
INSERT INTO "settings" VALUES (8, 'Shampoo', 'shampoo', 'alert');
INSERT INTO "settings" VALUES (9, 'Acondicionador', 'aconditioner', 'alert');
INSERT INTO "settings" VALUES (10, 'Aceite', 'oil', 'alert');
INSERT INTO "settings" VALUES (11, '5ta y 42', 'https://5tay42.enzona.net/nuevos-productos', 'url');
INSERT INTO "settings" VALUES (12, 'Carlos 3ro', 'https://www.tuenvio.cu/carlos3/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (13, 'Cuatro Caminos', 'https://www.tuenvio.cu/4caminos/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (14, 'Tipica de Boyeros', 'https://www.tuenvio.cu/tipicaboyeros/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (15, 'Villa Diana', 'https://www.tuenvio.cu/caribehabana/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (16, 'El Pedregal', 'https://www.tuenvio.cu/tvpedregal/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (17, 'Artemisa', 'https://www.tuenvio.cu/artemisa/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (18, 'Picadillo', 'picadillo', 'alert');

PRAGMA foreign_keys = true;
