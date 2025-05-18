8-PUZZLE AI GAME

TỔNG QUAN VỀ BÀI TẬP

Dự án này mô phỏng trò chơi 8-Puzzle, một bài toán nổi tiếng trong trí tuệ nhân tạo (AI), với giao diện trực quan để giải quyết bài toán tìm kiếm bằng các thuật toán tìm kiếm khác nhau. 

8-Puzzle là một trò chơi trí tuệ cổ điển gồm một bảng 3x3 với 8 ô số (1–8) và một ô trống. Mục tiêu của trò chơi là di chuyển các ô số (bằng cách trượt vào vị trí trống) sao cho sắp xếp được bảng từ trạng thái ban đầu bất kỳ về trạng thái đích (mục tiêu).

Trò chơi này được xem là một bài toán tìm kiếm không gian trạng thái, rất phổ biến trong lĩnh vực Trí tuệ nhân tạo (AI). Việc giải quyết 8-Puzzle đòi hỏi phải tìm được một chuỗi hành động (di chuyển các ô) ngắn nhất hoặc tối ưu nhất từ trạng thái ban đầu về trạng thái mục tiêu.

MỤC TIÊU

Các thuật toán AI được triển khai giúp giải quyết bài toán 8-Puzzle bằng nhiều cách tiếp cận khác nhau, mỗi thuật toán sẽ cho ra kết quả và thời gian thực thi khác nhau, mang lại cái nhìn trực quan về hiệu quả của từng phương pháp tìm kiếm giúp người học tập, nghiên cứu về các thuật toán tìm kiếm dễ dàng quan sát, so sánh và không bị nhàm chán khi học. Các thuật toán này bao gồm:

Thuật toán tìm kiếm không có thông tin (Uninformed Search): BFS, DFS, USC, IDDFS

Thuật toán tìm kiếm có thông tin (Informed Search): Greedy, A, IDA**

Thuật toán tìm kiếm cục bộ (Local Search): SHC, SAHC, Stochastic HC, Beam Search, Simulated Annealing, Genetic Algorithm

Thuật toán ràng buộc (CSPs): Backtracking, Forward Checking, Min-Conflicts

Thuật toán tìm kiếm trong môi trường phức tạp (Complex Environment): Sensorless, And-Or Search

Thuật toán học tăng cường (Reinforcement Learning): Q-Learning

Thông qua dự án này, người dùng có thể dễ dàng quan sát quá trình giải quyết bài toán 8-Puzzle qua giao diện đồ họa, với các thuật toán khác nhau hiển thị rõ ràng những bước đi và quá trình tìm kiếm trong không gian trạng thái.

Mục lục





















































 diện



1. Thuật toán tìm kiếm không có thông tin (Uninformed Search)

Thuật toán tìm kiếm không có thông tin là các thuật toán tìm kiếm mà không sử dụng bất kỳ thông tin bổ sung nào ngoài trạng thái ban đầu và các trạng thái liên quan. Các thuật toán này chỉ dựa vào việc mở rộng các trạng thái theo một thứ tự cụ thể mà không dựa vào đánh giá về chất lượng của các trạng thái đó. Do không có "thông tin thông minh", các thuật toán này có thể tốn kém về bộ nhớ và thời gian.

Ưu điểm:

Đơn giản và dễ hiểu, không yêu cầu thông tin bổ sung ngoài trạng thái ban đầu.

Tìm kiếm theo chiều rộng (BFS) đảm bảo tìm được giải pháp tối ưu nếu tồn tại.

Nhược điểm:

Tiêu tốn nhiều bộ nhớ và thời gian khi không gian trạng thái lớn.

Các thuật toán như DFS có thể không tìm được giải pháp nếu không có giới hạn độ sâu.

Không tối ưu trong những bài toán phức tạp, vì chúng không sử dụng thông tin bổ sung để hướng dẫn tìm kiếm.

Mô phòng trong trò chơi 8-puzzle:

