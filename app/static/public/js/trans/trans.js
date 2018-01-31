var interval_sec = 600; // 600초 -> 10분
var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project'),
        doc_id = getUrlParameter('doc_id'),
        origin_lang,
        trans_lang,
        current_reply_obj,
        page = 1,
        rows = 20000;
    this.preInits = function () {
        // body 흐리게
        local.mask();

        // 원문 로딩
        var jqxhr = $.get("/api/v1/toolkit/workbench/docs/" + doc_id, function (data) {
                console.log('[/api/v1/toolkit/workbench/docs/' + doc_id + ' 9987] : ');
                console.log(data);
                if (data.results != null && data.results != undefined && data.results.length > 0) {
                    origin_lang = data.results[0].origin_lang;
                    trans_lang = data.results[0].trans_lang;
                    var html = '';
                    $(data.results).each(function (idx, res) {
                        html += '<tr>';
                        html += '    <td>' + res.sentence_id + '</td>';
                        html += '    <td>' + res.origin_text + '</td>';

                        if(IsValidStr(res.trans_text)){
                            html += '    <td><textarea rows=1>' + res.trans_text + '</textarea></td>';
                        }else{
                            html += '    <td><textarea rows=1 placeholder="해석을 지우고 포커스를 옮기면 현재 행이 리셋됩니다."></textarea></td>';
                        }

                        html += '    <td>';
                        if (res.trans_status == '0') {
                            html += '    <i class="fa fa-times" aria-hidden="true" style="color:gray; cursor:pointer;"></i>';
                            html += '    <i class="fa fa-check" aria-hidden="true" style="color:orange; cursor:pointer; display:none;"></i>';
                        } else {
                            html += '    <i class="fa fa-times" aria-hidden="true" style="color:gray; cursor:pointer; display:none;"></i>';
                            html += '    <i class="fa fa-check" aria-hidden="true" style="color:orange; cursor:pointer;"></i>';
                        }
                        html += '    </td>';
                        if (res.trans_type == 'TM') {
                            html += '<td class="tmColor" title="문장저장소">TM</td>';
                        } else if (res.trans_type == 'MT') {
                            html += '<td class="mtColor" title="실시간번역">MT</td>';
                        } else if (res.trans_type == 'T') {
                            html += '<td class="tColor" title="자체번역">T</td>';
                        } else {
                            html += '<td></td>';
                        }
                        if (res.comment_cnt > 0) html += '    <td><i class="fa fa-comment" aria-hidden="true" style="color:orange; cursor:pointer;"></i></td>';
                        else html += '    <td><i class="fa fa-comment" aria-hidden="true" style="color:gray; cursor:pointer;"></i></td>';
                        html += '</tr>';
                    });
                    $('#mainTbl tbody tr').after(html);
                }
            })
            .done(function () {})
            .fail(function () {
                console.log("error : 5565");
            })
            .always(function () {});
        jqxhr.always(function () {
            if ($('#mainTbl tbody tr').length < 1) location.href = location.href;
        });

        local.getDocReplies();
    };
    this.regEvents = function () {
        // 문서댓글 새로고침 버튼
        $('#comment_refresh input[type=button]').on('click', function () {
            local.getDocReplies();
        });
        // 문서댓글 추가
        $('#new_comment_div2 input[type=button]').on('click', function (e) {
            e.preventDefault();
            var comment = $('#new_comment_div2 input[type=text]').val();
            $.ajax({
                url: '/api/v1/toolkit/workbench/docs/' + doc_id + '/comments',
                type: 'POST',
                data: {
                    comment: comment
                },
                async: true,
                success: function (args) {
                    console.log('9658 args : ', args);
                    if (args.result == 'OK') {
                        local.getDocReplies();
                        $('#new_comment_div2').find('input[type=text]').val('');
                    }
                },
                error: function (e) {
                    console.log('fail code : 5595');
                    console.log(e.responseText);
                }
            });
        });
        // 댓글 보기 아이콘 클릭 : 미리 가져오지 않고 실시간으로 댓글리스트 가져옴
        $(document).on('click', '.fa-comment', function () {
            showComment(null, this);
        });
        // 댓글창 닫기 아이콘 클릭
        $(document).on('click', '.fa-close', function () {
            $('#commentDiv').hide();
            $('#transArea, #resultArea').css({
                'opacity': '1'
            });
        });
        // 댓글 입력버튼 클릭
        $(document).on('click', '#new_comment_div input[type=button]', function () {
            $(this).blur();
            var sentence_id = $('#commentDiv').attr('data-sentence-id');
            var url = '/api/v1/toolkit/workbench/docs/' + doc_id + '/sentences/' + sentence_id + '/comments';
            console.log('url 4458 : ', url);
            var data = {
                'comment': $('#new_comment_div input[type=text]').val()
            };
            console.log('data 1145 : ', data);
            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                async: true,
                success: function (args) {
                    console.log('args 1254 : ', args);
                    if (args.result == 'OK') {
                        local.getComments('1', doc_id, sentence_id);
                        $('#new_comment_div').find('input[type=text]').val('');
                    }
                },
                error: function (e) {
                    console.log('fail 4592 : ' + e.responseText);
                }
            });
        });
        // 댓글 삭제아이콘 클릭
        $(document).on('click', '#comments img', function () {
            if (confirm('정말로 삭제하시겠습니까?')) {
                var sentence_id = $('#commentDiv').attr('data-sentence-id');
                var url = '/api/v1/toolkit/workbench/docs/sentences/comments/' + $(this).attr('data-id');
                console.log('url 2893 : ', url);
                $.ajax({
                    url: url,
                    type: 'DELETE',
                    async: true,
                    success: function (args) {
                        console.log('args 9876 : ', args);
                        if (args.result == 'OK') {
                            local.getComments('1', doc_id, sentence_id);
                        }
                    },
                    error: function (e) {
                        console.log('fail code : 4554');
                        console.log(e.responseText);
                    }
                });
            }
        });
        // 문서댓글 삭제아이콘 클릭
        $(document).on('click', '#doc_chat_content img', function () {
            if (confirm('정말로 삭제하시겠습니까?')) {
                var comment_id = $(this).closest('p').attr('data-comment-id');
                var url = '/api/v1/toolkit/workbench/docs/comments/' + comment_id;
                $.ajax({
                    url: url,
                    type: 'DELETE',
                    async: true,
                    success: function (args) {
                        console.log('args 7774 : ', args);
                        if (args.result == 'OK') {
                            local.getDocReplies();
                        }
                    },
                    error: function (e) {
                        console.log('fail code : 4411');
                        console.log(e.responseText);
                    }
                });
            }
        });
        // 단어장 검색버튼
        $('#btnPublicSearch').on('click', function (e) {
            e.preventDefault();
            var keyword = $('#txtPublicSearch').val();
            if (!IsValidStr(keyword)) {
                alert('단어를 입력해주세요');
                $('#txtPublicSearch').focus();
                return false;
            }
            var jqxhr = $.get('/api/v1/search?q=' + keyword + '&target=tb', function (data) {
                    console.log('/api/v1/search?q=' + keyword + '&target=tb');
                    console.log(data);
                    // 현재 출력된 단어들과 대조해서 출력되어 있을 경우 무시
                    var is_newword = true;
                    $('#tran2section table td div span.boldWord').each(function (idx, res) {
                        //alert($(this).text());
                        if (keyword.trim().toUpperCase() == $(this).text().trim().toUpperCase()) {
                            is_newword = false;
                            alert('아래 목록에 존재하는 단어입니다.');
                        }
                    });
                    //alert(is_newword);
                    if (is_newword) {
                        var result = '';
                        if (data != undefined && data.tb.length > 0) {
                            // DB에 단어가 있을 경우
                            if (!is_word) {
                                for (var i = 0; i < data.tb.length; i++) {
                                    result = '<div>';
                                    result += '    <input data-id="' + data.tb[i].term_id + '" type="button" value="수정 (' + data.tb[i].username + ')"> ';
                                    result += '    <span class="boldWord">' + $('#txtPublicSearch').val() + '</span> ';
                                    result += '    <input type="text" class="miniWord" value="' + data.tb[i].trans_text + '">';
                                    result += '</div>';
                                }
                                $('#tran2section table tr:nth-of-type(2) td').prepend(result);

                                $('#tran2section table tr:nth-of-type(2) input[type=text]').css({
                                    'border': '1px solid #999',
                                    'border-radius': '5px',
                                    'width': '98%',
                                    'margin': '2px auto',
                                    'padding-top': '5px',
                                    'padding-bottom': '5px',
                                    'padding-left': '5px'
                                });
                                // 단어수정
                                $('#tran2section table div input[type=button]').on('click', function (e) {
                                    e.preventDefault();
                                    var trans_word = $(this).closest('div').find('input[type=text]').val();
                                    var word_id = $(this).attr('data-id');
                                    var url = '/api/v1/toolkit/termbase/' + word_id;
                                    console.log('url : ', url);
                                    console.log('trans_word : ', trans_word);
                                    $.ajax({
                                        url: url,
                                        type: 'PUT',
                                        data: {
                                            origin_lang: trans_word,
                                            trans_lang: trans_word,
                                            origin_text: trans_word,
                                            trans_text: trans_word
                                        },
                                        success: function (args) {
                                            console.log(args);
                                            if (args.result == 'OK') {
                                                local.showMessage('수정되었습니다.');
                                            } else {
                                                local.showMessage('수정되지 않았습니다.');
                                            }
                                        },
                                        error: function (e) {
                                            local.showMessage('fail 386');
                                            console.log(e.responseText);
                                        }
                                    });
                                });
                            }
                        } else {
                            // DB에 단어가 없을 경우
                            result = '<div>';
                            result += '    <input type="button" value="등록"> ';
                            result += '    <span class="boldWord">' + $('#txtPublicSearch').val() + '</span> ';
                            result += '    <input type="text" class="miniWord" value="">';
                            result += '</div>';

                            $('#tran2section table tr:nth-of-type(2) td').prepend(result);

                            $('#tran2section table tr:nth-of-type(2) input[type=text]').css({
                                'border': '1px solid #999',
                                'border-radius': '5px',
                                'width': '98%',
                                'margin': '2px auto',
                                'padding-top': '5px',
                                'padding-bottom': '5px',
                                'padding-left': '5px'
                            });
                            // 단어등록
                            $('#tran2section table div input[type=button]').on('click', function (e) {
                                e.preventDefault();
                                var new_word = $(this).closest('div').find('.boldWord').text();
                                var new_word_trans = $(this).closest('div').find('input[type=text]').val();
                                //alert('new_word_trans : ', new_word_trans);
                                var data = {
                                    origin_lang: origin_lang,
                                    trans_lang: trans_lang,
                                    origin_text: new_word,
                                    trans_text: new_word_trans
                                };
                                console.log('data : ', data);
                                $.ajax({
                                    url: '/api/v1/toolkit/termbase/',
                                    type: 'post',
                                    data: data,
                                    async: true,
                                    success: function (args) {
                                        local.showMessage('등록되었습니다.');
                                    },
                                    error: function (e) {
                                        console.log('fail 113 : ' + e.responseText);
                                    }
                                });
                            });
                        }
                    }
                })
                .done(function () {})
                .fail(function () {
                    console.log("1548 error");
                })
                .always(function () {});
            jqxhr.always(function () {});
        });
        // 원문 클릭 : TB, TB, MT 검색
        $('#mainTbl tr td:nth-of-type(2)').on('click', function (e) {
            e.preventDefault();
            $('#loading_img1').show();
            $('#loading_img2').show();

            // 원문 클릭했을 때 (우측에) ajax api 호출, TM, MT 따로 호출해야 함!
            var thisText = $(this).text(),
                this_idx = $(this).closest('tr').prevAll().length,
                doc_id = getUrlParameter('doc_id'),
                sentence_id = $(this).closest('tr').find('td:eq(0)').text(); // this_idx : 1부터 시작

            $('#originSentence').html('');
            $('#originSentence').text(thisText);

            $('#resultTbl').html('');

            // TM, TB
            local.getTmAjax(doc_id, sentence_id, thisText, this_idx);

            // MT
            local.getMtAjax(thisText, this_idx);
        });
        // 번역문 textarea
        $('#mainTbl textarea').on('focusout', function (e) {
            e.preventDefault();
            local.saveTrans($(this));
        });
        // x 버튼 클릭 : 완료로 전환
        $('.fa-times').on('click', function (e) {
            e.preventDefault();
            local.saveTranStatus($(this), '1');
        });
        // 체크(완료) 버튼 클릭 : 미완료로 전환
        $('.fa-check').on('click', function (e) {
            e.preventDefault();
            local.saveTranStatus($(this), '0');
        });
        // 탭1
        $('#tabTbl td:nth-of-type(1)').on('click', function (e) {
            e.preventDefault();
            $('#resultTbl').show();
            $('#resultTbl2').show();
            $('#tabTbl td:nth-of-type(1)').css({
                'font-weight': 'bold',
                'border': '1px solid rgba(207, 204, 204, 0.404)',
                'border-top': '0px',
                'border-left': '0px',
                'background-color': 'rgb(252, 253, 252)'
            });
            $('#tabTbl td:nth-of-type(2)').css({
                'border': '1px solid rgba(207, 204, 204, 0.404)',
                'border-right': '0px',
                'border-bottom': '0px',
                'font-weight': 'normal',
                'background-color': '#fff'
            });
            $('#tran1section').show();
            $('#tran2section').show();
            $('#doc_chat').hide();
        });
        // 탭2
        $('#tabTbl td:nth-of-type(2)').on('click', function (e) {
            e.preventDefault();
            // $('#resultArea').css({
            //     'border': '0px solid rgba(207, 204, 204, 0.404)'
            // });
            $('#resultTbl').hide();
            $('#resultTbl2').hide();
            $('#tabTbl td:nth-of-type(1)').css({
                'font-weight': 'normal',
                'border-bottom': '0px',
                'border-left': '1px solid #fff',
                'border-top': '1px solid rgba(207, 204, 204, 0.404)',
                'background-color': '#fff'
            });
            $('#tabTbl td:nth-of-type(2)').css({
                'font-weight': 'bold',
                'border': '1px solid rgba(207, 204, 204, 0.404)',
                'border-top': '0px',
                'border-right': '0px',
                'background-color': 'rgb(252, 253, 252)'
            });
            $('#tran1section').hide();
            $('#tran2section').hide();
            $('#doc_chat').show();
        });

        // 완전히 로딩 후 로더 숨김
        $('#dvLoading').hide();

        // 마스크 해제       
        // 애니메이션 효과 - 일단 1초동안 초기화 됐다가 0% 불투명도로 변화.
        $('#mask').fadeIn(1000);
        $('#mask').fadeTo("slow", 1000).hide();
    };
    // 코멘트 리스트 가져오기
    this.getComments = function (user, doc, sentence) {
        //var url = '/api/v1/toolkit/workbench/docs/sentences/' + sentence + '/comments';
        var url = '/api/v1/toolkit/workbench/docs/' + doc_id + '/sentences/' + sentence + '/comments';
        console.log('5124 url');
        console.log(url);
        //var data = {};
        $.ajax({
            url: url,
            type: 'GET',
            //data: data,
            async: true,
            success: function (args) {
                console.log('args 9756 : ', args);
                var result = '';
                if (args.results != undefined) {
                    if (args.results.length > 0) {
                        $(args.results).each(function (idx, res) {
                            console.log('res 4586 : ', res);
                            result += '<p>' + res.name + ' : ' + res.comment + ' <img data-id="' + res.comment_id + '" src="/static/public/img/comment_del2.png"></p>';
                        });
                    } else {
                        result = '<p>등록된 의견이 없습니다.</p>';
                    }
                }
                console.log('result : ', result);
                $('#comments').html(result);
            },
            error: function (e) {
                console.log('fail 8431 : ' + e.responseText);
            }
        });
    };
    // 번역상태 저장
    this.saveTranStatus = function (thisObj, xy) {
        var sentence_id = thisObj.closest('tr').find('td:nth-of-type(1)').text();
        var url = '/api/v1/toolkit/workbench/docs/sentences/' + sentence_id + '/status/' + xy;
        console.log('[6545 url]');
        console.log(url);
        var x = thisObj.closest('tr').find('.fa-times');
        var y = thisObj.closest('tr').find('.fa-check');
        $.ajax({
            url: url,
            type: 'PUT',
            success: function (args) {
                console.log('[2145 args]');
                console.log(args);
                if (args.result == 'OK') {
                    if (xy == '1') {
                        // 번역상태 미완료 -> 완료로 변경
                        x.hide();
                        y.show();
                    } else {
                        // 번역상태 완료 -> 미완료로 변경
                        y.hide();
                        x.show();
                    }
                }
            },
            error: function (e) {
                console.log('fail 4595 : ' + e.responseText);
            }
        });
    };
    // 번역문 저장
    this.saveTrans = function (thisObj) {
        var sentence_id = thisObj.closest('tr').find('td:nth-of-type(1)').text();
        var url = '/api/v1/toolkit/workbench/docs/sentences/' + sentence_id + '/trans';
        console.log('4975 [번역문저장 url]');
        console.log(url);
        var trans_type = '';

        if (thisObj.val().trim() == '') trans_type = 'X';
        else {
            if (thisObj.closest('tr').find('td:nth-of-type(5)').text().trim() == '') {
                trans_type = 'T';
            } else {
                trans_type = thisObj.closest('tr').find('td:nth-of-type(5)').text().trim();
            }
        }
        var data = {
            trans_type: trans_type,
            trans_text: thisObj.val()
        };
        console.log('3391 [data]');
        console.log(data);
        $.ajax({
            url: url,
            type: 'PUT',
            data: data,
            success: function (args) {
                console.log('args 397 : ', args);
                if (args.result != 'OK') {
                    local.showMessage('번역문이 저장되지 않았습니다.');
                } else {
                    // 번역상태 미완료로 초기화
                    local.saveTranStatus(thisObj, '0');

                    if (trans_type == 'X') thisObj.closest('tr').find('td:eq(4)').removeClass().text('');
                    else if (trans_type == 'T') thisObj.closest('tr').find('td:eq(4)').removeClass().addClass('tColor').text('T');
                    // else if (trans_type == 'TM') thisObj.closest('tr').find('td:eq(4)').css({
                    //     'background-color': '#FF6FE6'
                    // }).text('TM');
                    // else if (trans_type == 'MT') thisObj.closest('tr').find('td:eq(4)').css({
                    //     'background-color': '#FCFCFC'
                    // }).text('MT');
                }
            },
            error: function (e) {
                local.showMessage('fail 281');
                console.log(e.responseText);
            }
        });
    };
    this.textAreaExpand = function () {
        $('#mainTbl').on('keyup', 'textarea', function (e) {
            e.preventDefault();
            $(this).css('height', 'auto');
            $(this).height(this.scrollHeight);
        });
        $('#mainTbl').find('textarea').keyup();
    };
    this.mask = function () {
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        $('#mask').css({
            'width': maskWidth,
            'height': maskHeight
        });
    };
    // TM 번역문 + 단어장 불러오기
    this.getTmAjax = function (doc_id, sentence_id, thisText, this_idx) {
        var url = '/api/v1/search?q=' + thisText + '&target=tm,tb&ol=' + origin_lang + '&tl=' + trans_lang;
        console.log('[2154 /api/v1/search?q=' + thisText + '&target=tb,tm&ol=' + origin_lang + '&tl=' + trans_lang + ']');
        console.log(url);
        var jqxhr = $.get(url, {
                sentence: thisText
            }, function (data) {
                console.log('## 결과 ################################');
                console.log('[data] ', data);
                console.log('[data.tm] ', data.tm);
                var tm_html = '';
                if (data.tm != undefined && data.tm.length > 0) {
                    for (var i = 0; i < data.tm.length; i++) {
                        tm_html += '<tr>';
                        tm_html += '    <td width="7%" style="text-align:center;">' + parseInt(i + 1) + '<br>(' + data.tm[i].score + '%)<br>' + data.tm[i].username + '</td>';
                        tm_html += '    <td width="5%" class="tmColor" style="text-align:center;">TM</td>';
                        tm_html += '    <td width="88%">' + data.tm[i].trans_text + '</td>';
                        tm_html += '</tr>';
                    }
                }
                $('#resultArea').css({
                    'border-top': '0'
                });
                $('#resultTbl').append(tm_html);

                $('#resultTbl tr').on('click', function (e) {
                    e.preventDefault();
                    //alert('1. 좌측에 해석문 입력\n2. 아이콘 x 로 변경 혹은 유지\n3. TM/TB/MT 선택에 따른 변경');
                    var transType = $(this).find('td:eq(1)').text();
                    var transBgClass = '';
                    switch (transType) {
                        case 'TM': // 문장
                            transBgClass = 'tmColor';
                            break;
                        case 'TB': // 단어
                            transBgClass = 'tbColor';
                            break;
                        case 'MT': // 실시간
                            transBgClass = 'mtColor';
                            break;
                        case 'T': // 자체
                            transBgClass = 'tColor';
                            break;
                    }
                    console.log('[transType] 5556 : ', transType);
                    console.log('[transBgClass] 8546 : ', transBgClass);
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(3) textarea').val($(this).find('td:nth-of-type(3)').text()).keyup();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(4) i:nth-of-type(2)').hide();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(4) i:nth-of-type(1)').show();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(5)').removeClass().addClass(transBgClass).html(transType);
                    local.saveTrans($('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(3) textarea'));
                });
                var tb_html = '';

                console.log('[5692 data.tb] ');
                console.log(data.tb);
                if (data.tb != undefined && data.tb.length > 0) {
                    for (var j = 0; j < data.tb.length; j++) {
                        tb_html += '<div>';
                        tb_html += '    <input type="button" data-id="' + data.tb[j].term_id + '" value="수정 (' +  data.tb[j].username + ')"> ';
                        tb_html += '    <span class="boldWord">' + data.tb[j].origin_text + '</span>';
                        tb_html += '    <input type="text" class="miniWord" value="' + data.tb[j].trans_text + '">';
                        tb_html += '</div>';
                    }
                }

                $('#tran2section table tr:nth-of-type(2) td').empty().append(tb_html);
                $('#tran2section table tr:nth-of-type(2) input[type=text]').css({
                    'border': '1px solid #999',
                    'border-radius': '5px',
                    'width': '98%',
                    'margin': '2px auto',
                    'padding-top': '5px',
                    'padding-bottom': '5px',
                    'padding-left': '5px'
                });
                $('#tran2section table div input[type=button]').on('click', function (e) {
                    e.preventDefault();
                    var org_word = $(this).closest('div').find('.boldWord').text();
                    var trans_word = $(this).closest('div').find('input[type=text]').val();
                    var word_id = $(this).attr('data-id');
                    $.ajax({
                        url: '/api/v1/toolkit/termbase/' + word_id,
                        type: 'PUT',
                        data: {
                            trans_text: trans_word
                        },
                        success: function (args) {
                            console.log('6695 [args]');
                            console.log(args);
                            if (args.result == 'OK') {
                                local.showMessage('수정되었습니다.');
                            } else {
                                local.showMessage('수정되지 않았습니다.');
                            }
                        },
                        error: function (e) {
                            local.showMessage('fail 386');
                            console.log(e.responseText);
                        }
                    });
                });
            })
            .done(function () {})
            .fail(function () {
                local.showMessage("error 348");
            })
            .always(function () {});
        jqxhr.always(function () {
            $('#loading_img1').hide();
            $('#loading_img2').hide();
        });
    };
    // MT 번역문 불러오기
    this.getMtAjax = function (thisText, this_idx) {
        var o_lang, t_lang;
        if (origin_lang == 'ko') o_lang = 1;
        else if (origin_lang == 'en') o_lang = 2;
        else if (origin_lang == 'zh') o_lang = 4;
        if (trans_lang == 'ko') t_lang = 1;
        else if (trans_lang == 'en') t_lang = 2;
        else if (trans_lang == 'zh') t_lang = 4;
        var data = {
            "source_lang_id": o_lang, // 1=한국어 2=영어 4=표준중국어
            "target_lang_id": t_lang, // 1=한국어 2=영어 4=표준중국어
            "where": "phone", // 노상관
            "sentence": thisText, // 번역할문장
            "user_email": "admin@sexycookie.com" // 일종의 암호로, 이거 바꾸면 안돌아가요
        };
        $.ajax({
            url: 'http://52.196.164.64/translate',
            type: 'post',
            data: data,
            async: true,
            success: function (args) {
                console.log('[args 5326] ', args);
                var mt_html = '';

                mt_html += '<tr>';
                mt_html += '    <td width="7%" style="text-align:center;">1</td>';
                mt_html += '    <td width="5%" class="mtColor" style="tsext-align:center;">MT</td>';
                mt_html += '    <td width="88%">' + args.ciceron + '</td>';
                mt_html += '</tr>';

                $('#resultArea').css({
                    'border-top': '0'
                });
                $('#resultTbl').append(mt_html);
                // 이벤트 등록
                $('#resultTbl tr').on('click', function (e) {
                    e.preventDefault();
                    //alert('1. 좌측에 해석문 입력\n2. 아이콘 x 로 변경 혹은 유지\n3. TM/TB/MT 선택에 따른 변경');
                    var transType = $(this).find('td:eq(1)').text();
                    var transBgClass = '';
                    switch (transType) {
                        case 'TM': // 문장
                            transBgClass = 'tmColor';
                            break;
                        case 'TB': // 단어
                            transBgClass = 'tbColor';
                            break;
                        case 'MT': // 실시간
                            transBgClass = 'mtColor';
                            break;
                        case 'T': // 자체
                            transBgClass = 'tColor';
                            break;
                    }
                    console.log('[transType] 8457 : ', transType);
                    console.log('[transBgClass] 3696 : ', transBgClass);
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(3) textarea').val($(this).find('td:nth-of-type(3)').text()).keyup();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(4) i:nth-of-type(2)').hide();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(4) i:nth-of-type(1)').show();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(5)').removeClass().addClass(transBgClass).text(transType);

                    local.saveTrans($('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(3) textarea'));
                });
            },
            error: function (e) {
                console.log('fail 4102 : ' + e.responseText);
            }
        });
    };
    // 문서댓글 출력
    this.getDocReplies = function () {
        console.log('/api/v1/toolkit/workbench/docs/' + doc_id + '/comments?page=' + page + '&rows=' + rows);
        //var data = {};
        $.ajax({
            url: '/api/v1/toolkit/workbench/docs/' + doc_id + '/comments?page=' + page + '&rows=' + rows,
            type: 'GET',
            //data: data,
            async: true,
            success: function (args) {
                console.log('5481 args');
                console.log(args);
                if (args != null && args != undefined) {
                    if (parseInt(args.total_cnt) > 0 && parseInt(args.results.length) > 0) {
                        $('#total_comment').html('의견공유 (' + args.total_cnt + ')');
                        var rows = '';
                        $(args.results).each(function (idx, args) {
                            if (args.sentence_id == '') {
                                rows += '<p data-comment-id="' + args.comment_id + '">[' + args.name + '] ' + args.comment;
                                rows += '    <img data-id="13" src="/static/public/img/comment_del2.png">';
                                rows += '</p>';
                            } else {
                                rows += '<p data-comment-id="' + args.comment_id + '"><a href="javascript:;" onclick="javascript:showComment(' + args.sentence_id + ', null);">' + args.sentence_id + '번 문장에 [' + args.name + ']님 의견이 추가되었습니다</a></p>';
                            }
                        });
                        $('#doc_chat_content').html(rows);
                        interval_sec = 600;
                    } else {
                        $('#doc_chat_content').html('아직 등록된 댓글이 없습니다.');
                    }
                }
            },
            error: function (e) {
                console.log('fail code : 8459');
                console.log(e.responseText);
            }
        });
    };
    // 인스턴트 메시지
    this.showMessage = function (msg) {
        $('#instant_div').text(msg);
        $('#instant_div').fadeIn();
        $('#transArea').css({
            'opacity': '0.2'
        });
        $('#resultArea').css({
            'opacity': '0.2'
        });
        $('#instant_div').fadeOut('slow');
        setTimeout(function () {
            $('#transArea').css({
                'opacity': '1'
            });
            $('#resultArea').css({
                'opacity': '1'
            });
            $('#instant_div').text('');
        }, 1000);
    };
    this.bind = function () {
        local.preInits();
    };
};

this.showComment = function (sid, thisObj) {
    $('#new_comment_div input[type=text]').val('');
    var script = new PageScript();
    var sentence_id;
    if (IsValidStr(sid)) sentence_id = sid;
    else sentence_id = $(thisObj).closest('tr').find('td:nth-of-type(1)').text();
    console.log(sentence_id);
    $('#sp_sentence').text(sentence_id);
    $('#comments').empty();
    $('#commentDiv').attr('data-sentence-id', sentence_id);
    script.getComments('7', script.doc_id, sentence_id);
    $('#commentDiv').show();
    $('#transArea').css({
        'opacity': '0.2'
    });
    $('#resultArea').css({
        'opacity': '0.2'
    });
};
$(function () {
    var script = new PageScript();
    script.bind();

    setTimeout(function () {
        script.regEvents();
        script.textAreaExpand();
        $('#mainTbl tr').show();
    }, 3000);

    // [실험적!] 600초(10분)에 한번씩 우측 문서댓글 리뉴얼
    setInterval(function () {
        script.getDocReplies();
    }, interval_sec * 1000);
    // 카운터
    setInterval(function () {
        $('#counter').text(interval_sec--);
    }, 1000);
});