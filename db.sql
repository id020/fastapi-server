/*
 Navicat Premium Dump SQL

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80046 (8.0.46)
 Source Host           : localhost:3306
 Source Schema         : lab_agent

 Target Server Type    : MySQL
 Target Server Version : 80046 (8.0.46)
 File Encoding         : 65001

 Date: 24/10/2026 10:43:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for sys_departments
-- ----------------------------
DROP TABLE IF EXISTS `sys_departments`;
CREATE TABLE `sys_departments` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '部门主键，自增编号',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '部门名称，不允许重复',
  `parent_id` int DEFAULT NULL COMMENT '上级部门ID；NULL表示顶级部门，关联本表id',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '部门说明',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `parent_id` (`parent_id`),
  KEY `ix_departments_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='部门组织表，使用parent_id构建树形部门结构';

-- ----------------------------
-- Records of sys_departments
-- ----------------------------
BEGIN;
INSERT INTO `sys_departments` (`id`, `name`, `parent_id`, `description`) VALUES (1, '总部', NULL, '演示组织根部门');
INSERT INTO `sys_departments` (`id`, `name`, `parent_id`, `description`) VALUES (2, '研发部', 1, '');
INSERT INTO `sys_departments` (`id`, `name`, `parent_id`, `description`) VALUES (3, '销售部', 1, '');
COMMIT;

-- ----------------------------
-- Table structure for sys_menus
-- ----------------------------
DROP TABLE IF EXISTS `sys_menus`;
CREATE TABLE `sys_menus` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '菜单或权限项主键，自增编号',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单或权限项名称',
  `permission` varchar(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '权限标识，供后端权限校验使用，必须唯一',
  `menu_type` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '类型：menu表示页面菜单，button表示按钮权限',
  `path` varchar(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '前端路由路径；按钮权限通常为空',
  `component` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '前端页面组件名称；按钮权限通常为空',
  `parent_id` int DEFAULT NULL COMMENT '父级菜单ID；NULL表示顶级菜单，关联本表id',
  `sort_order` int NOT NULL COMMENT '排序值，数值越小通常越靠前',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_menus_permission` (`permission`),
  KEY `parent_id` (`parent_id`),
  KEY `ix_menus_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='菜单与按钮权限表，permission字段存储权限标识';

-- ----------------------------
-- Records of sys_menus
-- ----------------------------
BEGIN;
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (1, '工作台', 'dashboard:view', 'menu', '/dashboard', 'Dashboard', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (2, '用户管理', 'users:view', 'menu', '/users', 'Users', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (3, '用户管理-编辑', 'users:write', 'button', '', '', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (4, '角色管理', 'roles:view', 'menu', '/roles', 'Roles', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (5, '角色管理-编辑', 'roles:write', 'button', '', '', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (6, '部门管理', 'departments:view', 'menu', '/departments', 'Departments', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (7, '部门管理-编辑', 'departments:write', 'button', '', '', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (8, '菜单管理', 'menus:view', 'menu', '/menus', 'Menus', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (9, '菜单管理-编辑', 'menus:write', 'button', '', '', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (10, '示例数据', 'records:view', 'menu', '/records', 'Records', NULL, 0);
INSERT INTO `sys_menus` (`id`, `name`, `permission`, `menu_type`, `path`, `component`, `parent_id`, `sort_order`) VALUES (11, '示例数据-编辑', 'records:write', 'button', '', '', NULL, 0);
COMMIT;

-- ----------------------------
-- Table structure for sys_role_departments
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_departments`;
CREATE TABLE `sys_role_departments` (
  `role_id` int NOT NULL COMMENT '角色ID，关联roles.id',
  `department_id` int NOT NULL COMMENT '部门ID，关联departments.id',
  PRIMARY KEY (`role_id`,`department_id`),
  KEY `department_id` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='角色与部门关联表，用于配置角色可访问的部门范围';

-- ----------------------------
-- Records of sys_role_departments
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for sys_role_menus
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menus`;
CREATE TABLE `sys_role_menus` (
  `role_id` int NOT NULL COMMENT '角色ID，关联roles.id',
  `menu_id` int NOT NULL COMMENT '菜单或权限项ID，关联menus.id',
  PRIMARY KEY (`role_id`,`menu_id`),
  KEY `menu_id` (`menu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='角色与菜单权限关联表，用于分配页面和按钮权限';

-- ----------------------------
-- Records of sys_role_menus
-- ----------------------------
BEGIN;
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 1);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (2, 1);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 2);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 3);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 4);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 5);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 6);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 7);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 8);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 9);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 10);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (2, 10);
INSERT INTO `sys_role_menus` (`role_id`, `menu_id`) VALUES (1, 11);
COMMIT;

-- ----------------------------
-- Table structure for sys_roles
-- ----------------------------
DROP TABLE IF EXISTS `sys_roles`;
CREATE TABLE `sys_roles` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '角色主键，自增编号',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色名称，不允许重复',
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色编码，供程序识别，必须唯一',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色说明',
  `data_scope` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据范围标识，例如all表示全部数据，department_tree表示本部门及下级部门数据',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `ix_roles_code` (`code`),
  KEY `ix_roles_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='角色定义表，包含角色编码、说明及数据范围';

-- ----------------------------
-- Records of sys_roles
-- ----------------------------
BEGIN;
INSERT INTO `sys_roles` (`id`, `name`, `code`, `description`, `data_scope`) VALUES (1, '系统管理员', 'admin', '拥有全部管理权限', 'all');
INSERT INTO `sys_roles` (`id`, `name`, `code`, `description`, `data_scope`) VALUES (2, '演示操作员', 'demo_operator', '仅查看示例数据', 'department_tree');
COMMIT;

-- ----------------------------
-- Table structure for sys_user_roles
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_roles`;
CREATE TABLE `sys_user_roles` (
  `user_id` int NOT NULL COMMENT '用户ID，关联users.id',
  `role_id` int NOT NULL COMMENT '角色ID，关联roles.id',
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户与角色关联表，支持用户关联多个角色';

-- ----------------------------
-- Records of sys_user_roles
-- ----------------------------
BEGIN;
INSERT INTO `sys_user_roles` (`user_id`, `role_id`) VALUES (1, 1);
INSERT INTO `sys_user_roles` (`user_id`, `role_id`) VALUES (2, 2);
INSERT INTO `sys_user_roles` (`user_id`, `role_id`) VALUES (3, 2);
COMMIT;

-- ----------------------------
-- Table structure for sys_users
-- ----------------------------
DROP TABLE IF EXISTS `sys_users`;
CREATE TABLE `sys_users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户主键，自增编号',
  `username` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '登录用户名，必须唯一',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '密码哈希值；保存加密哈希，不应保存明文密码',
  `nickname` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户显示姓名',
  `avatar` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '头像',
  `status` tinyint(1) NOT NULL COMMENT '账号是否启用：1启用，0停用',
  `department_id` int NOT NULL COMMENT '所属部门ID，关联departments.id；允许为空',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `department_id` (`department_id`),
  KEY `ix_users_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户账号表，包含登录信息、启用状态及所属部门';

-- ----------------------------
-- Records of sys_users
-- ----------------------------
BEGIN;
INSERT INTO `sys_users` (`id`, `username`, `password`, `nickname`, `avatar`, `status`, `department_id`, `create_time`, `update_time`) VALUES (1, 'admin', '$2b$12$yb4Tkeb7kcYLWdcueDr5sunwz9FrOpK70Dg9YzOKY0ptovIFlfSDi', '系统管理员', '', 1, 1, '2026-10-22 11:07:09', '2026-10-22 11:07:14');
INSERT INTO `sys_users` (`id`, `username`, `password`, `nickname`, `avatar`, `status`, `department_id`, `create_time`, `update_time`) VALUES (2, 'operator', '$2b$12$yb4Tkeb7kcYLWdcueDr5sunwz9FrOpK70Dg9YzOKY0ptovIFlfSDi', '演示操作员', '', 0, 2, '2026-10-22 11:07:12', '2026-10-22 11:07:17');
INSERT INTO `sys_users` (`id`, `username`, `password`, `nickname`, `avatar`, `status`, `department_id`, `create_time`, `update_time`) VALUES (3, 'aaa', '$2b$12$KpKyBVLBN.rBVyJ9V1xcOuj6sVdhiN1hSMYmk0sxocXBZuJWZF4aK', 'bbb', 'https://www.gravatar.com/avatar/default?d=identicon', 0, 2, '2026-10-23 13:15:00', '2026-10-23 13:40:19');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