Hiệu quả với hầu hết trạng thái, kể cả trạng thái khó.

Tuy nhiên:

DFS cần giới hạn độ sâu để tránh lặp vô hạn.

IDDFS kết hợp ưu điểm của DFS và BFS.

Dùng tốt cho trạng thái có độ sâu từ 15–20 bước.



































BFS (Tìm kiếm theo chiều rộng)

Thuật toán tìm kiếm theo chiều rộng (BFS) sẽ mở rộng các đỉnh của cây tìm kiếm từ gốc theo từng mức độ, kiểm tra tất cả các đỉnh cùng một mức trước khi chuyển sang mức tiếp theo.

Độ tối ưu: Tối ưu đối với các bài toán tìm kiếm vô hạn nếu không có thông tin.

Độ phức tạp: O(b^d), với b là độ rộng của cây và d là độ sâu của cây tìm kiếm.



DFS (Tìm kiếm theo chiều sâu)

DFS sẽ đi sâu vào một nhánh của cây tìm kiếm cho đến khi không thể mở rộng tiếp, rồi quay lại điểm phân nhánh và thử các nhánh khác.

Độ tối ưu: Không tối ưu trong trường hợp không có giới hạn độ sâu.

Độ phức tạp: O(b^d).



IDDFS (Tìm kiếm theo chiều sâu lặp lại)

Là sự kết hợp giữa DFS và BFS, IDDFS thực hiện DFS với các độ sâu giới hạn và tăng dần độ sâu cho đến khi tìm thấy giải pháp.

Độ tối ưu: Tốt nhất trong việc sử dụng bộ nhớ khi tìm kiếm trong không gian lớn.

Độ phức tạp: O(b^d), nhưng sử dụng bộ nhớ ít hơn so với BFS.



UCS (Tìm kiếm chi phí đồng nhất)

UCS tìm kiếm theo chi phí, mở rộng các đỉnh có chi phí thấp nhất trước.

Độ tối ưu: Tìm kiếm tối ưu trong các bài toán có chi phí không âm.

Độ phức tạp: O(b^d).



2. Thuật toán tìm kiếm có thông tin (Informed Search)

Thuật toán tìm kiếm có thông tin sử dụng thông tin bổ sung (như hàm đánh giá hoặc hàm heuristic) để hướng dẫn quá trình tìm kiếm. Thông tin này giúp thuật toán lựa chọn những trạng thái tiềm năng hơn để mở rộng, giúp cải thiện hiệu quả tìm kiếm và giảm thiểu chi phí tính toán. Đây là những thuật toán tìm kiếm hiệu quả hơn so với các thuật toán tìm kiếm không có thông tin, đặc biệt trong không gian trạng thái lớn.

Ưu điểm:

Tìm kiếm hiệu quả hơn nhờ sử dụng thông tin bổ sung (hàm đánh giá heuristic).

Các thuật toán như A* có thể tìm được giải pháp tối ưu trong không gian trạng thái có thông tin đầy đủ.

Nhược điểm:

Cần phải có một hàm đánh giá tốt, nếu không thuật toán có thể không tối ưu hoặc tốn kém tài nguyên.

Các thuật toán như A* hoặc Greedy có thể tốn thời gian và bộ nhớ khi không gian trạng thái rất lớn.

Mô phòng trong trò chơi 8-puzzle:

Hoạt động tốt trên trạng thái trung bình đến khó.

✅ A* đảm bảo tối ưu nếu heuristic là hợp lệ (admissible).

❗ Greedy có thể bị lệch hướng nếu heuristic không tốt.

✅ Nên áp dụng cho các trạng thái có độ dài từ 12–25 bước.















Greedy

Thuật toán Greedy đưa ra lựa chọn tốt nhất trong bước hiện tại mà không quan tâm đến tương lai, nhằm tối ưu hóa bước tiếp theo.

