# Melon Chat Server API 接口文档

## 一、基本 Cookies

1. `uid`
   用户唯一标识

2. `passwordHash`
   用户密码的哈希

## 二、用户操作

1. `GET /api/user/getName/[uid]`
   获取用户名

2. `GET /api/user/getUid/[username]`
   获取 `uid`

3. `GET /api/user/search/[keyword]`
   搜索所有用户名带有 `[keyword]` 前缀的用户的 `uid`，`[keyword]` 大于两个字符

4. `GET /api/user/getInfo/[uid]`
   获取用户名、个性签名、首页 Markdown、头像 `iid`

5. `GET /api/user/checkLogin`
   检查登录，成功返回 `uid`

6. `POST /api/user/setLabel`
   修改用户个性签名

7. `POST /api/user/setHomepage`
   修改用户首页 Markdown

8. `POST /api/user/setImage`
   修改用户头像

## 三、聊天室

1. `GET /api/publicMsg/num`
   获取消息总数

2. `GET /api/publicMsg/get/from=[from]&to=[to]`
   获取 `mid` 在 `from` 至 `to` 之间的消息

3. `POST /api/publicMsg/send`
   发送消息

## 四、文件

1. `GET /api/file/list`
   获取用户上传的文件列表

2. `GET /api/file/get/[fid]`
   下载文件

3. `GET /api/file/delete/[fid]`
   删除文件

4. `POST /api/file/upload`
   上传文件，成功返回 `fid`

## 五、图片

1. `GET /api/image/list`
   获取用户上传的图片列表

2. `GET /api/image/[iid]`
   下载图片

3. `GET /api/image/delete/[iid]`
   删除图片

4. `POST /api/image/upload`
   上传图片，成功返回 `iid`

## 六、剪贴板

1. `GET /api/note/list`
   获取用户上传的剪贴板列表

2. `GET /api/note/[nid]`
   获取剪贴板内容

3. `GET /api/note/public`
   获取所有公开且可检索剪贴板列表

4. `GET /api/note/delete/[nid]`
   删除剪贴板

5. `GET /api/note/changePermission/nid=[nid]&per=[per]`
   修改剪贴板权限

6. `POST /api/note/upload`
   新建剪贴板

## 七、私信

1. `GET /api/chat/num/[uid]`
   获取与 `[uid]` 用户的私信数量

2. `GET /api/chat/get/uid=[uid]&from=[from]&to=[to]`
   获取与 `[uid]` 用户私信第 `[from]` 条到第 `[to]` 条的数据

3. `POST /api/chat/send/uid=[uid]`
   发送私信

## 八、系统管理

1. `POST /api/admin/sql/[sql]`
   执行 `sql`，仅 `root` 有权

2. `GET /api/admin/be/[uid]`
   以 `[uid]` 的身份登录，仅 `root` 有权

3. `POST /api/admin/setUserName/[uid]`
   修改用户名，`admin` 和 `root` 都有权

4. `GET /api/admin/fileList`
   查看所有文件，包括被删除的，`admin` 和 `root` 都有权

5. `GET /api/admin/imageList`
   查看所有图片，包括被删除的，`admin` 和 `root` 都有权

6. `GET /api/admin/noteList`
   查看所有剪贴板，包括被删除的和不公开的，`admin` 和 `root` 都有权

7. `GET /api/admin/file/[fid]`
   下载文件，包括被删除的，`admin` 和 `root` 都有权

8. `GET /api/admin/image/[iid]`
   下载图片，包括被删除的，`admin` 和 `root` 都有权

9. `GET /api/admin/note/[nid]`
   查看剪贴板，包括被删除的和不公开的，`admin` 和 `root` 都有权

7. `GET /api/admin/deleteFile/[fid]`
   删除文件，`admin` 和 `root` 都有权

8. `GET /api/admin/deleteImage/[iid]`
   删除图片，`admin` 和 `root` 都有权

9. `GET /api/admin/deleteNote/[nid]`
   删除剪贴板，`admin` 和 `root` 都有权

10. `GET /api/admin/givePermission/[uid]`
    提升权力为 `admin`，仅 `root` 都有权

11. `GET /api/admin/removePermission/[uid]`
    降低权力为 `user`，仅 `root` 都有权