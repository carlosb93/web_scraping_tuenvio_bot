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
INSERT INTO "settings" VALUES (1, 'Pollo Muslo', 'muslo', 'alert');
INSERT INTO "settings" VALUES (2, 'Pollo Pechuga', 'pechuga', 'alert');
INSERT INTO "settings" VALUES (2, 'Pollo', 'pollo', 'alert');
INSERT INTO "settings" VALUES (3, 'Detergente', 'Detergente', 'alert');
INSERT INTO "settings" VALUES (4, 'Pasta Dental', 'Pasta', 'alert');
INSERT INTO "settings" VALUES (5, 'Papel Sanitario', 'Papel', 'alert');
INSERT INTO "settings" VALUES (6, 'Atun', 'Atun', 'alert');
INSERT INTO "settings" VALUES (7, 'Sardina', 'Sardina', 'alert');
INSERT INTO "settings" VALUES (8, 'Shampoo', 'Champu', 'alert');
INSERT INTO "settings" VALUES (9, 'Acondicionador', 'Acondicionador', 'alert');
INSERT INTO "settings" VALUES (10, 'Aceite', 'Aceite', 'alert');
INSERT INTO "settings" VALUES (11, '5ta y 42', 'https://5tay42.enzona.net/nuevos-productos', 'url');
INSERT INTO "settings" VALUES (12, 'Carlos 3ro', 'https://www.tuenvio.cu/carlos3/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (13, 'Cuatro Caminos', 'https://www.tuenvio.cu/4caminos/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (14, 'Tipica de Boyeros', 'https://www.tuenvio.cu/tipicaboyeros/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (15, 'Villa Diana', 'https://www.tuenvio.cu/caribehabana/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (16, 'El Pedregal', 'https://www.tuenvio.cu/tvpedregal/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (17, 'Artemisa', 'https://www.tuenvio.cu/artemisa/Products?depPid=0', 'url');
INSERT INTO "settings" VALUES (18, 'Picadillo', 'picadillo', 'alert');

PRAGMA foreign_keys = true;




PRAGMA foreign_keys = false;



-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO "user" VALUES (1, 'Mr. Charlie', 'mr_charlie93', 'en', 954732565, 58467340, 1, 1595723044.60631);
INSERT INTO "user" VALUES (2, 'Lucy Hondares', NULL, 'es', 998809619, '', 1, 1595709261.54301);
INSERT INTO "user" VALUES (3, 'Amy', 'amy_bing', 'es', 916277649, NULL, 1, 1595712180.33036);
INSERT INTO "user" VALUES (4, 'Brahayan', 'BrahayanGR', NULL, 712291624, NULL, 1, 1595712745.4858);
INSERT INTO "user" VALUES (5, 'Habana', 'hhabana2020', 'es', 1187586274, NULL, 1, 1595714091.75404);
INSERT INTO "user" VALUES (6, 'Kelly', NULL, NULL, 798027302, NULL, 1, 1595714196.57729);
INSERT INTO "user" VALUES (7, 'Ena Maria', NULL, 'es', 919200586, NULL, 1, 1595741992.34843);
INSERT INTO "user" VALUES (8, 'Aracne', NULL, NULL, 1232502123, NULL, 1, 1595765754.30649);
INSERT INTO "user" VALUES (9, 'Iliana', NULL, NULL, 1348442958, 54288852, 1, 1595767225.77383);
INSERT INTO "user" VALUES (10, 'Yusielys', NULL, NULL, 1153010776, NULL, 1, 1595786898.09958);
INSERT INTO "user" VALUES (11, 'Maria de Los Ángeles', NULL, 'es', 1190210857, NULL, 1, 1595787702.41342);
INSERT INTO "user" VALUES (12, 1, NULL, NULL, 759128099, NULL, 1, 1595790258.3143);
INSERT INTO "user" VALUES (13, 'Miladys', NULL, 'es', 1095284631, '', 1, 1595791556.7775);
INSERT INTO "user" VALUES (14, 'Baby', NULL, 'es', 1208977796, NULL, 1, 1595813835.49167);
INSERT INTO "user" VALUES (15, 'Vilma', NULL, 'es', 1189539262, NULL, 1, 1595874651.12694);
INSERT INTO "user" VALUES (16, 'Ave del Paraiso', NULL, 'es', 1338814284, NULL, 1, 1595874651.18445);
INSERT INTO "user" VALUES (17, 'Jorge Luis', NULL, 'es', 1195780347, '', 1, 1595874651.56413);
INSERT INTO "user" VALUES (18, 'Vivian', NULL, NULL, 1331362429, NULL, 1, 1595874651.97974);
INSERT INTO "user" VALUES (19, 'G. Viera', 'gvieralopez', NULL, 677816318, NULL, 1, 1595875294.04446);
INSERT INTO "user" VALUES (20, 'Zenia', NULL, NULL, 1065665053, NULL, 1, 1595877074.55621);
INSERT INTO "user" VALUES (21, 'Oscar', 'RamboXp', 'es', 718520667, ' ', 0, 1595880523.56326);
INSERT INTO "user" VALUES (22, 'Lazaro', NULL, NULL, 1337257510, '', 1, 1595882960.96919);
INSERT INTO "user" VALUES (23, 'Lietel', NULL, 'es', 1385779644, NULL, 1, 1595892302.44897);
INSERT INTO "user" VALUES (24, 'Annia Maria', NULL, 'es', 1308968588, '', 1, 1595899942.28838);
INSERT INTO "user" VALUES (25, 'ˣˣˣ 𝐕𝐢𝐜𝐭𝐨𝐫 ❄️🔥', 'vitty40', 'en', 768450449, 53158917, 1, 1595910951.04155);
INSERT INTO "user" VALUES (26, 'Andy Scott', 'andyscott93', 'en', 689663528, NULL, 1, 1595917317.25247);

PRAGMA foreign_keys = true;





PRAGMA foreign_keys = false;


-- ----------------------------
-- Records of settings4user
-- ----------------------------
INSERT INTO "settings4user" VALUES (1, 'Shampoo', 1189539262);
INSERT INTO "settings4user" VALUES (2, 'Pasta Dental', 1189539262);
INSERT INTO "settings4user" VALUES (3, 'Detergente', 1189539262);
INSERT INTO "settings4user" VALUES (4, 'Papel Sanitario', 1189539262);
INSERT INTO "settings4user" VALUES (5, 'Acondicionador', 1189539262);
INSERT INTO "settings4user" VALUES (6, 'Pollo Pechuga', 1189539262);
INSERT INTO "settings4user" VALUES (8, 'Artemisa', 712291624);
INSERT INTO "settings4user" VALUES (9, 'Pollo Muslo', 798027302);
INSERT INTO "settings4user" VALUES (11, 'Carlos 3ro', 1187586274);
INSERT INTO "settings4user" VALUES (12, 'Cuatro Caminos', 1187586274);
INSERT INTO "settings4user" VALUES (13, '5ta y 42', 1187586274);
INSERT INTO "settings4user" VALUES (14, 'Tipica de Boyeros', 1187586274);
INSERT INTO "settings4user" VALUES (15, 'Villa Diana', 1187586274);
INSERT INTO "settings4user" VALUES (16, 'El Pedregal', 1187586274);
INSERT INTO "settings4user" VALUES (17, 'Pollo Muslo', 1187586274);
INSERT INTO "settings4user" VALUES (18, 'Pollo Pechuga', 1187586274);
INSERT INTO "settings4user" VALUES (19, 'Detergente', 1187586274);
INSERT INTO "settings4user" VALUES (20, 'Pasta Dental', 1187586274);
INSERT INTO "settings4user" VALUES (21, 'Papel Sanitario', 1187586274);
INSERT INTO "settings4user" VALUES (22, 'Atun', 1187586274);
INSERT INTO "settings4user" VALUES (23, 'Sardina', 1187586274);
INSERT INTO "settings4user" VALUES (24, 'Shampoo', 1187586274);
INSERT INTO "settings4user" VALUES (25, 'Acondicionador', 1187586274);
INSERT INTO "settings4user" VALUES (26, 'Aceite', 1187586274);
INSERT INTO "settings4user" VALUES (27, 'Picadillo', 1187586274);
INSERT INTO "settings4user" VALUES (28, '5ta y 42', 954732565);
INSERT INTO "settings4user" VALUES (29, '5ta y 42', 916277649);
INSERT INTO "settings4user" VALUES (30, '5ta y 42', 1348442958);
INSERT INTO "settings4user" VALUES (31, 'Carlos 3ro', 1348442958);
INSERT INTO "settings4user" VALUES (32, 'Cuatro Caminos', 1348442958);
INSERT INTO "settings4user" VALUES (33, 'Tipica de Boyeros', 1348442958);
INSERT INTO "settings4user" VALUES (34, 'Villa Diana', 1348442958);
INSERT INTO "settings4user" VALUES (35, 'El Pedregal', 1348442958);
INSERT INTO "settings4user" VALUES (36, 'Pollo Muslo', 1348442958);
INSERT INTO "settings4user" VALUES (37, 'Pasta Dental', 1348442958);
INSERT INTO "settings4user" VALUES (38, 'Pollo Pechuga', 1348442958);
INSERT INTO "settings4user" VALUES (39, 'Detergente', 1348442958);
INSERT INTO "settings4user" VALUES (40, 'Papel Sanitario', 1348442958);
INSERT INTO "settings4user" VALUES (41, 'Atun', 1348442958);
INSERT INTO "settings4user" VALUES (42, 'Sardina', 1348442958);
INSERT INTO "settings4user" VALUES (43, 'Shampoo', 1348442958);
INSERT INTO "settings4user" VALUES (44, 'Acondicionador', 1348442958);
INSERT INTO "settings4user" VALUES (45, 'Aceite', 1348442958);
INSERT INTO "settings4user" VALUES (46, 'Picadillo', 1348442958);
INSERT INTO "settings4user" VALUES (47, 'El Pedregal', 759128099);
INSERT INTO "settings4user" VALUES (49, 'Shampoo', 1232502123);
INSERT INTO "settings4user" VALUES (50, 'Carlos 3ro', 1232502123);
INSERT INTO "settings4user" VALUES (51, 'El Pedregal', 798027302);
INSERT INTO "settings4user" VALUES (52, 'El Pedregal', 954732565);
INSERT INTO "settings4user" VALUES (53, '5ta y 42', 759128099);
INSERT INTO "settings4user" VALUES (54, 'Pollo Pechuga', 954732565);
INSERT INTO "settings4user" VALUES (55, 'Carlos 3ro', 718520667);
INSERT INTO "settings4user" VALUES (56, '5ta y 42', 718520667);
INSERT INTO "settings4user" VALUES (57, 'Villa Diana', 718520667);
INSERT INTO "settings4user" VALUES (58, 'Cuatro Caminos', 718520667);
INSERT INTO "settings4user" VALUES (59, 'Pollo Muslo', 718520667);
INSERT INTO "settings4user" VALUES (60, 'Pollo Pechuga', 718520667);
INSERT INTO "settings4user" VALUES (61, 'Pasta Dental', 718520667);
INSERT INTO "settings4user" VALUES (62, 'Picadillo', 718520667);
INSERT INTO "settings4user" VALUES (63, 'Carlos 3ro', 1337257510);
INSERT INTO "settings4user" VALUES (64, '5ta y 42', 1337257510);
INSERT INTO "settings4user" VALUES (65, 'Cuatro Caminos', 1337257510);
INSERT INTO "settings4user" VALUES (66, 'Villa Diana', 1337257510);
INSERT INTO "settings4user" VALUES (67, 'El Pedregal', 1337257510);
INSERT INTO "settings4user" VALUES (68, 'Tipica de Boyeros', 1337257510);
INSERT INTO "settings4user" VALUES (69, 'Pollo Pechuga', 1337257510);
INSERT INTO "settings4user" VALUES (70, 'Pollo Muslo', 1337257510);
INSERT INTO "settings4user" VALUES (71, 'Detergente', 1337257510);
INSERT INTO "settings4user" VALUES (72, 'Pasta Dental', 1337257510);
INSERT INTO "settings4user" VALUES (74, 'Papel Sanitario', 1337257510);
INSERT INTO "settings4user" VALUES (75, 'Sardina', 1337257510);
INSERT INTO "settings4user" VALUES (76, 'Shampoo', 1337257510);
INSERT INTO "settings4user" VALUES (77, 'Aceite', 1337257510);
INSERT INTO "settings4user" VALUES (78, 'Acondicionador', 1337257510);
INSERT INTO "settings4user" VALUES (79, 'Picadillo', 1337257510);
INSERT INTO "settings4user" VALUES (80, 'Atun', 1337257510);
INSERT INTO "settings4user" VALUES (81, '5ta y 42', 1385779644);
INSERT INTO "settings4user" VALUES (82, 'Cuatro Caminos', 1385779644);
INSERT INTO "settings4user" VALUES (83, 'Carlos 3ro', 1385779644);
INSERT INTO "settings4user" VALUES (84, 'Tipica de Boyeros', 1385779644);
INSERT INTO "settings4user" VALUES (85, 'Villa Diana', 1385779644);
INSERT INTO "settings4user" VALUES (86, 'El Pedregal', 1385779644);
INSERT INTO "settings4user" VALUES (89, 'Pollo Muslo', 1308968588);
INSERT INTO "settings4user" VALUES (90, 'Pollo Pechuga', 1308968588);
INSERT INTO "settings4user" VALUES (91, 'Shampoo', 1308968588);
INSERT INTO "settings4user" VALUES (92, 'Acondicionador', 1308968588);
INSERT INTO "settings4user" VALUES (93, 'Aceite', 1308968588);

PRAGMA foreign_keys = true;