Độ tối ưu: Không tối ưu, có thể dẫn đến giải pháp không chính xác.

Độ phức tạp: O(b^d).



A* (A-star)

A* kết hợp giữa tìm kiếm theo chi phí và tìm kiếm theo độ gần với mục tiêu, sử dụng hàm đánh giá f(n) = g(n) + h(n) để lựa chọn đỉnh tiếp theo.

Độ tối ưu: Tìm kiếm tối ưu nếu hàm đánh giá h(n) không vượt quá chi phí thực tế.

Độ phức tạp: O(b^d).



IDA* (Iterative Deepening A*)

IDA* kết hợp giữa IDDFS và A*, thực hiện A* với độ sâu lặp lại để tiết kiệm bộ nhớ.

Độ tối ưu: Tối ưu khi cần tiết kiệm bộ nhớ.

Độ phức tạp: O(b^d).



3. Thuật toán tìm kiếm cục bộ (Local Search)

Thuật toán tìm kiếm cục bộ tìm kiếm trong không gian trạng thái chỉ xung quanh vị trí hiện tại mà không cần phải theo dõi toàn bộ không gian trạng thái. Điều này giúp tiết kiệm bộ nhớ, nhưng cũng có thể dẫn đến các vấn đề như mắc kẹt tại tối ưu cục bộ. Các thuật toán này thích hợp cho những bài toán có không gian trạng thái lớn, nhưng không đảm bảo sẽ tìm được giải pháp tối ưu toàn cục.

Ưu điểm:

Tiết kiệm bộ nhớ và tính toán vì chỉ tìm kiếm trong một phần không gian trạng thái.

Các thuật toán như Simulated Annealing có thể tránh được tối ưu cục bộ và tìm được tối ưu toàn cục trong một số trường hợp.

Nhược điểm:

Không đảm bảo tìm ra giải pháp tối ưu toàn cục.

Các thuật toán như SHC có thể bị kẹt ở một tối ưu cục bộ nếu không có chiến lược làm lạnh thích hợp (như Simulated Annealing).

Mô phòng trong trò chơi 8-puzzle:

✅ Chọn trạng thái có độ dài lời giải khoảng 10 bước để tránh:

Quá dễ → không thể hiện rõ thuật toán.

Quá khó → kẹt cục bộ hoặc không tìm ra lời giải.

⚠️ Nên giới hạn độ sâu từ 20–30 bước hoặc max\_steps cụ thể.









































SHC (Simple Hill Climbing)

SHC là một thuật toán tìm kiếm cục bộ đơn giản, trong đó tại mỗi bước, thuật toán chỉ chọn một trạng thái kề tốt hơn trạng thái hiện tại (nếu có) và chuyển đến đó. Thuật toán dừng khi không tìm được trạng thái nào tốt hơn.

Độ tối ưu: Không đảm bảo tìm được tối ưu toàn cục, dễ rơi vào bẫy tối ưu cục bộ.

Độ phức tạp: O(b^d).



SAHC (Steepest-Ascent Hill Climbing)

SAHC là biến thể của SHC, trong đó tại mỗi bước, thuật toán đánh giá tất cả các trạng thái kề và chọn trạng thái có giá trị đánh giá tốt nhất (dốc nhất) để di chuyển.

Độ tối ưu: Vẫn không đảm bảo tìm được tối ưu toàn cục vì vẫn có thể mắc kẹt tại cực trị cục bộ hoặc cao nguyên.

Độ phức tạp: O(b^d).



Stochastic HC (Stochastic Hill Climbing)

Là một phiên bản ngẫu nhiên của SHC, nơi các bước đi không nhất thiết phải theo chiều dốc.

Độ tối ưu: Không tối ưu.

Độ phức tạp: O(b^d).

 

Beam Search

Thuật toán tìm kiếm cục bộ này chỉ mở rộng một số đỉnh giới hạn tại mỗi mức.

Độ tối ưu: Có thể không tối ưu vì giới hạn số đỉnh mở rộng.

