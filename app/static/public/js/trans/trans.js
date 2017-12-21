var PageScript = function () {
    var local = this,
        project_id = getUrlParameter('project_id'),
        doc_id = getUrlParameter('doc_id');
    this.preInits = function () {
        // body 흐리게
        local.mask();

        // 원문 로딩
        var jqxhr = $.get("/api/v1/users/1/docs/1", function (data) {
                //console.log('data 11 : ', data);
                var html = '';
                $(data.result).each(function (idx, res) {
                    html += '<tr>';
                    html += '    <td>' + res.sentence_id + '</td>';
                    html += '    <td>' + res.origin_text + '</td>';
                    html += '    <td><textarea rows=1>' + res.trans_text + '</textarea></td>';
                    html += '    <td>';
                    if (res.status == '0') {
                        html += '    <i class="fa fa-times" aria-hidden="true" style="color:gray; cursor:pointer;"></i>';
                        html += '    <i class="fa fa-check" aria-hidden="true" style="color:orange; cursor:pointer; display:none;"></i>';
                    } else {
                        html += '    <i class="fa fa-times" aria-hidden="true" style="color:gray; cursor:pointer; display:none;"></i>';
                        html += '    <i class="fa fa-check" aria-hidden="true" style="color:orange; cursor:pointer;"></i>';
                    }
                    html += '    </td>';
                    if (res.trans_type == 'T') {
                        html += '<td>T</td>';
                    } else if (res.trans_type == 'TM') {
                        html += '<td class="tmColor">TM</td>';
                    } else if (res.trans_type == 'MT') {
                        html += '<td class="mtColor">MT</td>';
                    } else {
                        html += '<td></td>';
                    }
                    html += '    <td><i class="fa fa-comment" aria-hidden="true" style="color:gray;"></i></td>';
                    html += '</tr>';
                });
                $('#mainTbl tbody').append(html);
            })
            .done(function () {})
            .fail(function () {
                //alert("error"); // 시연에 방해될 수 있어서 일부러 주석처리함
            })
            .always(function () {});
        jqxhr.always(function () {
            if ($('#mainTbl tbody tr').length < 1) location.href = location.href;
        });
    };
    this.regEvents = function () {
        // 단어장 검색버튼
        $('#btnPublicSearch').on('click', function (e) {
            e.preventDefault();

            //alert('1. 디비에 저장된 현재 해석문 삭제\n2. 아이콘 체크에서 엑스로 변경');   
            /* 샘플	
            $.ajax({
                url: '/groups/sortGroup',  
                type:'post',
                data:data,
                success:function(args){   
                    alert('ok');
                },   
                error:function(e){  
                    alert('fail');  
                    console.log(e.responseText);  
                }  
            });		
            */

            var keyword = $('#txtPublicSearch').val();

            var result = '';
            if (confirm('검색단어가 있을경우')) {
                result = '<div>';
                result += '    <input type="button" value="수정"> ';
                result += '    <span class="boldWord">' + $('#txtPublicSearch').val() + '</span> ';
                result += '    <input type="text" class="miniWord" value="' + $('#txtPublicSearch').val() + ' 해석">';
                result += '</div>';

                $('#tran2section table tr:nth-of-type(2) td').prepend(result);
                //console.log(result);
                $('#tran2section table tr:nth-of-type(2) input[type=text]').css({
                    'border': '1px solid #999',
                    'border-radius': '5px',
                    'width': '150px',
                    'padding-left': '5px'
                });
                $('#tran2section table div input[type=button]').on('click', function (e) {
                    e.preventDefault();
                    alert($(this).closest('div').find('.boldWord').text() + ' 수정');
                });
            } else {
                result = '<div>';
                result += '    <input type="button" value="등록"> ';
                result += '    <span class="boldWord">' + $('#txtPublicSearch').val() + '</span> ';
                result += '    <input type="text" class="miniWord" value="">';
                result += '</div>';

                $('#tran2section table tr:nth-of-type(2) td').prepend(result);
                //console.log(result);
                $('#tran2section table tr:nth-of-type(2) input[type=text]').css({
                    'border': '1px solid #999',
                    'border-radius': '5px',
                    'width': '150px',
                    'padding-left': '5px'
                });
                $('#tran2section table div input[type=button]').on('click', function (e) {
                    e.preventDefault();
                    alert($(this).closest('div').find('.boldWord').text() + ' 등록');
                });
            }
        });
        // 원문 클릭
        $('#mainTbl tr td:nth-of-type(2)').on('click', function (e) {
            e.preventDefault();

            $(document).ajaxStart(function () {
                $('#dvLoading2').show();
            });
            $(document).ajaxComplete(function (event, request, settings) {
                $('#dvLoading2').hide();
            });

            // 원문 클릭했을 때 (우측에) ajax api 호출, TM, MT 따로 호출해야 함!
            var thisText = $(this).text(),
                this_idx = $(this).closest('tr').prevAll().length,
                doc_id = getUrlParameter('doc_id'),
                sentence_id = $(this).closest('tr').find('td:eq(0)').text(); // this_idx : 1부터 시작

            $('#originSentence').html('');
            $('#originSentence').text(thisText);

            $('#resultTbl').html('');

            // TM
            local.getTmAjax(doc_id, sentence_id, thisText, this_idx);

            // MT
            local.getMtAjax(thisText, this_idx);

            // TB
            local.getTBAjax();
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
            $('#resultTbl2').hide();
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
        });
        // 탭2
        $('#tabTbl td:nth-of-type(2)').on('click', function (e) {
            e.preventDefault();
            $('#resultArea').css({
                'border-top': '0'
            });
            $('#resultTbl').hide();
            $('#resultTbl2').show();
            $('#tabTbl td:nth-of-type(1)').css({
                'font-weight': 'normal',
                'border-bottom': '0px',
                'border-left': '0px',
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
        });

        // 완전히 로딩 후 로더 숨김
        $('#dvLoading').hide();

        // 마스크 해제       
        // 애니메이션 효과 - 일단 1초동안 초기화 됐다가 0% 불투명도로 변화.
        $('#mask').fadeIn(1000);
        $('#mask').fadeTo("slow", 1000).hide();
    };
    // 번역상태 저장
    this.saveTranStatus = function (thisObj, xy) {
        var sentence_id = thisObj.closest('tr').find('td:nth-of-type(1)').text();
        var url = '/api/v1/users/1/docs/1/sentences/' + sentence_id + '/status/' + xy;
        var y = thisObj.closest('td').find('.fa-check').hide();
        var x = thisObj.closest('td').find('.fa-times').show();
        $.ajax({
            url: url,
            type: 'PUT',
            success: function (args) {
                console.log(args);
                if (args.result == 'OK') {
                    if (xy == '1') {
                        // 번역상태 미완료 -> 완료로 변경
                        $(x).hide();
                        $(y).show();
                    } else {
                        // 번역상태 완료 -> 미완료로 변경
                        $(y).hide();
                        $(x).show();
                    }
                }
            },
            error: function (e) {
                alert('fail 174');
                console.log(e.responseText);
            }
        });
    };
    // 번역문 저장
    this.saveTrans = function (thisObj) {
        var sentence_id = thisObj.closest('tr').find('td:nth-of-type(1)').text();
        var url = '/api/v1/users/1/docs/' + getUrlParameter('doc_id') + '/sentences/' + sentence_id;
        var trans_type = '';

        if (thisObj.val().trim() == '') trans_type = '';
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
        console.log(data);
        $.ajax({
            url: url,
            type: 'PUT',
            data: data,
            success: function (args) {
                if (args.result != 'OK') alert('번역문이 저장되지 않았습니다.');
                else {
                    // 번역상태 미완료로 초기화
                    local.saveTranStatus(thisObj, '0');
                }
            },
            error: function (e) {
                alert('fail 281');
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
        //화면의 높이와 너비를 구한다.
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();

        //마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
        $('#mask').css({
            'width': maskWidth,
            'height': maskHeight
        });
    };
    // TM 번역문 불러오기
    this.getTmAjax = function (doc_id, sentence_id, thisText, this_idx) {
        var jqxhr = $.get("http://ciceron.xyz:5000/api/v2/mypick/" + doc_id + "/" + sentence_id, function (data) {
                var tm_html = '';

                tm_html += '<tr>';
                tm_html += '    <td width="4%" style="text-align:center;">1</td>';
                tm_html += '    <td width="5%" class="tmColor" style="text-align:center;">TM</td>';
                tm_html += '    <td width="91%">' + data.translated + '</td>';
                tm_html += '</tr>';

                $('#resultArea').css({
                    'border-top': '0'
                });
                $('#resultTbl').append(tm_html);
                // 이벤트 등록
                $('#resultTbl tr').on('click', function (e) {
                    e.preventDefault();
                    //alert('1. 좌측에 해석문 입력\n2. 아이콘 x 로 변경 혹은 유지\n3. TM/TB/MT 선택에 따른 변경');
                    var transType = $(this).find('td:eq(1)').text();
                    var transBgClass = '';
                    switch (transType) {
                        case 'TM':
                            transBgClass = 'tmColor';
                            break;
                        case 'TB':
                            transBgClass = 'tbColor';
                            break;
                        case 'MT':
                            transBgClass = 'mtColor';
                            break;
                    }
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(3) textarea').val($(this).find('td:nth-of-type(3)').text()).keyup();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(4) i:nth-of-type(2)').hide();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(4) i:nth-of-type(1)').show();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(5)').removeClass().addClass(transBgClass).html(transType);
                    local.saveTrans($('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(3) textarea'));
                });
            })
            .done(function () {})
            .fail(function () {
                alert("error 348");
            })
            .always(function () {});
        jqxhr.always(function () {});
    };
    // MT 번역문 불러오기
    this.getMtAjax = function (thisText, this_idx) {
        var data = {
            "source_lang_id": 2, // 1: 한국어 2: 영어
            "target_lang_id": 1, // 1: 한국어 2: 영어
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
                var mt_html = '';

                mt_html += '<tr>';
                mt_html += '    <td width="4%" style="text-align:center;">2</td>';
                mt_html += '    <td width="5%" class="mtColor" style="tsext-align:center;">MT</td>';
                mt_html += '    <td width="91%">' + args.google + '</td>';
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
                        case 'TM':
                            transBgClass = 'tmColor';
                            break;
                        case 'TB':
                            transBgClass = 'tbColor';
                            break;
                        case 'MT':
                            transBgClass = 'mtColor';
                            break;
                    }
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(3) textarea').val($(this).find('td:nth-of-type(3)').text()).keyup();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(4) i:nth-of-type(2)').hide();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(4) i:nth-of-type(1)').show();
                    $('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(5)').removeClass().addClass(transBgClass).html(transType);

                    local.saveTrans($('#mainTbl tr:nth-of-type(' + parseInt(this_idx + 1) + ') td:nth-of-type(3) textarea'));
                });
            },
            error: function (e) {
                //alert('fail 410');
                console.log('fail 410 : ' + e.responseText);
            }
        });
        // TB 단어장 불러오기
        this.getTBAjax = function () {
            var result = '';
            //alert('1. 디비에 저장된 현재 해석문 삭제\n2. 아이콘 체크에서 엑스로 변경');   
            /* 샘플	
            $.ajax({
                url: '/groups/sortGroup',  
                type:'post',
                data:data,
                success:function(args){   
                    alert('ok');
                },   
                error:function(e){  
                    alert('fail');  
                    console.log(e.responseText);  
                }  
            });		
            */
            result = '<div>';
            result += '    <input type="button" value="수정"> ';
            result += '    <span class="boldWord">book</span> ';
            result += '    <input type="text" class="miniWord" value="책">';
            result += '</div>';

            result += '<div>';
            result += '    <input type="button" value="수정"> ';
            result += '    <span class="boldWord">apple</span> ';
            result += '    <input type="text" class="miniWord" value="사과">';
            result += '</div>';

            $('#tran2section table tr:nth-of-type(2) td').empty().append(result);
            //console.log(result);
            $('#tran2section table tr:nth-of-type(2) input[type=text]').css({
                'border': '1px solid #999',
                'border-radius': '5px',
                'width': '150px',
                'padding-left': '5px'
            });
            $('#tran2section table div input[type=button]').on('click', function (e) {
                e.preventDefault();
                alert($(this).closest('div').find('.boldWord').text() + ' 수정');
            });
        };
    };
    this.bind = function () {
        local.preInits();
    };
};
$(function () {
    var script = new PageScript();
    script.bind();

    setTimeout(function () {
        script.regEvents();
        script.textAreaExpand();
        $('#mainTbl tr').show();
    }, 3000);
});