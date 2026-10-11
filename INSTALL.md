# Cài đặt GitHub profile — bản xanh dương dịu, chữ trắng

## 1. Slogan

Bản diễn đạt tiếng Anh tự nhiên: **Be yourself. Conquer yourself. Push beyond your limits.**

Bản này diễn đạt theo ý sống là chính mình, vượt qua bản thân và mở rộng giới hạn. Cụm “TIỆM CỦA GIỚI HẠN” trong câu gốc chưa rõ nghĩa nên đây là bản diễn đạt, không phải bản dịch sát từng từ.

Banner đã bỏ final-year, HUCE, Nghệ An và Hà Nội. README giữ chuyên ngành Khoa học máy tính và ngày sinh, cùng hai email được cung cấp.

## 2. Đưa file lên repository profile

Repository phải Public và có tên đúng bằng username GitHub của bạn.
Đưa README.md, assets/, scripts/ và .github/workflows/contributions.yml vào thư mục gốc repository.
Không đưa tất cả vào một thư mục cha profile-kit.

Cách dùng Git trên máy tính:
1. Clone repository profile của bạn.
2. Chép các file trong bộ này vào repository vừa clone, gồm cả thư mục .github.
3. Tại terminal của repository chạy:

```bash
git add README.md assets scripts .github/workflows/contributions.yml
git commit -m "Update profile with light blue banner and contribution playground"
git push
```

Nếu dùng giao diện web: Upload README.md, assets và scripts; tạo file mới tên .github/workflows/contributions.yml bằng Add file → Create new file rồi dán nội dung workflow vào. Thư mục .github có thể bị ẩn khi chọn file trên máy.

## 3. Bật đóng góp private trên profile

Mở Your profile → ở phía trên bảng đóng góp chọn Contribution settings → bật Private contributions.
GitHub hiển thị số lượng hoạt động ẩn danh của repo private, không công khai tên hay nội dung repo.

## 4. Tạo token cho đồ thị và thống kê

1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic).
2. Generate new token (classic).
3. Đặt tên profile-contributions và chọn thời hạn phù hợp.
4. Chọn scope read:user cho dữ liệu profile. Bản này chỉ hỏi lịch đóng góp tổng hợp; không cần đọc mã nguồn repo.
5. Tạo token của CHÍNH tài khoản sở hữu repository profile.
6. Trong repository profile: Settings → Secrets and variables → Actions → New repository secret.
7. Name: PROFILE_TOKEN. Secret: token vừa tạo.

Chỉ lưu token vào Secret; không dán token vào README hoặc workflow.
Workflow dùng token cá nhân để truy vấn lịch đóng góp của đúng tài khoản, không âm thầm dùng token public nếu thiếu cấu hình.
Nếu GitHub báo thiếu quyền hoặc token hết hạn, kiểm tra và cập nhật Secret. Nếu tài khoản tổ chức hạn chế PAT, cần tuân theo cấu hình quyền của tổ chức.

## 5. Chạy workflow

Actions → Update contribution playground → Run workflow.
Khi thành công, workflow cập nhật ba file:
- assets/github-snake.svg
- assets/github-snake-dark.svg
- assets/contribution-stats.svg

Ảnh rắn tự chọn theme sáng/tối; màu chủ đạo là xanh dương. Thống kê gồm tổng đóng góp, số ngày hoạt động và chuỗi ngày hoạt động dài nhất trong lịch năm vừa qua.
Tự chạy hằng ngày lúc 07:17 giờ Việt Nam. Workflow tự nhận username từ chủ repository nên không cần điền username thủ công.
Nếu gặp lỗi git push 403, vào Settings → Actions → General → Workflow permissions để kiểm tra quyền ghi hoặc quy tắc bảo vệ nhánh. Không tắt bảo vệ nhánh; dùng nhánh/PR được phép nếu repository có quy định.

## 6. Phạm vi dữ liệu và trạng thái hiện tại

Bộ file đã có workflow nhưng CHƯA chạy trên tài khoản GitHub của bạn; các ảnh rắn/thống kê ban đầu chỉ là thông báo chờ cấu hình, không có số liệu giả.
Đây là hoạt ảnh mô phỏng Snake dựa trên bảng đóng góp, không phải trò chơi điều khiển trực tiếp trong README.
Lịch GitHub là đóng góp được GitHub ghi nhận, không phải tổng mọi commit trên mọi nhánh hoặc toàn bộ lịch sử. Nó có thể gồm commit, pull request, issue và review.
Nếu thiếu commit, kiểm tra email tác giả có liên kết với tài khoản GitHub và commit có nằm trên nhánh mặc định hoặc gh-pages theo quy tắc GitHub. Có thể cần chờ GitHub cập nhật bảng đóng góp.
Token và truy vấn chỉ dùng trong Actions; file xuất bản chỉ có số liệu tổng hợp và ảnh, không chứa tên repo hay nội dung commit private.

Banner chính là GIF: slogan gõ từng chữ, dòng trạng thái luân phiên Exploring AI - Building Backend và Curiosity. Code. Continuous learning., màn hình laptop chạy chữ, con trỏ nhấp nháy và điểm sáng chuyển động nhẹ. Không cần dịch vụ bên ngoài cho hiệu ứng banner. Rắn dùng workflow ở trên; badge dùng Shields.io. assets/profile-banner.png là ảnh nền tĩnh với tên, nhãn AI / Backend và laptop; GIF chứa slogan và các dòng chữ động đầy đủ. Không cần API key AI.

## Nguồn
- https://docs.github.com/en/account-and-profile/how-tos/contribution-settings/manage-visibility-settings-for-private-contributions-and-achievements
- https://github.com/Platane/snk
- https://github.com/DenverCoder1/readme-typing-svg
- https://docs.github.com/en/graphql/guides/forming-calls-with-graphql