Độ phức tạp: O(b^k), với k là số lượng beam.



Simulated Annealing

Thuật toán làm lạnh mô phỏng mô phỏng quá trình vật lý của làm lạnh từ từ để tránh tối ưu cục bộ.

Độ tối ưu: Tìm tối ưu toàn cục trong không gian trạng thái lớn.

Độ phức tạp: O(b^d).



Genetic Algorithm

Thuật toán di truyền mô phỏng quá trình chọn lọc tự nhiên để tìm ra giải pháp tối ưu.

Độ tối ưu: Tìm giải pháp gần tối ưu.

Độ phức tạp: O(b^d).

 

4. Thuật toán ràng buộc (CSPs - Constraint Satisfaction Problems)

Thuật toán ràng buộc được sử dụng để giải quyết các bài toán trong đó các biến phải thỏa mãn một tập hợp các ràng buộc. Những bài toán này thường gặp trong các lĩnh vực như phân công, lịch trình, và tổ chức. Các thuật toán ràng buộc không chỉ tìm kiếm một giải pháp mà còn phải kiểm tra tính hợp lệ của các lựa chọn trong suốt quá trình tìm kiếm.

Ưu điểm:

Tốt cho các bài toán có ràng buộc rõ ràng, như phân bổ tài nguyên hoặc lập kế hoạch.

Các thuật toán như Min-Conflicts có thể tìm được giải pháp tốt với các bài toán ràng buộc phức tạp.

Nhược điểm:

Các thuật toán này không phải lúc nào cũng có thể áp dụng cho tất cả loại bài toán tìm kiếm.

Tốn thời gian và tài nguyên khi số lượng ràng buộc và biến tăng lên.

Mô phòng trong trò chơi 8-puzzle:

Hữu ích khi kiểm soát biến số rõ ràng.

Không phải luôn phù hợp với các bài toán trạng thái như 8-Puzzle.

✅ Áp dụng trạng thái vừa phải (8–12 bước) để thấy rõ hiệu quả loại trừ.
















Backtracking

Thuật toán quay lui, thử các lựa chọn khác nhau và quay lại khi gặp mâu thuẫn.

Độ tối ưu: Tìm kiếm giải pháp tối ưu.

Độ phức tạp: O(b^d), có thể giảm với việc cắt tỉa (pruning).



Forward Checking

Kiểm tra các ràng buộc phía trước để loại bỏ các lựa chọn không khả thi.

Độ tối ưu: Tối ưu hơn backtracking khi kiểm tra trước.

Độ phức tạp: O(b^d), nhưng có thể giảm đáng kể.



Min-Conflicts

Thuật toán tìm giải pháp tối ưu bằng cách giảm số lượng mâu thuẫn tại mỗi bước.

Độ tối ưu: Có thể tìm kiếm giải pháp tối ưu hoặc gần tối ưu.

Độ phức tạp: O(b^d), tùy vào cách cắt tỉa và số mâu thuẫn.



5. Thuật toán tìm kiếm trong môi trường phức tạp (Complex Environment)

Thuật toán tìm kiếm trong môi trường phức tạp được áp dụng trong các bài toán mà môi trường không hoàn toàn rõ ràng hoặc không đầy đủ thông tin. Những thuật toán này có thể làm việc trong các tình huống không chắc chắn, nơi các thông tin về trạng thái không có sẵn hoặc chỉ có thể đoán được, ví dụ như trong các bài toán tìm kiếm sensorless hoặc tìm kiếm And-Or.

Ưu điểm:

Phù hợp với các bài toán có sự không chắc chắn hoặc không đầy đủ thông tin.

Các thuật toán như Sensorless hoặc And-Or Search có thể giải quyết các vấn đề trong môi trường phức tạp mà các thuật toán truyền thống gặp khó khăn.

Nhược điểm:

Cần có môi trường và sự mô phỏng phức tạp, điều này có thể tăng độ khó và chi phí tính toán.

