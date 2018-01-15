from flask import Blueprint
import app.workbench.controllers as ctrl

workbench = Blueprint('workbench', __name__)


# 문서 문장 목록 조회, 번역편집툴에서 열기
workbench.add_url_rule('/docs/<int:did>', view_func=ctrl.get_doc, methods=['GET'])

# 작업내용 CSV파일로 다운로드
workbench.add_url_rule('/docs/<int:did>/output', view_func=ctrl.output_doc_to_file, methods=['POST'])


# 번역문 저장
workbench.add_url_rule('/docs/sentences/<int:sid>/trans', view_func=ctrl.save_trans_sentence, methods=['PUT'])

# 번역문 상태 수정
workbench.add_url_rule('/docs/sentences/<int:sid>/status/<int:status>', view_func=ctrl.save_sentence_status, methods=['PUT'])


# 번역문 댓글 조회
workbench.add_url_rule('/docs/sentences/<int:sid>/comments', view_func=ctrl.get_trans_comments, methods=['GET'])

# 번역문 댓글 추가
workbench.add_url_rule('/docs/sentences/<int:sid>/comments', view_func=ctrl.make_trans_comment, methods=['POST'])

# 번역문 댓글 삭제
workbench.add_url_rule('/docs/sentences/comments/<int:cid>', view_func=ctrl.delete_trans_comment, methods=['DELETE'])