Các thuật toán này có thể kém hiệu quả nếu môi trường không được mô tả rõ ràng hoặc thiếu dữ liệu.

Mô phòng trong trò chơi 8-puzzle: Chủ yếu để minh họa ý tưởng, không thực tế trong 8-Puzzle cơ bản.

❗Chưa phát huy tối đa sức mạnh trong trò chơi này.

Sensorless

Thuật toán tìm kiếm làm việc trong môi trường không có thông tin về trạng thái.

Độ tối ưu: Không tối ưu, vì thiếu thông tin từ môi trường.

Độ phức tạp: O(b^d).



And-Or Search

Tìm kiếm trong môi trường phân nhánh, tìm kiếm các chuỗi hành động phù hợp với các ràng buộc.

Độ tối ưu: Tìm kiếm giải pháp tối ưu cho các bài toán phân nhánh.

Độ phức tạp: O(b^d).



6. Thuật toán học tăng cường (Reinforcement Learning)

Thuật toán học tăng cường là một phương pháp học máy trong đó một tác nhân học cách hành động tối ưu trong một môi trường thông qua việc nhận thưởng hoặc phạt sau mỗi hành động. Thay vì tìm kiếm giải pháp từ trước, tác nhân học qua kinh nghiệm và cải thiện hiệu suất qua thời gian. Điều này giúp giải quyết các bài toán phức tạp và động, nơi môi trường có thể thay đổi theo từng bước.

Ưu điểm:

AI có thể học hỏi từ môi trường và tối ưu hóa hành vi của mình theo thời gian.

Phù hợp với các bài toán động và không chắc chắn, nơi môi trường thay đổi theo từng hành động.

Nhược điểm:

Cần một lượng lớn dữ liệu và thời gian để huấn luyện.

Các thuật toán như Q-Learning có thể không hiệu quả trong không gian trạng thái lớn hoặc phức tạp mà không có chiến lược học thích hợp.

Mô phòng trong trò chơi 8-puzzle:

Đặt điều kiện thưởng, phạt để tạo động lực cho AI học tăng cường. Và ngày càng tìm ra các giải pháp tối ưu hơn.

+100 điểm nếu đạt goal

+1 điểm với mỗi ô đúng vị trí

-5 điểm nếu trạng thái không tiến bộ (số ô đúng không tăng)

-20 điểm nếu lặp trạng thái

Trạng thái ban đầu nên đơn giản, sau đó nâng dần độ khó.

✅ Thích hợp để demo khả năng học từ môi trường động.







Q-Learning

Thuật toán học tăng cường, học từ kinh nghiệm bằng cách tối ưu hóa giá trị Q cho các trạng thái và hành động.

Độ tối ưu: Tìm kiếm giải pháp tối ưu với đủ số lần học.

Độ phức tạp: O(b^d), phụ thuộc vào việc cập nhật Q-table.



GIAO DIỆN



Giao diện trò chơi được chia thành ba khu vực chính theo chiều ngang: khu vực chọn thuật toán tìm kiếm, giao diện trò chơi 8-puzzle, và khu vực hiển thị biểu đồ trực quan hiệu quả thuật toán.

Khu vực thuật toán bao gồm 6 nhóm thuật toán, mỗi nhóm có một combobox chứa danh sách các thuật toán tương ứng, giúp người dùng dễ dàng lựa chọn và đảm bảo tính chính xác khi xác định thuật toán sẽ thực hiện. Khi người dùng chọn một thuật toán trong bất kỳ nhóm nào, các nhóm còn lại sẽ tự động được đặt lại về trạng thái rỗng để tránh xung đột tín hiệu. Việc lựa chọn thuật toán đồng nghĩa với việc hệ thống bắt đầu khởi chạy quá trình tìm kiếm lời giải bằng thuật toán đó.

Khu vực trung tâm là nơi hiển thị chính của trò chơi 8-puzzle với 8 ô số được sắp xếp theo trạng thái khởi tạo ban đầu. Đây là không gian chính để quan sát quá trình thuật toán giải quyết bài toán. Các ô sẽ di chuyển bằng cách hoán đổi vị trí với ô trống theo đường đi được xác định bởi thuật toán. Bên cạnh khu vực lưới là một nhóm các nút điều khiển cho phép người dùng nhập trạng thái đầu vào theo nhiều cách: nhập từ bàn phím (nut INPUT), sinh ngẫu nhiên (nút RANDOM) hoặc chọn trạng thái đặc biệt (nút SPECIAL) có độ phức tạp từ 10–20 bước để kiểm tra năng lực của các thuật toán phức tạp. Ngoài ra, còn có các nút RESET để quay lại trạng thái khởi tạo, nut CHART để vẽ biểu đồ sau mỗi lần giải xong, thanh tiến tình progressBar để hiển thị phần trăm thực hiện thuật toán và các label bên dưới dùng để hiển thị thông tin như tên thuật toán, tiến độ giải, đường đi, thời gian và số bước thực hiện. Người dùng cũng có thể tạm dừng hoặc tiếp tục quá trình giải bằng các nút điều khiển tương ứng, cho phép quan sát chi tiết trạng thái hiện tại của trò chơi.

Ngay bên dưới giao diện trò chơi là ba trạng thái mẫu được sử dụng để mô phỏng và đánh giá hiệu quả hoạt động của các nhóm thuật toán khác nhau.

Khu vực biểu đồ đóng vai trò không kém phần quan trọng. Tại đây, hệ thống hiển thị biểu đồ cột để so sánh hiệu quả của các thuật toán trong cùng một nhóm, dựa trên thời gian tìm kiếm lời giải và số bước thực hiện. Biểu đồ này cung cấp cái nhìn trực quan giúp người dùng dễ dàng đánh giá và so sánh mức độ hiệu quả giữa các thuật toán. Hiện tại, hệ thống cho phép vẽ biểu đồ cho bất kỳ trạng thái khởi đầu nào được chọn, tuy nhiên, chưa bắt buộc các thuật toán cùng nhóm phải có chung trạng thái xuất phát. Để đảm bảo việc so sánh chính xác hơn, người dùng được khuyến khích chọn cùng một trạng thái khởi đầu (có thể chọn trạng thái mẫu từ ô start\_state) cho tất cả các thuật toán trong một nhóm.

KẾT LUẬN

Dự án 8-Puzzle AI Game này không chỉ giúp người chơi trải nghiệm trực quan quá trình giải quyết bài toán 8-Puzzle mà còn là một ví dụ tuyệt vời về cách các thuật toán AI có thể áp dụng trong việc giải quyết các bài toán tìm kiếm phức tạp. Qua việc so sánh các thuật toán tìm kiếm không có thông tin, tìm kiếm có thông tin và các thuật toán tìm kiếm cục bộ, người dùng có thể nhận thấy rõ sự khác biệt về hiệu quả và thời gian thực thi của từng thuật toán. Các thuật toán học tăng cường như Q-Learning cũng cho thấy khả năng học hỏi và cải thiện hiệu suất trong môi trường phức tạp.

Chắc chắn rằng việc sử dụng giao diện đồ họa trong dự án này không chỉ mang lại một trải nghiệm thú vị mà còn là một công cụ hữu ích để nghiên cứu và học hỏi về AI. Qua mỗi lần thử nghiệm với các thuật toán khác nhau, người dùng có thể hiểu rõ hơn về cách các thuật toán hoạt động và tối ưu hóa các quá trình tìm kiếm trong các không gian trạng thái lớn.

Dự án này sẽ là bước đầu tiên trong việc xây dựng các ứng dụng AI phức tạp hơn và mang lại cái nhìn sâu sắc hơn về cách AI có thể được ứng dụng trong thực tế.



